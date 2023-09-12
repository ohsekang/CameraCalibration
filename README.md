# Camera Calibration
> 차량 내 서라운드 뷰 카메라 보정 프로세스를 쉽게 완료할 수 있는 카메라 보정 관련 스크립팅 도구 모음입니다.  
> 각 코드 파일은 개별적으로 사용할 수 있으며, 외부 인터페이스도 호출할 수 있습니다. 
  
![](https://img.shields.io/badge/Language-python-blue.svg) 　
![](https://img.shields.io/badge/Requirement-openCV-brightgreen) 　
![License](https://img.shields.io/badge/License-GPL-orange.svg)

## DEMO
![DEMO](demo.gif)

## Quick Start
리포지토리를 복제하고 main.py를 실행하여 간단한 예제 결과를 확인합니다.  
opencv(>=3.4.2)**와 **numpy(>=1.19.2)**가 설치되어 있는지 확인합니다. 
```
git clone https://github.com/ohsekang/CameraCalibration.git
cd ./CameraCalibration
python main.py
```  
  
## File Tree  
> 프로젝트 구조 미리보기 
```
│  main.py                    // 주요 프로그램
│
├─ExtrinsicCalibration
│  │  extrinsicCalib.ipynb    // 외부 캘리브레이션 코드(주석 포함)
│  │  extrinsicCalib.py       // 외부 캘리브레이션을 위한 Python 코드
│  │  README.md               // 외부 캘리브레이션 문서
│  │  __init__.py             // init 파일, API 설명
│  │
│  └─data                     // 외부 기준 보정(캘리브레이션) 데이터 폴더
│
├─IntrinsicCalibration
│  │  intrinsicCalib.ipynb    // 내부 참조 보정 코드(설명 포함)
│  │  intrinsicCalib.py       // 내부 참조 보정 Python 코드
│  │  README.md               // 내부 참조 보정 문서
│  │  __init__.py             // init 파일, API 설명
│  │
│  └─data                     // 내부 참조 보정(캘리브레이션) 데이터 폴더
│
├─SurroundBirdEyeView
│  │  surroundBEV.ipynb       // 원형 조감도 코드(설명 포함)
│  │  surroundBEV.py          // 조감도 Python 코드 살펴보기
│  │  README.md               // 조감도 문서
│  │  __init__.py             // init 파일, API 설명
│  │
│  └─data                     // 원형 조감도용 파라미터 폴더
│     ├─front                 // 사전 저장된 카메라의 K, D, H 파라미터 파일
│     ├─back                  // 사전 저장된 카메라의 K, D, H 파라미터 파일
│     ├─left                  // 사전 저장된 카메라의 K, D, H 파라미터 파일
│     └─right                 // 사전 저장된 카메라의 K, D, H 파라미터 파일
│
└─Tools                       // 몇 가지 관련 보정 도구
    │  collect.py             // 이미지 획득
    │  undistort.py           // 이미지 왜곡 제거
    └─data                    // 데이터 폴더

```

  
## Camera Intrinsic Calibration 
> 카메라 내부 기준 보정
  
`intrinsicCalib.py`  [문서 보기](./IntrinsicCalibration/README.md/)  
**어안 카메라** 및 **일반 카메라** 모델을 포함한 카메라의 **온라인 보정** 및 **오프라인 보정**을 포함합니다.  
그리고 **카메라, 비디오, 이미지** 세 가지 입력을 지원하고 카메라 내부 참조 및 왜곡 벡터를 생성합니다.   

- 파이썬 파일을 직접 실행하고 argparse를 통해 더 많은 매개변수를 입력할 수 있으며, argparse 매개변수 목록은 설명서를 참조하세요.
```
python intrinsicCalib.py
```  

- 또한, 아래 설명된 바와 같이 호출을 위해 `InCalibrator` 클래스가 제공되며, **main.py**에 예제가 나와 있습니다. 
```
from intrinsicCalib import InCalibrator

calibrator = InCalibrator(camera_type)              # 내부 기준 캘리브레이터 초기화
for img in images:
    result = calibrator(img)                        # 원본 이미지를 한 번에 하나씩 읽어들여 보정 결과를 업데이트합니다.
undist_img = calibrator.undistort(raw_frame)        # 왜곡 제거 방법을 사용하여 왜곡된 이미지 얻기
```
또는 사전 정의된 보정 모드를 사용하려면 `CalibMode` 클래스를 호출하고, 각 모드에 대한 자세한 내용은 설명서를 참조하세요.  
```
from intrinsicCalib import InCalibrator, CalibMode

calibrator = InCalibrator(camera_type)              # 내부 기준 캘리브레이터 초기화
calib = CalibMode(calibrator, input_type, mode)     # 보정 모드 선택
result = calib()                                    # 보정 시작
```
원본 파일에서 각 파라미터를 직접 수정하거나 `get_args()` 메서드를 사용하여 파라미터를 가져와서 수정할 수 있습니다.
```
args = InCalibrator.get_args()                      # 인자 인수(args) 가져오기
args.INPUT_PATH = './IntrinsicCalibration/data/'    # args 매개변수 수정
calibrator = InCalibrator(camera_type)              # 내부 기준 캘리브레이터 초기화
```  

결과 예시:
<img src="https://i.loli.net/2021/06/22/nxOsU1mM4D3kJWS.png" width="750" height="200" alt="inCalib_result.jpg"/>  
<img src="https://i.loli.net/2021/06/22/iVETOUIMqCRHDYr.png" width="750" height="300" alt="inCalib_image.jpg"/>  
  
  
## Camera Extrinsic Calibration  
> 카메라 외부 기준 보정

`extrinsicCalib.py`  [문서 보기](./ExtrinsicCalibration/README.md/)    
카메라의 **외부 파라미터 보정**을 완료하고, (동일한 보정 플레이트 포함) 두 뷰의 **변환**을 실현하고, **단일 반응 변환 행렬**을 생성합니다.  
예를 들어, 지상을 동시에 촬영하는 **UAV 카메라**와 **차량에 장착된 서라운드 뷰 카메라**의 캘리브레이션 플레이트를 기반으로 차량 장착 카메라의 외부 파라미터를 캘리브레이션할 수 있습니다.  
차량 장착 카메라에서 드론 카메라로 단일 응답 변환 행렬을 생성하고 **조감도**의 변환을 구현합니다(즉, 차량 장착 카메라 시점을 드론 시점으로 변환).    
  
- 파이썬 파일을 직접 실행하고 argparse를 통해 더 많은 파라미터를 입력할 수 있으며, argparse 파라미터 목록은 설명서를 참조하세요.
```
python extrinsicCalib.py
```  
  
- 또한, 아래 설명된 바와 같이 호출을 위해 `ExCalibrator` 클래스가 제공되며, **main.py**에 예제가 나와 있습니다.  
```
from extrinsicCalib import ExCalibrator

exCalib = ExCalibrator()                            # 외부 기준 캘리브레이터 초기화
homography = exCalib(src_raw, dst_raw)              # 왜곡이 제거된 두 개의 이미지를 입력해 동형 행렬을 구합니다.
src_warp = exCalib.warp()                           # warp 메서드를 사용하여 원본 이미지의 변형 결과를 얻습니다.
```    
원본 파일에서 각 파라미터를 직접 수정하거나 `get_args()` 메서드를 사용하여 파라미터를 가져와서 수정할 수 있습니다.  
```
args = ExCalibrator.get_args()                      # 인자 인수(args) 가져오기
args.INPUT_PATH = './ExtrinsicCalibration/data/'    # args 매개변수 수정
exCalib = ExCalibrator()                            # 외부 기준 캘리브레이터 초기화
```    
  
결과 예시:  
![exCalib_result.jpg](https://i.loli.net/2021/06/22/5fMmcxTuZ2aIUyN.png)   
  
  
## Surround Camera Bird Eye View  
> 서라운드 카메라 조감도 스플라이스 생성  
  
`surroundBEV.py`  [문서 보기](./SurroundBirdEyeView/README.md/)    
앞, 뒤, 왼쪽, 오른쪽에서 4개의 **원시 카메라 이미지**를 입력해 **조감도**를 생성합니다.  
**직접 스티칭**과 **퓨전 스티칭**을 포함하며, **밝기 밸런스 및 화이트 밸런스**를 수행할 수 있습니다.   
  
- 파이썬 파일을 직접 실행하고 argparse를 통해 더 많은 파라미터를 입력할 수 있으며, argparse 파라미터 목록은 설명서를 참조하세요.
```
python surroundBEV.py
```  
  
- 또한, 아래 설명된 바와 같이 호출을 위해 `BevGenerator` 클래스가 제공되며, **main.py**에 예제가 있습니다.  
```
from surroundBEV import BevGenerator

bev = BevGenerator()                                # 서라운드 조감도 생성기를 초기화합니다.
surround = bev(front,back,left,right)               # 앞, 뒤, 좌, 우에서 4개의 원본 카메라 이미지를 입력하여 스티칭된 조감도를 얻습니다.
```    
위의 생성은 **실시간**을 보장하는 직접 스티칭의 결과이며, 퓨전 및 밸런싱도 사용할 수 있지만 다음과 같이 느린 속도로 사용할 수 있습니다.
```
bev = BevGenerator(blend=True, balance=True)        # 이미지 블렌딩 및 밸런싱 사용.
surround = bev(front,back,left,right,car)           # 차량 이미지 추가 가능
```
원본 파일에서 각 매개변수를 직접 수정하거나 `get_args()` 메서드를 사용하여 매개변수를 가져와서  
```
args = BevGenerator.get_args()                      # 서라운드 조감도 매개변수 가져옵니다.
args.CAR_WIDTH = 200
args.CAR_HEIGHT = 350                               # 새 파라미터로 수정합니다.
bev = BevGenerator()                                # 조감도 생성기를 초기화합니다.
```    
  
결과 예시: 
<div align=center><img src="https://i.loli.net/2021/06/22/fOwPsTYkCFeo8dW.png" width="740" height="170" alt="camera.jpg"/></div>  
<div align=center><img src="https://i.loli.net/2021/06/22/HeKJVBm2vEINy4z.png" width="360" height="400" alt="bev.jpg"/></div>   
   
   
## Other Tools
'collect.py'를 사용하여 이미지 또는 비디오의 **데이터 캡처**를 위해 카메라를 켭니다.
'undistort.py'를 사용하여 이미지 왜곡을 일괄 처리합니다.
'decomposeH.py'를 사용하여 유니-스토캐스틱 행렬 H와 카메라의 내부 파라미터 K로부터 **회전 행렬 R과 변환 행렬 T**를 가져옵니다(필터링할 결과가 두 개 이상 있을 수 있음).
'timeAlign.py'를 사용하면 **타임스탬프**로 명명된 **이미지를 시간별로 정렬**하여 해당 목록을 얻을 수 있습니다.   
'img2vid.py'를 사용하면 이미지를 동영상으로 변환할 수 있습니다.  
     
## License  
[GPL-3.0 License](LICENSE)  
  
  
*`Copyright (c) 2021 ZZH`*  
  
  
