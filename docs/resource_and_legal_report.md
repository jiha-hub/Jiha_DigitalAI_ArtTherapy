# 📄 Resource & Legal Compliance Report (리소스 및 법적 고지 보고서)

## 1. 법적 고지 및 라이선스 (Legal & License)
- **원본 저작권**: 본 소프트웨어는 SDS24(Integrating Generative AI into Art Therapy) 연구 논문 및 제공된 코드를 기반으로 제작되었습니다.
- **라이선스 적용**: 원본 코드의 라이선스인 **GNU GPL v3**를 그대로 계승합니다.
- **주요 가공 및 구현 내역**:
    - **구조 혁신**: Jupyter Notebook의 단선적 스크립트를 상용 수준의 Python Package(Class-based)로 변환하였습니다.
    - **UI/UX 독자 개발**: Gradio를 활용한 인터랙티브 웹 인터페이스 및 '마인드팔레트' 전용 브랜드 아이덴티티를 구축하였습니다.
    - **최적화**: 로컬 GPU 환경(Windows)에서의 메모리 효율성 극대화를 위해 모델 CPU Offloading 및 런타임 클린업 로직을 독립적으로 설계하여 추가하였습니다.
- **보증의 부인**: GPL v3 섹션 15 및 16에 따라 본 소프트웨어는 어떠한 형태의 보증도 제공하지 않으며 사용으로 인한 결과는 사용자에게 있습니다.

## 2. 경제적 지출 및 API 보고 (Financial Report)
현재까지의 **순수 지출 금액은 0원($0)**입니다.
- **모델 소싱**: 모든 AI 모델(Stable Diffusion XL, Kandinsky 2.2)은 Hugging Face의 오픈소스를 활용하여 별도의 API 요금(OpenAI 등)이 발생하지 않습니다.
- **인프라 비용**: 현재 사용자님의 로컬 GPU 자원을 활용하므로 클라우드 서버 비용이 발생하지 않았습니다.
- **라이선스료**: 오픈소스 라이선스 정책에 따라 상업적 활용을 포함하여 무료로 이용 가능합니다.

## 3. 서버/시스템 용량 분석 (Resource Usage)
- **저장소 점유**:
    - AI 가중치(Weights): 약 22.5 GB (SDXL Base, XL VAE, T2I Adapter, Kandinsky-Inpaint)
    - Python 환경 및 라이브러리: 약 4.2 GB
    - **권장 여유 공간**: 최소 30 GB 이상의 SSD 공간.
- **메모리(RAM/VRAM) 요구사항**:
    - 시스템 RAM: 최소 16GB 이상 권장
    - GPU VRAM: 최소 8GB 이상 (현재 `low_vram` 옵션 적용으로 8GB에서도 구동 가능)

## 4. 다중 사용자 서비스(Deployment) 가이드
현재 로컬 구현본을 외부에서 여러 명이 사용하게 하려면 다음과 같은 시스템 업그레이드가 필요합니다.
1. **공개 서버 배포**: AWS EC2(g4dn 이상) 또는 Google Cloud(Vertex AI)의 GPU 인스턴스에 설치.
2. **도커(Docker)라이징**: 어떤 서버 환경에서도 환경 충돌 없이 실행될 수 있도록 컨테이너화 작업.
3. **인증 시스템**: 다중 사용자 사용 시 개별 작품 보관을 위한 간단한 로그인 기능 추가.
4. **API 서버화**: 현재의 UI 형태를 유지하면서, 모바일 앱 백엔드로 활용하기 위한 FastAPI 기반의 REST API 개발.

---
**마인드팔레트 기술/사업 팀 통합 보고**
