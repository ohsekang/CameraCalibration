# Camera Intrinsic Calibration
> 카메라 내부 기준의 온라인 보정
  
Requirement： opencv(>=3.4.2) numpy(>=1.19.2)  
  
카메라의 **온라인 보정** 및 **오프라인 보정**은 **어안 카메라** 및 **일반 카메라**용 모델이 포함된 `intrinsicCalib.py`를 사용하여 수행할 수 있습니다.  
**카메라, 비디오 및 이미지** 입력을 동시에 지원하고, **카메라 내부 참조** 및 **수차 벡터**를 생성하며, **리프루션 오류**를 표시합니다.  
자세한 코멘트는 `intrinsicCalib.ipynb`에 포함되어 있거나, Jupyter 노트북에서 직접 코드를 실행할 수 있습니다.   
도구에서 `undistort.py`를 사용하여 카메라 참조 및 왜곡 벡터 파일을 기반으로 이미지 왜곡을 제거할 수 있습니다.  
  

【디렉토리】  
- [Quick Start](#quick-start)
  * [intrinsicCalib.py](#intrinsiccalibpy)
    + 온라인 보정
    + 오프라인 보정
    + 수동 모드
    + 추가 설정
- [Calibration Principle](#calibration-principle)
- [Code Detailed Annotation](#code-detailed-annotation)

## Quick Start
### intrinsicCalib.py 
> 카메라 내부 기준 보정  

**카메라를 연결**하고 보드를 캘리브레이션할 준비를 마친 후 명령줄에서 실행하기만 하면 됩니다(기본 카메라 온라인 캘리브레이션)
```
python intrinsicCalib.py
```
argparse를 통해 더 많은 매개변수를 입력하거나 `-h` 또는 `--help`를 사용하여 모든 매개변수 정보를 확인할 수 있으며, **각 매개변수의 기본값을 참고하세요**
```
python intrinsicCalib.py -h
```

| Argument   | Type | Default   | Help                                             | 참고                             |
|:------------|:----:|:---------:|:-------------------------------------------------|:---------------------------------|
| -input     | str  | camera    | Input Source: camera/video/image                 | 입력 형식 카메라/비디오/이미지           |
| -type      | str  | fisheye   | Camera Type: fisheye/normal                      | 카메라 유형 어안/일반                |
| -id        | int  | 1         | Camera ID                                        | 카메라 번호                          |
| -path      | str  | ./data/   | Input Video/Image Path                           | 사진 및 비디오 입력 경로                |
| -video     | str  | video.mp4 | Input Video File Name (eg.: video.mp4)           | 입력 동영상 파일 이름(확장자 포함)          |
| -image     | str  | img_raw   | Input Image File Name Prefix (eg.: img_raw)      | 이미지 파일명 접두사 입력                |
| -mode      | str  | auto      | Image Select Mode: auto/manual                   | 자동/수동 모드 선택                 |
| -fw        | int  | 1280      | Camera Frame Width                               | 카메라 해상도 프레임 폭                 |
| -fh        | int  | 1024      | Camera Frame Height                              | 카메라 해상도 프레임 높이                |
| -bw        | int  | 7         | Chess Board Width (corners number)               | 보드 너비. [안쪽 모서리 번호(수)]             |
| -bh        | int  | 6         | Chess Board Height (corners number)              | 보드의 높이. [안쪽 모서리 번호(수)]             |
| -size      | int  | 10        | Chess Board Square Size (mm)                     | 보드 그리드 측면의 길이 mm                     |
| -num       | int  | 5         | Least Required Calibration Frame Number          | 보정된 사진 샘플의 최소 개수를 초기화합니다.        |
| -delay     | int  | 8         | Capture Image Time Interval (frame number)       | 샘플 사이의 프레임 수                  |
| -subpix    | int  | 5         | Corners Subpix Optimization Region               | 코너 좌표의 하위 픽셀 최적화를 위한 검색 영역 크기 |
| -fps       | int  | 20        | Camera Frame per Second (FPS)                    | 카메라 프레임 속도                       |
| -fs        | float| 0.5       | Camera Undistort Focal Scale                     | 디에버레이션을 위한 초점 거리 스케일링 계수            |
| -ss        | float| 1         | Camera Undistort Size Scale                      | 왜곡 제거를 위한 크기 스케일링 계수            |
| -store     | bool | False     | Store Captured Images (Ture/False)               | 캡처한 이미지 저장 여부                |
| -store_path| str  | ./data/   | Path to Store Captured Images                    | 캡처한 이미지를 저장할 경로              |
| -crop      | bool | False     | Crop Input Video/Image to (fw,fh) (Ture/False)   | 입력 비디오/이미지 크기를 fw fh로 자를지 여부 |
| -resize    | bool | False     | Resize Input Video/Image to (fw,fh) (Ture/False) | 입력 비디오/이미지 크기를 fw fh로 확대할지 여부 |
   
-------------------------------------------------------------------------------
   
이 프로그램은 카메라, 비디오 및 사진 입력에 대한 수동 / 자동 모드를 포함하여 'CalibMode'에서 **6 가지 보정 모드**를 사전 설정합니다.  
**온라인 카메라 보정**은 쉽고 빠르지만 정확도를 높이려면 **오프라인 비디오/사진 보정**을 권장합니다.  
(예: 카메라 보정 모드에서 '저장'을 True로 설정하고 캡처한 이미지를 저장한 다음 나중에 사진 수동 모드를 사용하여 좋은 품질의 선명한 이미지를 선택하고 정렬되지 않은 모서리를 제거합니다.) 
(또는 카메라를 사용하여 비디오를 녹화한 후 나중에 비디오 보정 모드를 사용하여 오프라인으로 보정하여 더 나은 결과를 선택할 수 있습니다.)  
아래 몇 가지 예를 통해 이를 설명합니다:  
   
#### 예 1(온라인 보정)  
**어안 카메라**의 자동 온라인 보정 시간입니다(기본 설정). 
카메라 해상도를 1280 x 720으로 설정하고 바둑판 격자 **모서리 점**의 수를 6 x 8, 각 셀 **측면**의 길이를 20mm(또는 기본값으로 그대로 둘 수 있음)로 설정하고 기본값을 유지하기 위해 매개변수를 입력하지 않은 경우 다음과 같이 입력합니다.  
```
python intrinsicCalib.py -fw 1280 -fh 720 -bw 6 -bh 8 -size 20
```  
(기본 `-ID 1` 카메라 입력 `-입력 카메라`, 어안 카메라 모델 `-타입 어안`, 자동 모드 `-모드 자동`)  
프로그램이 정상적으로 실행되고 카메라를 켜고 이미지를 읽으면 `raw_frame` 창이 나타납니다.  
- 카메라를 캘리브레이션 플레이트에 정렬
- **스페이스바**를 눌러 보정을 시작합니다.
- 다양한 각도에서 보드에 초점을 맞추는 스테디 모션 카메라 
  
카메라가 캘리브레이션 플레이트를 발견하고 일정량의 데이터를 획득하면 'undistort_frame' 창이 나타나며, 이 시점에서 초기 캘리브레이션이 완료되어 왜곡이 제거된 이미지가 생성됩니다.
- 데이터를 계속 수집하면 프로그램이 캘리브레이션 결과를 지속적으로 최적화합니다.
- 왜곡이 제거된 이미지가 안정되면 **ESC**를 눌러 종료하고 보정을 완료합니다.
  
보정 결과의 카메라 내부 기준 행렬은 `camera_{id}_K.npy`에 저장되며, 왜곡 계수 벡터는 `camera_{id}_D.npy`에 저장됩니다.  
여기서 {id}는 -id의 입력 파라미터로, **데이터의 관리 및 구분을 용이하게 하기 위해 캘리브레이션마다 해당 카메라의 ID 값을 입력하는 것을 권장합니다**.  
  
프로그램은 그림과 같이 실행됩니다.
![1.png](https://i.loli.net/2021/04/06/OAMVYJqezPcFhjI.png)  
  
보정 정확도를 향상시키는 데 필요합니다:
- 보드 보정 보드가 곧고 정확한지 확인합니다.
- 흔들림과 모션 블러를 최소화하기 위해 카메라를 안정적으로 유지하세요.
- 코너 포인트 수가 더 많은 캘리브레이션 플레이트 선택
- 조명 조건 확인
- 멀티 캘리브레이션
  
--------------------------------------------------------------------------------
  
#### 예 2(오프라인 보정)    
(참고: **동영상 또는 이미지를 . /데이터/에 저장하고 기본값**에 따라 이름을 지정하면 쉽게 사용할 수 있도록 매개변수 입력을 저장할 수 있습니다.) 
오프라인으로 보정하는 경우 입력은 로컬 비디오이고 파일은 . /데이터/비디오.mp4에 있고, 바둑판 모서리 점의 수가 6×8이며, 기본값을 유지하기 위해 매개변수를 입력하지 않은 경우 다음을 입력합니다.  
```
python intrinsicCalib.py -input video -path ./data/ -video video.mp4 -bw 6 -bh 8
```  

오프라인으로 보정하는 경우 입력은 로컬 이미지이고, 파일은 . /데이터/, 이미지 이름은 img_raw_xxx.xxx, 바둑판 모서리 점의 수는 7×6, 기본값을 유지하기 위해 매개변수를 입력하지 않은 경우 다음을 입력합니다.
```
python intrinsicCalib.py -input image -path ./data/ -image img_raw -bw 7 -bh 6
```    
**스크립트는 이 이름의 접두사가 포함된 입력 경로 아래의 모든 이미지를 입력으로 받습니다**.  
예제에 제공된 이미지를 읽고 보정 결과와 왜곡이 제거된 이미지를 확인하세요.  
![inCalib_result.jpg](https://i.loli.net/2021/06/22/nxOsU1mM4D3kJWS.png)   
  
--------------------------------------------------------------------------------
  
#### 예 3(수동 모드)   
자동 모드와 수동 모드 사이를 전환하려면 '모드'를 **자동** 또는 **수동**으로 변경합니다.  
수동 모드에서:  
- 카메라가 입력되는 동안 **스페이스바**를 누를 때마다 현재 프레임 이미지가 캘리브레이션 샘플로 캡처됩니다.
- 비디오 입력 시에도 마찬가지입니다.
- 이미지가 입력되면 사진을 한 장씩 읽은 후 **스페이스바**를 눌러 확인하고 다른 키를 눌러 사진을 삭제합니다.
- **ESC**를 눌러 보정을 완료하고 종료합니다.  
출력 화면에는 캡처된 유효한 이미지 수가 표시됩니다.  
예시:
```
python intrinsicCalib.py -input image -mode manual -fw 1280 -fh 1024 -bw 7 -bh 6
```    
  
--------------------------------------------------------------------------------  
  
#### 예제 4(추가 설정)  
`-fw` `-fh` `-fps` 카메라의 해상도와 프레임 속도를 설정할 때 **카메라가 이 설정을 지원하는지 확인**하세요. 
`-num` 는 보정에 필요한 최소 이미지 수(초기 보정 수일 뿐, 좋은 결과를 얻으려면 여전히 충분한 수의 유효한 이미지가 필요함)로, 보정 품질에 따라 조정할 수 있습니다.
`-size` 는 보드 그리드의 길이이며, 이 설정은 중요하지 않으므로 실제 크기를 모르는 경우 기본값으로 그대로 두십시오.  
`-subpix` 해상도 및 실제 보드 크기에 따라 조정된 모서리 하위 픽셀에 대한 최적화된 검색 영역, 지도의 저해상도 또는 작은 보드 크기는 아래쪽으로 조정해야 합니다.  
`-delay` 카메라 또는 비디오 입력을 자동 모드로 설정한 상태에서 x로 설정하면 매 x 프레임마다 샘플링하여 입력한다는 의미입니다.  
`-store` 카메라 또는 비디오 입력 시 True로 설정하면 캡처된 이미지(코너 포인트 감지)를 . /데이터/ 경로에 저장되며 **이미지 입력 수동 모드**를 사용하여 보정을 위해 다시 선택할 수 있습니다.  
`-fs` `-ss` 왜곡 제거를 위한 새로운 카메라 내 기준의 초점 거리 및 크기 배율을 사용하여 시야를 조정할 수 있습니다.  
`-crop` 입력으로 이미지 중앙의 (fw, fh) 크기를 자르면 대체 설정으로만 사용되며 일반적으로 사용되지 않습니다.
`-resize` 입력을 (fw,fh) 크기로 강제 설정하면 카메라의 내부 파라미터가 변경되며, 이는 백업 설정일 뿐 일반적으로 사용되지 않습니다.
  
例：
```
python intrinsicCalib.py  -fw 1280 -fh 720 -bw 6 -bh 8 -num 10 -delay 15 -store True -subpix 3 
```    
  
* 보다 심층적인 세부 설정의 경우 코드를 변경할 수 있습니다.  
  
#### 일반적인 문제  
- 리눅스에서는 카메라 이미지를 읽으려면 `cv2.VideoCapture(id)` 대신 `cv2.VideoCapture(f"/dev/video{id}")`를 사용하는 것이 좋습니다.  
- 카메라 보정 시 왜곡된 이미지에 이상이 있는 경우 계산이 분산되어 재투사 오차가 매우 커질 수 있으므로 ESC를 종료하여 재보정해야 합니다. 
- 일반적으로 분산은 이전 이미지의 품질이 좋지 않아 발생한 초기화 오류로 인한 것이며, 매개 변수 설정을 확인하여 보정 플레이트가 평평하고 직선인지 확인하고
  `-num` `-delay` `subpix` 등의 값을 수정하거나 이미지의 순서 등을 변경하거나 이미지를 다시 획득 할 수 있습니다.  
- 어안 카메라 모델은 일반 카메라 모델과 다르며, 특히 디왜곡 벡터의 표현이 다르며 자체 opencv 함수에 의해 처리됩니다.  
  
--------------------------------------------------------------------------------  
  
  
## Calibration Principle
> Reference: [OpenCV 공식 문서](https://docs.opencv.org/3.0.0/db/d58/group__calib3d__fisheye.html)、비주얼 슬램에 대한 14개의 강의

**어안 카메라(단안) 보정의 목적은 카메라의 내부 파라미터 K와 왜곡 계수 D를 구하는 것이며, 이에 따라 이미지의 왜곡을 제거할 수 있습니다**

[좌표 변환 관계]를 클릭합니다:  
![2.png](https://i.loli.net/2021/04/07/4Nwzeag9EZTrDWl.png)

월드 좌표계 Pw=(X,Y,Z)와 카메라 좌표계 Pc=(x,y,z)의 변환은 회전 행렬 R과 변환 벡터 t: [강체 변환]을 통해 구현할 수 있습니다.   
  
![1](http://latex.codecogs.com/svg.latex?\begin{bmatrix}{x}\\\\{y}\\\\{z}\\\\\end{bmatrix}=R\\cdot\\begin{bmatrix}{X}\\\\{Y}\\\\{Z}\\\\\end{bmatrix}+t)   

카메라의 비트 위치를 변환 행렬 **T=[R|t]**로 표시합니다:  

![2](http://latex.codecogs.com/svg.latex?\{P_c}=T{P_w})  

좌표 z를 정규화하여 정규화된 좌표를 얻고 극좌표계 r, θ를 사용하여 표현합니다:  
  
![3](http://latex.codecogs.com/svg.latex?\begin{cases}a=x\setminus{z}\\\\b=y\setminus{z}\\\\r^{2}=a^{2}+b^{2}\\\\\theta=atan(r)\\\\\end{cases})   
  
렌즈의 모양으로 인해 발생하는 수차는 방사상 수차와 접선 수차로 나눌 수 있으며, 중심과의 거리와 관련된 이차 및 고차 다항식 함수를 사용하여 보정할 수 있습니다.  
어안 카메라의 ** 수차에 대해서는 k1,k2,k3,k4를 계수로 하는 세타 다항식을 사용하여 설명하며, D=(k1,k2,k3,k4)**는 캘리브레이션 결과 중 하나입니다:  
  
![4](http://latex.codecogs.com/svg.latex?\\theta_{d}=\theta(1+k_{1}\theta^{2}+k_{2}\theta^{4}+k_{3}\theta^{6}+k_{4}\theta^{8}))  
  
카메라 좌표계 포인트는 디왜곡 후 다음과 같이 변환되며, Pc=(x',y',1)일 때입니다:  
  
![5](http://latex.codecogs.com/svg.latex?\begin{cases}x^{'}=(\theta_{d}\setminus{r})x\\\\y^{'}=(\theta_{d}\setminus{r})y\\\\\end{cases})  

카메라의 내부 파라미터 행렬 K는 다음과 같이 표현되며, **카메라의 내부 파라미터를 수학적으로 유도하여 캘리브레이션 결과 중 하나인 폐쇄 루프 솔루션**을 얻을 수 있습니다:  
  
![6](http://latex.codecogs.com/svg.latex?K=\begin{bmatrix}{f_{x}}&{0}&{c_{x}}\\\\{0}&{f_{y}}&{c_{y}}\\\\{0}&{0}&{1}\\\\\end{bmatrix})  
  
[원근 투영] 픽셀 좌표 Puv와 카메라 좌표 Pc 사이의 관계는 카메라 모델에서 얻을 수 있습니다:  
  
![7](http://latex.codecogs.com/svg.latex?\{P_u_v}=K{P_c}) 
  
투영 후 최종 픽셀 포인트 좌표는 다음과 같습니다(여기서 스큐 파라미터 α는 일반적으로 0입니다).  
  
![8](http://latex.codecogs.com/svg.latex?\begin{cases}u=f_{x}(x^{'}+\alpha{y^{'}})+c_{x}\\\\v=f_{y}y^{'}+c_{y}\\\\\end{cases})  
  
**캘리브레이션 프로세스** :
- 카메라가 이미지를 캡처합니다(일정한 간격으로)
- 체스판 모서리 찾기(cv2.findChessboardCorners), 모서리 좌표 가져오기
- 코너 좌표의 서브픽셀 최적화(cv2.cornerSubPix)는 [서브픽셀 최적화의 원리]를 참조하세요.(https://xueyayang.github.io/pdf_posts/%E4%BA%9A%E5%83%8F%E7%B4%A0%E8%A7%92%E7%82%B9%E7%9A%84%E6%B1%82%E6%B3%95.pdf)
- 예상 계산된 카메라 내부 기준(cv2.CALIB_USE_INTRINSIC_GUESS), [장정유 보정 방법 원리](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.558.1926&rep=rep1&type=pdf)
- 캘리브레이션 결과(cv2.fisheye.calibrate)를 얻고 새로운 데이터를 기반으로 지속적으로 최적화합니다.
- 카메라의 내부 기준 및 왜곡 벡터를 기반으로 매핑 행렬을 가져와 왜곡이 없는 변환 관계와 왜곡이 수정된 변환 관계를 계산합니다(cv2.fisheye.initUndistortRectifyMap).
- 이미지 왜곡 제거를 위한 리매핑(cv2.remap)
*_참고: 기능에 대한 자세한 내용은 공식 오픈CV 문서 또는 코드 주석*을 참조하세요.

## Code Detailed Annotation
intrinsicCalib.ipynb의 **중문 상세 코드 주석**은 [intrinsicCalib.ipynb]를 참조하세요.(https://nbviewer.jupyter.org/github/dyfcalid/CameraCalibration/blob/master/IntrinsicCalibration/intrinsicCalib.ipynb)  
  
`2021.6 ZZH`  

[맨 위로](#camera-calibration)

