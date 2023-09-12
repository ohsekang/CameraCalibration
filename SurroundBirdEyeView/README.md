# Surround Camera Bird Eye View Generator
> 차량에 장착된 서라운드 뷰 카메라 스티칭의 항공 뷰 생성  
  

## surroundBEV.py
조감도를 생성하려면 **전면, 후면, 좌측 및 우측의 4개의 원시 카메라 이미지**를 입력합니다.
**밝기 밸런싱 및 화이트 밸런싱**이 가능한 **다이렉트 스플라이싱 및 퓨전 스플라이싱**이 포함됩니다.
  
네 대의 카메라의 K, D, H 파라미터 파일과 원본 카메라 이미지는 데이터 아래에 4개의 별도 파일에 저장됩니다(기본 파일에 표시된 대로).  
명령줄에서 실행
```
python surroundBEV.py
```
argparse를 통해 더 많은 매개변수를 입력하거나 `-h` 또는 `--help`를 사용하여 모든 매개변수 정보를 확인할 수 있으며, **각 매개변수의 기본값을 참고하세요**.
```
python surroundBEV.py -h
```
| Argument   | Type | Default   | Help                                             | 참고                    |
|:-----------|:----:|:---------:|:-------------------------------------------------|:----------------------- |
| -fw        | int  | 1280      | Camera Frame Width                               | 카메라 원시 이미지 너비        |
| -fh        | int  | 1024      | Camera Frame Height                              | 카메라 원시 이미지 높이        |
| -bw        | int  | 1000      | Chess Board Width (corners number)               | 체스 판 너비(모서리 번호)          |
| -bh        | int  | 1000      | Chess Board Height (corners number)              | 체스 판 높이(모서리 번호)          |
| -cw        | int  | 250       | Car Frame Width                                  | 차량 사진 너비            |
| -ch        | int  | 400       | Car Frame Height                                 | 차량 사진 높이            |
| -fs        | float| 1         | Camera Undistort Focal Scale                     | 왜곡 제거를 위한 초점 거리 스케일링 계수  |
| -ss        | float| 2         | Camera Undistort Size Scale                      | 왜곡 제거를 위한 크기 스케일링 계수  |
| -blend  | bool  | False   | Blend BEV Image (Ture/False)                         | 이미지 융합 유무에 관계없이 조감도 스티칭하기  |
| -balance| bool | False   | Balance BEV Image (Ture/False)                        | 조감도 스티칭에 이미지 밸런싱을 사용할지 여부  |

**참고**: 위의 파라미터 설정 및 해당 파일**은 링뷰 이미지 스티칭의 예시**일 뿐이며, 자신의 카메라 등에 사용하려면 **내부 및 외부 파라미터 보정** 단계를 완료하여 교체용 해당 파일을 받으시기 바랍니다.   
** 여기의 모든 파라미터 설정이 내부 및 외부 파라미터 보정 및 디스토션과 동일한지 확인하세요! ** (특히 디스토션 계수)  
차량 사진은 적절한 크기로 조정하고 인수에 `-cw` `-ch` 파라미터를 동기화하여 변경할 수 있습니다.   

이미지 블렌딩 및 이미지 밝기 컬러 밸런스 작업은 '-blend' 및 '-balance' 매개변수를 (True/False)로 설정하여 활성화할 수 있습니다.  
또는 BevGenerator 클래스를 초기화할 때 다음과 같이 파라미터를 직접 전달합니다.
```
bev = BevGenerator(blend=True, balance=True)
```

실시간 조감도 생성을 위해서는 **BevGenerator 클래스**를 호출하여 4개의 카메라 이미지를 실시간으로 읽어들인 후 함수에 전달하여 조감도를 생성하는 것을 권장합니다.
```
from surroundBEV import BevGenerator

bev = BevGenerator()                                # 조감도 생성기 초기화하기
surround = bev(front,back,left,right)               # 앞, 뒤, 왼쪽, 오른쪽에서 4개의 원본 카메라 이미지를 입력하면 조감도를 스티칭할 수 있습니다.
```
  
------------------------------------------------------------------------------------------------------  
  
스티칭은 중간 차량 사진의 치수를 기준으로 **프리셋 마스크**를 사용하여 수행됩니다.  
직접 접합하려면 차량 사진의 네 모서리와 조감도의 네 모서리를 가져와서 해당 마스크를 얻습니다.
융합 접합의 경우 마스크 간에 겹치도록 더 큰 영역을 취하고 두 마스크와의 거리를 기준으로 겹치는 영역에서 가중치를 계산합니다.
다음 그림과 같이(예시: 전면 보기 마스크):
![mask.jpg](https://i.loli.net/2021/06/22/Sm6wlYzqTxZahpg.png)
  
**결과 연결하기**:  
![surround.jpg](https://i.loli.net/2021/06/22/2JRw31FszrDgxZK.png)  

`2021.6 ZZH`  
  
