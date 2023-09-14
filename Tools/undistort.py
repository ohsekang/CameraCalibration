import argparse
import os
import numpy as np
import cv2

# 여기에서 매개변수 값을 수정하세요.
parser = argparse.ArgumentParser(description="Fisheye Camera Undistortion")
parser.add_argument('-width', default=1280, type=int, help='Camera Frame Width')
parser.add_argument('-height', default=1024, type=int, help='Camera Frame Height')
parser.add_argument('-load', default=True, type=bool, help='Load New Camera K/D Data (True/False)')
parser.add_argument('-path_read', default='./data/', type=str, help='Original Image Read Path')
parser.add_argument('-path_save', default='./', type=str, help='Undistortion Image Save Path')
parser.add_argument('-path_k', default='./data/camera_0_K.npy', type=str, help='Camera K File Path')
parser.add_argument('-path_d', default='./data/camera_0_D.npy', type=str, help='Camera D File Path')
parser.add_argument('-focalscale', default=1, type=float, help='Camera Undistortion Focal Scale')
parser.add_argument('-sizescale', default=1, type=float, help='Camera Undistortion Size Scale')
parser.add_argument('-offset_h', default=0, type=float, help='Horizontal Offset of Optical Axis')
parser.add_argument('-offset_v', default=0, type=float, help='Vertical Offset of Optical Axis')
parser.add_argument('-srcformat', default='jpg', type=str, help='Original Image Format (jpg/png)')
parser.add_argument('-dstformat', default='jpg', type=str, help='Final Image Format (jpg/png)')
parser.add_argument('-quality', default=100, type=int, help='Save Image Quality (jpg:0-100, png:9-0 (low-high))')
parser.add_argument('-name', default=None, type=str, help='Save Image Name')
args = parser.parse_args()

def main():
    # 카메라 내부 매개변수와 왜곡 벡터를 직접 할당하거나 npy 파일을 로드할 수 있으며, 위의 args.load를 False로 수동으로 변경해야 합니다.
    if not args.load:
        camera_mat = np.array([[350.4931893001142, 0.0, 647.6297467576265], 
                               [0.0, 352.43072872484805, 513.5196785119657], 
                               [0.0, 0.0, 1.0]])
        dist_coeff = np.array([[-0.03367245449576437], [0.015380779195912842], 
                              [-0.018654590946883556], [0.0058128945633924185]])
    else:
        if not os.path.exists(args.path_k):
            raise Exception("Camera K File Path not exist")  
        if not os.path.exists(args.path_d):
            raise Exception("Camera D File Path not exist")  
        camera_mat = np.load(args.path_k)        # argparse에서 카메라 내부 매개변수 파일 경로 및 파일 이름 수정
        dist_coeff = np.load(args.path_d)        # argparse에서 왜곡 벡터 파일 경로 및 파일 이름 수정
    
    # 왜곡 제거, 광축 중심 맞추기, 초점 또는 프레임 조정 후의 새로운 카메라 내부 매개변수
    camera_mat_dst = camera_mat.copy()
    camera_mat_dst[0][0] *= args.focalscale
    camera_mat_dst[1][1] *= args.focalscale
    camera_mat_dst[0][2] = args.width / 2 * args.sizescale + args.offset_h
    camera_mat_dst[1][2] = args.height / 2 * args.sizescale + args.offset_v
    print(camera_mat.tolist())
    print(camera_mat_dst.tolist())
    print(dist_coeff.tolist())
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
                    camera_mat, dist_coeff, np.eye(3, 3), camera_mat_dst, 
                    (args.width * args.sizescale, args.height * args.sizescale), cv2.CV_16SC2) 
    
    # args.path_read의 모든 그림을 왜곡 제거하고 args.path_save 경로에 저장합니다.
    if not os.path.exists(args.path_read):
        raise Exception("Original Image Read Path not exist") 
    if not os.path.exists(args.path_save):
        raise Exception("Undistortion Image Save Path not exist") 
    filenames = os.listdir(args.path_read)       # argparse에서 이미지 경로 수정
    index = 1
    for filename in filenames:
        if filename[-4:] == '.' + args.srcformat:
        # if filename == 'img_src.jpg':          # 이 코드 줄을 사용하면 특정 이미지의 왜곡을 제거할 수 있습니다.
            print(filename)
            img = cv2.imread(args.path_read + filename)
            img = cv2.remap(img, map1, map2, cv2.INTER_LINEAR)
            
            if not args.name is None:
                filename = args.name + '_{:04d}.'.format(index) + args.srcformat  # argparse에 저장된 이미지의 접두사 이름을 입력하세요.
                index += 1
                
            if args.dstformat == 'jpg':
                cv2.imwrite(args.path_save + filename[:-4] + '.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, args.quality])
            elif args.dstformat == 'png':
                cv2.imwrite(args.path_save + filename[:-4] + '.png', img, [cv2.IMWRITE_PNG_COMPRESSION, args.quality])
            else:
                cv2.imwrite(filename[:-4] + '.' + args.dstformat, img)

if __name__ == '__main__':
    main()
    
