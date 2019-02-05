import pandas as pd
import sys
# sys.path.append('/home/yongchen/anaconda3/lib/python3.6/site-packages')
# sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2 as cv
from ast import literal_eval as make_tuple
import os, argparse
import csv
import numpy as np

parser = argparse.ArgumentParser(description='Folder locations')
parser.add_argument('--parent_folder', dest='parent_location',          # /data1/posture_images_dataset/videos 2018_02_27
                    help='home directory', type=str)


args = parser.parse_args()
storage_loc = args.parent_location


def write_to_csv(folder):
    with open(os.path.join(storage_loc, folder, 'aligned_poselet_posture.csv'), 'w') as f:
        f.write('pose,image_name,Neck,RShoulder,RElbow,LShoulder,'
                'LElbow,RHip, RKnee, LHip, LKnee, Nose, REye,'
                'LEye, right_collar_angle, left_collar_angle, right_upper_arm_angle,'
                'right_forearm_angle, left_upper_arm_angle, left_forearm_angle,'
                'neck_to_right_hip_angle, right_thigh_angle, right_calf_angle,'
                'neck_to_left_hip_angle, left_thigh_angle, left_calf_angle, neck_angle,'
                'right_eye_angle, left_eye_angle, right_eye_to_back_angle,'
                'left_eye_to_back_angle, right_collar_lengt, left_collar_length,'
                'right_upper_arm_length, right_forearm_length, left_upper_arm_length,'
                'left_forearm_length, neck_to_right_hip_length, right_thigh_length,'
                'right_calf_length, neck_to_left_hip_length, left_thigh_length,'
                'left_calf_length, neck_length, right_eye_length, left_eye_length,'
                'right_eye_to_back_length, left_eye_to_back_length\n')
        writer = csv.writer(f, delimiter=',')
        writer.writerows(patient)
    f.close()


_, folders, _ = os.walk(storage_loc).__next__()
folders.sort()
# print(np.size(folders))

box_to_check = 0

for folder in folders:
    # if folder != '2017-06-20-0948-40':
    # if folder != '2017-07-10-2013-02':
    #    continue
    if not os.path.exists(os.path.join(storage_loc, folder, 'points.csv')):
        print('point.csv does not exist')
        continue

    if not os.path.exists(os.path.join(storage_loc, folder, 'patient_posture.csv')):
        print('patient.csv does not exist')
        continue

    if os.path.exists(os.path.join(storage_loc, folder, 'aligned_poselet_postur.csv')):
        aligned_data = pd.read_csv(os.path.join(storage_loc, folder, 'aligned_poselet_postur.csv'),
                       delimiter=',', dtype={'image_name': str})

        box_to_check += len(aligned_data['image_name'])

    else:
        bbox_data = pd.read_csv(os.path.join(storage_loc, 'patient_bbox.csv'),
                                delimiter=',', dtype={'image_name': str})
        if len(bbox_data['image_name']) > box_to_check:
            data = pd.read_csv(os.path.join(storage_loc, folder, 'points.csv'),
                               delimiter=',', dtype={'image_name': str})
            # print(data)
            # prev_img_name = data.iloc[start - 1]['image_name']
            all_pose = pd.read_csv(os.path.join(storage_loc, folder, 'patient_posture.csv'),
                                   delimiter=',', dtype={'image_name': str})

            start = 0

            num_detections = len(data['image_name'])
            all_body_points = data.iloc[:][['Neck', 'RShoulder', 'RElbow', 'LElbow', 'RHip',
                                            'RKnee', 'LHip', 'LKnee', 'Nose', 'REye', 'LEye']]
            # print(all_body_points)
            bbox_ranges = bbox_data.iloc[:][['x_min', 'y_min', 'x_max', 'y_max']]

            patient = []
            i = start
            # j = 0
            while i < num_detections:
                prev_match = 0
                img_name = data.iloc[i]['image_name']
                if_null = 0

                if pd.isnull(img_name):
                    img_name = prev_img_name
                    data.set_value(i, 'image_name', img_name)
                    box_to_check = box_to_check - 1
                    if_null = 1
                else:
                    prev_img_name = img_name

                box_img_name = bbox_data.iloc[box_to_check]['image_name']
                # print(img_name)
                # print(box_img_name)
                # print(i)
                # print(box_to_check)

                if (img_name == box_img_name):
                    # print('append')
                    nose_points = all_body_points.iloc[i][['Nose']]
                    reye_points = all_body_points.iloc[i][['REye']]
                    leye_points = all_body_points.iloc[i][['LEye']]

                    x_min = bbox_ranges.iloc[box_to_check][['x_min']]
                    x_min = x_min.item()
                    y_min = bbox_ranges.iloc[box_to_check][['y_min']]
                    y_min = y_min.item()
                    x_max = bbox_ranges.iloc[box_to_check][['x_max']]
                    x_max = x_max.item()
                    y_max = bbox_ranges.iloc[box_to_check][['y_max']]
                    y_max = y_max.item()

                    if (x_max == -1) & (x_min == -1) & (y_max == -1) & (y_min == -1):
                        box_to_check += 1
                        i += 1
                        if if_null == 0:
                            pose = all_pose.iloc[len(patient)]['pose']
                            nan = ['unclear'] + [img_name] + ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                         'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                         'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                         'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                         'nan', 'nan', 'nan', 'nan', 'nan', 'nan']
                            patient.append(nan)
                            # patient = pd.DataFrame(patient)
                        continue

                    matches = 0
                    for nose_point in nose_points:
                        if not pd.isnull(nose_point):
                            nose_point = make_tuple(nose_point)
                            nose_x = nose_point[0]
                            nose_y = nose_point[1]
                            if (x_min <= nose_x <= x_max) & (y_min <= nose_y <= y_max):
                                matches += 1

                    for reye_point in reye_points:
                        if not pd.isnull(reye_point):
                            reye_point = make_tuple(reye_point)
                            reye_x = reye_point[0]
                            reye_y = reye_point[1]
                            if (x_min <= reye_x <= x_max) & (y_min <= reye_y <= y_max):
                                matches += 1

                    for leye_point in leye_points:
                        if not pd.isnull(leye_point):
                            leye_point = make_tuple(leye_point)
                            leye_x = leye_point[0]
                            leye_y = leye_point[1]
                            if (x_min <= leye_x <= x_max) & (y_min <= leye_y <= y_max):
                                matches += 1
                    if matches > 0:
                        # print('append')
                        if if_null == 1:
                            # print('append')
                            if matches > prev_match:
                                patient.pop()
                                poselet = data.iloc[i].values
                                pose = all_pose.iloc[len(patient)][['pose']].values
                                info = np.append([pose], [poselet])
                                patient.append(info)
                                # j += 1
                        else:
                            # print('first match')
                            # print(i)
                            prev_match = matches
                            # pose = all_pose.iloc[j]['pose']
                            # print(pose)
                            poselet = data.iloc[i].values
                            pose = all_pose.iloc[len(patient)][['pose']].values
                            info = np.append([pose], [poselet])
                            patient.append(info)

                    else:
                        if if_null != 1:
                            pose = all_pose.iloc[len(patient)]['pose']
                            nan = ['incorrect'] + [img_name] + ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan',
                                                'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

                            # print(nan)
                            patient.append(nan)
                    box_to_check += 1
                i += 1
            # print(patient)
            write_to_csv(folder)
            print('write')
        else:
            print("no more bboxes")
            sys.exit()
