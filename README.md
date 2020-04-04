# Rekognition Architecture :relaxed

# What is Rekognition ? 
- 딥러닝 기반의 수백만 이미지 인식/분석 서비스
- 얼굴 비교, 얼굴 분석, 객체 및 장면 인식 등 많은 기술을 사용할 수 있다.
- 최대 15MB, 이미지 바이트 배열로 전달 시 최대 5MB의 이미지 파일 크기 지원
- 최소한 45픽셀 이어야 분석이 가능

# Expected cost
- AWS 프리 티어를 사용하는 고객은 Amazon Rekognition Image를 무료로 시작할 수 있습니다.  프리 티어는 12개월 동안 유지되며, 이 기간에는 매월 5,000개의 이미지를 분석하고 매월 얼굴 메타데이터 1,000개를 저장할 수 있습니다.
- 월별 처리된 처음 1백만 개의 이미지*	이미지당 0.0012 USD	1.20 USD
  월별 처리된 다음 9백만 개의 이미지*	이미지당 0.00096 USD	0.96 USD
  월별 처리된 다음 9천만 개의 이미지*	이미지당 0.00072 USD	0.72 USD
  월별 1억 개를 초과하여 처리된 이미지*	이미지당 0.00048 USD	0.48 USD

# Rekognition Architecture on AWS

![](./image/aws.PNG)
