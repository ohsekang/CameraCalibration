import cv2
import os
import numpy as np
from ExtrinsicCalibration import ExCalibrator
from IntrinsicCalibration import InCalibrator, CalibMode
from SurroundBirdEyeView import BevGenerator


def runInCalib_1():
    print("Intrinsic Calibration ......")
    calibrator = InCalibrator('fisheye')                # 내부 매개변수 교정기 초기화
    PATH = './IntrinsicCalibration/data/'
    images = os.listdir(PATH)
    for img in images:
        print(PATH + img)
        raw_frame = cv2.imread(PATH + img)
        result = calibrator(raw_frame)                  # 원본 이미지를 읽을 때마다 교정 결과가 업데이트됩니다.

    print("Camera Matrix is : {}".format(result.camera_mat.tolist()))
    print("Distortion Coefficient is : {}".format(result.dist_coeff.tolist()))
    print("Reprojection Error is : {}".format(np.mean(result.reproj_err)))

    raw_frame = cv2.imread('./IntrinsicCalibration/data/img_raw0.jpg')
    cv2.imshow("Raw Image", raw_frame)
    undist_img = calibrator.undistort(raw_frame)        # 왜곡되지 않은 방법을 사용하여 왜곡된 이미지를 얻습니다.
    cv2.imshow("Undistorted Image", undist_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def runInCalib_2():
    print("Intrinsic Calibration ......")
    args = InCalibrator.get_args()                      # 내부 매개변수 교정 인수 매개변수 가져오기
    args.INPUT_PATH = './IntrinsicCalibration/data/'    # 새 매개변수로 수정
    calibrator = InCalibrator('fisheye')                # 내부 매개변수 교정기 초기화
    calib = CalibMode(calibrator, 'image', 'auto')      # 교정 모드 선택
    result = calib()                                    # 교정 시작

    print("Camera Matrix is : {}".format(result.camera_mat.tolist()))
    print("Distortion Coefficient is : {}".format(result.dist_coeff.tolist()))
    print("Reprojection Error is : {}".format(np.mean(result.reproj_err)))

    raw_frame = cv2.imread('./IntrinsicCalibration/data/img_raw0.jpg')
    # calibrator.draw_corners(raw_frame)                  # 모서리 점 그리기
    cv2.imshow("Raw Image", raw_frame)
    undist_img = calibrator.undistort(raw_frame)        # 왜곡되지 않은 방법을 사용하여 왜곡된 이미지를 얻습니다.
    cv2.imshow("Undistort Image", undist_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def runExCalib():
    print("Extrinsic Calibration ......")
    exCalib = ExCalibrator()                            # 외부 매개변수 교정기 초기화

    src_raw = cv2.imread('./ExtrinsicCalibration/data/img_src_back.jpg')
    dst_raw = cv2.imread('./ExtrinsicCalibration/data/img_dst_back.jpg')

    homography = exCalib(src_raw, dst_raw)              # 호모그래피 행렬을 얻기 위해 해당하는 두 개의 왜곡된 이미지를 입력합니다.
    print("Homography Matrix is:")
    print(homography.tolist())

    src_warp = exCalib.warp()                           # Warp 메소드를 사용하여 원본 이미지의 변환 결과 얻기

    cv2.namedWindow("Source View", flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow("Source View", src_raw)
    cv2.namedWindow("Destination View", flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow("Destination View", dst_raw)
    cv2.namedWindow("Warped Source View", flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow("Warped Source View", src_warp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def runBEV():
    print("Generating Surround BEV ......")
    front = cv2.imread('./SurroundBirdEyeView/data/front/front.jpg')
    back = cv2.imread('./SurroundBirdEyeView/data/back/back.jpg')
    left = cv2.imread('./SurroundBirdEyeView/data/left/left.jpg')
    right = cv2.imread('./SurroundBirdEyeView/data/right/right.jpg')

    args = BevGenerator.get_args()                      # 조감도 인수 매개변수 가져오기
    args.CAR_WIDTH = 200
    args.CAR_HEIGHT = 350                               # 새 매개변수로 수정

    bev = BevGenerator(blend=True, balance=True)        # 둘러보기 조감도 생성기 초기화
    surround = bev(front, back, left, right)            # 전면, 후면, 왼쪽, 오른쪽의 4개의 원본 카메라 이미지를 입력하여 접합된 조감도를 얻습니다.

    cv2.namedWindow('surround', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow('surround', surround)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # runInCalib_1()
    runInCalib_2()
    runExCalib()
    runBEV()

if __name__ == '__main__':
    main()

