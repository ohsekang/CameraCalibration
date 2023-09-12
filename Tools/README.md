# Tools  
> 보정 프로세스에서 사용할 수 있는 몇 가지 가젯은 다음과 같습니다.
  
  
## collect.py    
> USB 카메라를 제어하여 이미지 또는 비디오 캡처  
  
```
python collect.py
```
argparse를 통해 더 많은 매개변수를 입력할 수 있으며, '-h'를 사용하여 모든 매개변수 정보를 확인할 수 있습니다.  
```
python collect.py -h
```
| Argument   | Type | Default   | Help                                             | 
|:-----------|:----:|:---------:|:-------------------------------------------------|
| -type      | str  | image     | Collect Data Type: image/video                   |
| -id        | int  | 1         | Camera ID                                        |
| -path      | str  | ./data/   | Input Video/Image Path                           |
| -name      | str  | test      | Save Video/Image Name                            |
| -fw        | int  | 1280      | Camera Frame Width                               |
| -fh        | int  | 720       | Camera Frame Height                              |
| -fps       | int  | 25        | Camera Frame per Second (FPS)                    |
  
'유형'이 이미지일 때 **스페이스바**를 눌러 이미지를 캡처하면 이미지가 표시되고 **Y**를 눌러 확인, **N**을 눌러 취소하면 여러 번 캡처할 수 있습니다.  
'유형'이 동영상일 때 **스페이스바**를 눌러 동영상 녹화를 시작하고 스페이스바를 다시 눌러 녹화를 중지하면 여러 번 녹화할 수 있습니다.
   
**예시**: 카메라 1에서 1280*1024 이미지를 캡처한 다음 실행합니다.
```
python collect.py -type image -id 1 -fw 1280 -fh 1024
```
리눅스에서는 카메라 이미지를 읽으려면 `cv2.VideoCapture(id)` 대신 `cv2.VideoCapture(f"/dev/video{id}")`를 사용하는 것이 좋습니다.  
  
--------------------------------------------------------------------------------  
  
## undistort.py  
> 카메라의 내부 기준 및 왜곡 벡터에 따라 원본 이미지의 왜곡을 제거합니다.  
  
처리할 원본 이미지와 캘리브레이션으로 생성된 결과 데이터(`카메라_K.npy` 및 `카메라_D.npy`)를 데이터 폴더에 넣거나 해당 경로 파라미터를 직접 입력합니다.
명령줄에서 실행하기만 하면 됩니다.
```
python undistort.py
```
argparse를 통해 더 많은 매개변수를 입력할 수 있으며, '-h'를 사용하여 모든 매개변수 정보를 확인할 수 있습니다.
```
python undistort.py -h
```
| Argument   | Type  | Default | Help                                              | 
|:-----------|:-----:|:-------:|:--------------------------------------------------|
| -width     | int   | 1280    | Camera Frame Width                                |
| -height    | int   | 1024    | Camera Frame Height                               |
| -load      | bool  | True    | Load New Camera K/D Data (True/False)             |
| -path_read | str   | ./data/ | Original Image Read Path                          |
| -path_save | str   | ./      | Undistortion Image Save Path                      |
| -path_k    | str   | ./data/camera_0_K.npy | Camera K File Path                  |
| -path_d    | str   | ./data/camera_0_D.npy | Camera D File Path                  |
| -focalscale| float | 1       | Camera Undistortion Focal Scale                   |
| -sizescale | float | 1       | Camera Undistortion Size Scale                    |
| -offset_h  | float | 0       | Horizonal Offset of Height                        |
| -offset_v  | float | 0       | Vertical Offset of Height                         |
| -srcformat | str   | jpg     | Source Image Format (jpg/png)                     |
| -dstformat | str   | jpg     | Destination Image Format (jpg/png)                |
| -quality   | int   | 100     | Save Image Quality (jpg:0-100, png:9-0 (low-high))|
| -name      | str   | None    | Save Image Name                                   |

**예시**: 여러 개의 'png' 원시 데이터를 처리하려면 '새 보정 데이터'를 불러와 '1280×720' 크기의 왜곡 제거된 이미지를 얻습니다.  
이름을 `undist_img`로 지정하고, `jpg` 형식으로 저장하고, `저장 품질`을 95로 설정하고, 다른 모든 것을 기본값으로 그대로 둔 다음 다음 명령을 실행합니다.
```
 python undistort.py -width 1280 -height 720 -load True -srcformat png -dstformat jpg -name undist_img -quality 95
```
스크립트 파일 경로에 있는 `-srcformat` 형식의 모든 이미지는 왜곡이 제거되고 새 이미지가 생성됩니다.
왜곡 제거 작업이 특정 이미지 하나에 대해서만 수행되는 경우 코드를 수정할 수 있습니다(코드에 이미 주석 처리됨).
  
--------------------------------------------------------------------------------  
  
## decomposeH.py   
> 회전 행렬 R과 이동 행렬 T는 단일 응력 행렬 H와 카메라 보간기 K에서 구할 수 있습니다(여러 결과를 살펴볼 수 있습니다).  
  
  
## timeAlign.py   
> 타임스탬프가 지정된 이미지를 시간별로 정렬하여 해당 목록을 가져올 수 있습니다.  
  
  
## img2vid.py   
> 연속 사진을 동영상으로 변환 가능  
  
