import argparse
import cv2
import numpy as np
import os

# 여기에서 매개변수 값을 수정하세요.
parser = argparse.ArgumentParser(description="Control Camera to Collect Data (Image/Video)")
parser.add_argument('-type', '--DATA_TYPE', default='image', type=str, help='Collect Data Type: image/video')
parser.add_argument('-id', '--CAMERA_ID', default=0, type=int, help='Camera ID')
parser.add_argument('-path', '--SAVE_PATH', default='./data/', type=str, help='Save Video/Image Path')
parser.add_argument('-name', '--SAVE_NAME', default='test', type=str, help='Save Video/Image Name')
parser.add_argument('-fw','--FRAME_WIDTH', default=1280, type=int, help='Camera Frame Width')
parser.add_argument('-fh','--FRAME_HEIGHT', default=720, type=int, help='Camera Frame Height')
parser.add_argument('-fps','--VIDEO_FPS', default=25, type=int, help='Camera Video Frame per Second')
args = parser.parse_args()

def main():        
    if not os.path.exists(args.SAVE_PATH):                                      # 경로 확인
        raise Exception("save path not exist")  
    DATA = np.empty([0,args.FRAME_HEIGHT,args.FRAME_WIDTH,3])                   # 수집된 데이터
    flag = False                                                                # 이미지 플래그 수집

    cap = cv2.VideoCapture(args.CAMERA_ID)                                      # 카메라 켜기
    if not cap.isOpened(): 
        raise Exception("camera {} open failed".format(args.CAMERA_ID))         # 활성화 실패 보고 오류
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.FRAME_WIDTH)                         # 카메라 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, args.VIDEO_FPS)                                   # 카메라 프레임 속도를 설정하세요. 카메라가 지원하는지 확인하세요.
    
    win1 = "camera_{}_frame".format(args.CAMERA_ID)
    win2 = "press y/n to validate"
    index = 0
    while True:                                                                 # 비디오 입력 교정
        key = cv2.waitKey(1)                                                    # 키보드 입력 받기
        ok, raw_frame = cap.read()                                              # 카메라에서 원시 프레임 읽기
        if not ok:                               
            raise Exception("camera read failed")                               # 동영상을 읽지 못했습니다.
        
        if args.DATA_TYPE == 'image':                                           # 【이미지 획득 모드】
            if key == 32:                                                       # 프레임 이미지를 캡처하려면 스페이스바를 누르세요.
                img = raw_frame.copy()                                          # 프레임 이미지를 임시로 저장
                flag = True
            if flag:
                cv2.namedWindow(win2, flags = cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                cv2.imshow(win2, img)
                if key in (ord("y"), ord("Y")):                                  # 이미지 캡처를 확인하려면 Y를 누르세요.
                    cv2.imwrite(args.SAVE_PATH + 'camera{}_'.format(args.CAMERA_ID) + args.SAVE_NAME + '{}.jpg'.format(len(DATA)),img)
                    DATA = np.append(DATA, [img], axis=0)
                    print(len(DATA))                                             # 현재 수집된 데이터의 양을 표시합니다.
                    flag = False
                    cv2.destroyWindow(win2)
                elif key in (ord("n"), ord("N")):                                # 이미지를 삭제하고 다시 가져오려면 N을 누르세요.
                    flag = False
                    cv2.destroyWindow(win2)

        elif args.DATA_TYPE == 'video':                                          # 【동영상 캡처 모드】
            if key == 32:                                                        # 스페이스 바를 눌러 비디오 녹화를 시작하세요
                if not flag:
                    videoWrite = cv2.VideoWriter(args.SAVE_PATH + 'camera{}_'.format(args.CAMERA_ID) + args.SAVE_NAME + '{}.mp4'.format(index), 
                                         cv2.VideoWriter_fourcc('M','P','4','V'), args.VIDEO_FPS, (args.FRAME_WIDTH,args.FRAME_HEIGHT))
                    flag = True 
                else:
                    flag = False                                                 # 녹음을 종료하려면 다시 스페이스바를 누르세요
                    videoWrite.release()
                    cv2.destroyWindow(win1)
                    win1 = "camera_{}_frame".format(args.CAMERA_ID)
                    print(index+1)
                    index += 1 
            if flag:
                win1 = "camera_{}_frame_COLLECTING......".format(args.CAMERA_ID)
                videoWrite.write(raw_frame)

        cv2.namedWindow(win1, flags = cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 창 크기를 수동으로 드래그할 수 있습니다.
        cv2.imshow(win1, raw_frame)    
        if key == 27: break                                                      # 종료하려면 ESC

    cap.release()
    cv2.destroyAllWindows() 
    
if __name__ == '__main__':
    main()
