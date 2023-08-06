%%%%%%%%
% Title: template_registration_mscene.m
%
% Author: Young, Jenny, bue
% License: GPLv>=3
% Version: 2021-04-23
%
% Description:
%   Template script for matlab based IF registration for
%   one slide, one microscopy scene, all microscopy channel cyclic images.
%
% Instructions:
%   Use mplex_image.regist.registration function to edit and run this template.
%
% Input :
%   Tiffs or big tiffs (>4GB) with filename ending in m_regex_ext.
%   There can be as many files in the m_src_dir input folder as they want,
%   though m_regex_round, m_regex_marker, m_regex_micchannel and
%   m_glob_img_dapi, m_glob_img have to be slide_mscene specific,
%   whatever naming convention you follow.
%
%   E.g. ChinLab filename convention is:
%   Rx_Bi.o.mark.ers_Slidename-Section_xxx_xx_x_-Scene_cx_ORG.tif,
%   where channel c1 is DAPI and x can be variable (i.e. from axioscan)
%
% Output:
%    The output tiff files in m_dst_dir folder will follow the naming convention:
%    Registered-round<>marker<>slidepxscene<>micchanel<>ext
%    Make sure that you integrate a separator (symbolized by <>) into your regex patterns.
%%%%%%%%%%%%%%%%

% input parameter slides and scenes
m_slide = 'peek_s_slide';  % slide label which will be used in the filename
m_mscene = 'peek_s_mscene';  % bue 20210423: will this be used at all?
m_pxscene = peek_sls_pxscene;  % list of pxscene label strings string
% input parameter crop coordinates
m_crop = peek_sll_pxcrop;  % list of list of crop coordinates string
% input parameter file extension
m_regex_ext = 'peek_s_regex_ext';  % file extension rexgex pattern
% input parameter round
m_regex_round_ref = 'peek_s_regex_round_ref';  % reference staining round regexp pattern
m_regex_round_nonref = 'peek_s_regex_round_nonref';  % staining round regexp pattern (capturing rounds other than ref round is crucial. capturing ref round too is ok.)
% input parameter marker
m_regex_marker_ref = 'peek_s_regex_marker_ref';  % reference round stain regex pattern
m_regex_marker_nonref = 'peek_s_regex_marker_nonref';  % stain regex pattern (capturing stains other than ref round is crucial. capturing ref round stains too is ok.)
% input parameter micchannel
m_regex_micchannel_ref = 'peek_s_regex_micchannel_ref';  % reference round microscopy channel regex pattern
m_regex_micchannel_nonref = 'peek_s_regex_micchannel_nonref';  % microscopy channel regex pattern (capturing microscopy channels other than ref round is crucial. capturing ref round microscopy channel too is ok.)
% input parameter dapi images
m_glob_img_dapiref = 'peek_s_glob_img_dapiref';  % slide_mscene specific ref round dapi channel image glob pattern
m_glob_img_dapinonref = 'peek_s_glob_img_dapinonref';  % slide_mscene specific dapi channel image glob pattern (capturing dapi channels other than ref round is crucial. capturing ref round dapi channel too is ok.)
% input parameter dapi and non-dapi images
m_glob_img_ref = 'peek_s_glob_img_ref';  % slide_mscene specific ref round image glob pattern
m_glob_img_nonref = 'peek_s_glob_img_nonref';  % slide_mscene specific image glob pattern (capturing images other then ref round is crucial. capturing ref round images too is ok.)
% input parameter filesystem
m_src_dir = 'peek_s_src_dir';  % location of raw images folder
m_dst_dir = 'peek_s_dst_dir';  % location of folder where registered images will be stored
% input parameter registration
m_npoint = peek_i_npoint;  % number of features to detect in image (default = 10000)


% specify run
sprintf('\nrun slide mscene: %s%s', m_slide, m_mscene)
sprintf('input path: %s', m_src_dir)
sprintf('output path: %s', m_dst_dir)

% get dapi reference round file name
m_filedapi_ref = dir(strcat(m_src_dir, m_glob_img_dapiref));
if length(m_filedapi_ref) < 1
   sprintf(strcat('Error: no DAPI reference round file found with glob:', m_src_dir, m_glob_img_dapiref))
   %exit
elseif length(m_filedapi_ref) > 1
   sprintf(strcat('Error: more than 1 DAPI reference round file found with glob:', m_src_dir, m_glob_img_dapiref))
   %exit
end

% get dapi file name for all rounds
m_filedapi_nonref = dir(strcat(m_src_dir, m_glob_img_dapinonref));
if length(m_filedapi_nonref) < 1
   sprintf(strcat('Error: no DAPI files found with glob:', m_src_dir, m_imgdapi_glob))
   %exit
end

% get all file name for reference rounds
%m_fileall
m_file_ref = dir(strcat(m_src_dir, m_glob_img_ref));
if length(m_file_ref) < 1
   sprintf(strcat('Error: no refernce round files found with glob:', m_src_dir, m_glob_img_ref))
   %exit
end

% get all file name for all rounds
%m_fileall
m_file_nonref = dir(strcat(m_src_dir, m_glob_img_nonref));
if length(m_file_nonref) < 1
   sprintf(strcat('Error: no files found with glob:', m_src_dir, m_file_nonref))
   %exit
end


%% handle reference round %%
sprintf('get keypoints reference round DAPI image: %s', m_filedapi_ref.name)

% load dapi reference file and get key points
m_dapi_ref = imread(strcat(m_src_dir, m_filedapi_ref.name));  % load DAPI reference file
m_dapi_ref = imadjust(m_dapi_ref);  % adjust DAPI R1
m_point_ref = detectSURFFeatures(m_dapi_ref);  % detect features of DAPI reference (alternative method detectKAZEFeatures)
m_point_ref = m_point_ref.selectStrongest(m_npoint);  % select m_point (e.g. 10000) strongest feature
[m_feature_ref, m_validpoint_ref] = extractFeatures(m_dapi_ref, m_point_ref);  % get features and locations of DAPI R1

% get reference coordinate system
m_outputview_ref = imref2d(size(m_dapi_ref));

% clear
clear m_dapi_ref;
clear m_point_ref;

% extract round, marker, and file extension metadata from dapi ref file name
m_round_ref = regexp(m_filedapi_ref.name, m_regex_round_ref, 'tokens');
m_round_ref = m_round_ref{1}{1};
m_marker_ref = regexp(m_filedapi_ref.name, m_regex_marker_ref, 'tokens');
m_marker_ref = m_marker_ref{1}{1};
m_ext = regexp(m_filedapi_ref.name, m_regex_ext, 'tokens');
m_ext = m_ext{1}{1};

% for each file form this reference round, dapi and non-dapi
for i = 1:length(m_file_ref)
    if contains(m_file_ref(i).name, m_round_ref)
        sprintf('process reference round DAPI and non-DAPI image: %s', m_file_ref(i).name)

        % extract microscopy metadata for file name
        m_micchannel_ref = regexp(m_file_ref(i).name, m_regex_micchannel_ref, 'tokens');
        m_micchannel_ref = m_micchannel_ref{1}{1};

        % load file
        m_img = imread(strcat(m_src_dir, m_file_ref(i).name));

        % for each pxscene
        for j = 1:length(m_crop)

            % crop
            if strcmp(m_crop{j},'none')
                m_imgj = m_img;
            else
                m_imgj = imcrop(m_img, m_crop{j});
            end

            % save file
            s_pathfilename = sprintf('%s%s%s/Registered-%s%s_%s%s_%s_%s', m_dst_dir, m_slide, m_pxscene{j}, m_round_ref, m_marker_ref, m_slide, m_pxscene{j}, m_micchannel_ref, m_ext);
            sprintf('write file: %s', s_pathfilename)
            mkdir(strcat(m_dst_dir, m_slide, m_pxscene{j}));
            imwrite(m_imgj, s_pathfilename);

            % clean
            clear m_imgj;
        end
        clear m_img;
    end
end


%% registration loop %%
for i = 1:length(m_filedapi_nonref)

    % for each non reference round dapi file
    if not(strcmp(m_filedapi_nonref(i).name, m_filedapi_ref.name))
        sprintf('\nget keypoints non-reference round DAPI image: %s', m_filedapi_nonref(i).name)

        % load non-reference dapi file and get key points
        m_dapi_nonref = imread(strcat(m_src_dir, m_filedapi_nonref(i).name));  % load non-reference DAPI file
        m_dapi_nonref = imadjust(m_dapi_nonref);  % adjust non-refrence DAPI image
        m_point_nonref = detectSURFFeatures(m_dapi_nonref);  % detect features of non-reference DAPI (alternative method detectKAZEFeatures)
        m_point_nonref = m_point_nonref.selectStrongest(m_npoint);  % select m_point (e.g. 10000) strongest feature
        [m_feature_obj, m_validpoint_obj] = extractFeatures(m_dapi_nonref, m_point_nonref);  % get features and locations of non-refrence DAPI

        % get key point reference on reference pairs
        m_indexpair = matchFeatures(m_feature_ref, m_feature_obj);
        m_matched_ref = m_validpoint_ref(m_indexpair(:,1));  % validPtsRef
        m_matched_obj = m_validpoint_obj(m_indexpair(:,2));  % validPtsObj

        % actual registration
        [m_tform, m_inlier_distorted, m_inlier_original, m_status] = estimateGeometricTransform(m_matched_obj, m_matched_ref,  'similarity', 'MaxNumTrials',20000, 'Confidence',95, 'MaxDistance',10);
        [m_dapi_registered, m_dapiref_registered] = imwarp(m_dapi_nonref, m_tform, 'OutputView', m_outputview_ref);

        % clear
        clear m_dapi_nonref;
        clear m_point_nonref;
        clear m_indexpair;
        clear m_matched_ref;
        clear m_matched_obj;
        clear m_feature_obj;
        clear m_validpoint_obj;
        clear m_inlier_distorted;
        clear m_inlier_original;
        clear m_status;
        clear m_dapi_registered;
        clear m_dapiref_registered;

        % extract round, marker metadata from file name
        m_round_nonref = regexp(m_filedapi_nonref(i).name, m_regex_round_nonref, 'tokens');
        m_round_nonref = m_round_nonref{1}{1};
        m_marker_nonref = regexp(m_filedapi_nonref(i).name, m_regex_marker_nonref, 'tokens');
        m_marker_nonref = m_marker_nonref{1}{1};

        % for each file from this round, dapi and non-dapi
        for i = 1:length(m_file_nonref)
            if contains(m_file_nonref(i).name, m_round_nonref)
                sprintf('process non-reference round DAPI and non-DAPI image: %s', m_file_nonref(i).name)

                % extract microscopy metadata for file name
                m_micchannel_nonref = regexp(m_file_nonref(i).name, m_regex_micchannel_nonref, 'tokens');
                m_micchannel_nonref = m_micchannel_nonref{1}{1};

                % load file
                m_img = imread(strcat(m_src_dir, m_file_nonref(i).name));

                % transform
                [m_marker_registered, m_markerref_registered] = imwarp(m_img, m_tform, 'OutputView',m_outputview_ref); %transform all rounds 2 and higher

                % clear
                clear m_img;
                clear m_markerref_registered;

                % for each pxscene
                for j = 1:length(m_crop)

                    % crop
                    if strcmp(m_crop{j}, 'none')
                        m_marker_registeredj = m_marker_registered;
                    else
                        m_marker_registeredj = imcrop(m_marker_registered, m_crop{j});
                    end

                    % save file
                    s_pathfilename = sprintf('%s%s%s/Registered-%s%s_%s%s_%s_%s', m_dst_dir, m_slide, m_pxscene{j}, m_round_nonref, m_marker_nonref, m_slide, m_pxscene{j}, m_micchannel_nonref, m_ext);
                    sprintf('write file: %s', s_pathfilename)
                    imwrite(m_marker_registeredj, s_pathfilename);

                    % clear
                    clear m_marker_registeredj;
                end
                clear m_marker_registered;
             end
        end
    end
    clear m_tform;
end

%that's all, folk!
sprintf('finish!')
%exit
