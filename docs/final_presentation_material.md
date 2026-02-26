# 🎨 MindPalette Final Presentation Material (v4.0)

이 문서는 마인드팔레트(MindPalette) 프로젝트의 논문 기반 배경부터 솔루션 설계, 기술 구현까지 집대성한 발표용 상세 자료입니다.

---

## I. 전체 구성도 (System Overview)

| 구분 | 단계 (Phase) | 활성 기술 / 모델 | 핵심 데이터 및 산출물 |
| :--- | :--- | :--- | :--- |
| **I. 표현 (Expression)** | 발산적 드로잉 | PidiNet + SDXL Adapter + **Therapeutic LoRA** | 사용자 스케치, 심박수(HR), 1차 치유 이미지 |
| **II. 분석 (Analysis)** | 정서 분석 및 가이드 | Bio-feedback Agent (Nurse + Data) | 감정 상태 리포트, 10대 치유 테마 덱 |
| **III. 다듬기 (Refinement)** | 상징물 추가 및 수정 | Kandinsky 2.2 Inpainting (Low Saturation) | 화풍이 유지된 수정 이미지, 자기 효능감 확보 |
| **IV. 공유 (Consolidation)** | 기록 및 소셜 소통 | Social Gallery System + SNS Sharing | 그림 일기, 전시 카드, 지지적 댓글 |

---

## II. 논문 기반 (Academic Foundations)

### 1. 배경 (Background)
*   **문제제기 / 필요성**: 
    *   **Emotional Inexpressibility**: 현대인의 정신건강 위기 속에서 고통을 언어로 표현하지 못하는 '정서적 실어증' 현상 심화.
    *   **Access Barrier**: 전통적 미술 치료는 시간/비용적 허들과 전문가 의존도가 높아 일상적 접근이 어려움.
    *   **AI의 역할**: 언어화되지 않은 고통을 '시각적 상징'으로 외부화(Externalization)하여 객관적으로 마주하게 함.

### 2. 방법 (Methodology)
*   **적용 기술**: 사용자의 원본 구도를 90% 이상 유지하는 **T2I-Adapter** 기술과 심리적 안정을 위한 **LoRA(Low-Rank Adaptation)** 가중치 기법.
*   **연구 목적 / 설정**: 
    *   사용자의 '자기 정체성(Sense of Ownership)'을 해치지 않는 이미지 생성 강도 도출.
    *   디지털 색채의 피로도를 낮추고 치료적 질감(수채화, 파스텔 등)을 구현하는 방법론 확립.
*   **연구방법**: 
    *   스케치 준수율(Conditioning Scale) 0.8~1.0 구간에서의 사용자 주관적 만족도 및 치유 효능감 분석.
    *   Kandinsky 2.2 기반 인페인팅의 맥락 유지 기능 활용.
*   **논문 기반 설계 (Architecture)**: 
    *   **Conditioning Engine**: PidiNet을 통한 예술적 엣지 추출 공정.
    *   **Artistic Transformer**: 텍스트 프롬프트와 스케치 조건을 병렬 처리하는 디퓨전 파이프라인.

### 3. 결과 (Results)
*   **결과 해석**: 
    *   사용자는 자신의 스케치가 보존되었을 때 작품에 대한 애착과 효능감을 강하게 느낌.
    *   치료적 LoRA(예: Soft Watercolor)가 적용된 정제된 색감이 고채도 이미지 대비 심리적 이완 효과(심박수 안정화)를 보임.

---

## III. 솔루션 기반 (Solution Overview)

### 1. 솔루션 개요
*   **솔루션 컨셉**: **"당신의 낙서가 위로의 마스터피스가 됩니다."** 
    *   단순한 이미지 생성을 넘어 사용자의 생체 신호와 서사를 결합한 개인 맞춤형 아트 테라피.
*   **주요 기능**: 
    *   **3-Step Pipeline**: 발산(Expression) -> 조율(Refinement) -> 공유(Gallery).
    *   **Therapeutic Style Selector**: 심리 상태에 따른 5대 전문 화풍(LoRA) 지원.
    *   **Social Connectivity**: 치유의 과정을 초대장 형태로 공유하고 댓글로 지지받는 전시 시스템.

### 2. 솔루션 설계 및 모듈 설명
*   **솔루션 아키텍처 (논문 + 솔루션)**: 
    *   **Front-end**: Gradio 기반의 직관적 3단 레이아웃.
    *   **Model Core**: SDXL(Base) + T2I-Adapter(Sketch) + Kandinsky(Inpaint) + PEFT(LoRA 로딩).
    *   **Data Layer**: 로컬 파일 시스템 기반의 `gallery_log.json` 및 메타데이터 관리.
*   **주요 기능 및 흐름 설명**: 
    1.  사용자가 캔버스에 스케치를 그리고 심박수를 입력.
    2.  `ArtTherapyModel`이 선택된 치료 화풍과 엣지를 결합하여 1차 이미지 생성.
    3.  생성된 이미지 하단의 '내면 다듬기'로 즉시 이동하여 부분 수정(Inpainting) 수행.
    4.  최종 결과물에 제목을 붙여 갤러리에 저장하고 SNS로 초대장 발송.

### 3. 솔루션 시연 (Demo Context)
*   **솔루션 화면 레이아웃**: 
    *   **Sidebar**: 단계별 내비게이션 (표현하기 / 다듬기 / 전시관).
    *   **Interactive Area**: 스케치 에디터와 생성 결과물의 병렬 배치.
    *   **Social Area**: 갤러리 아이템 클릭 시 나타나는 플로팅 감상창 및 댓글창.

### 4. 코드 리뷰 (Technical Review)
*   **개발 환경**: Python 3.10 (Conda environment: `art_therapy`), CUDA 11.8+ 호환 PyTorch.
*   **데이터 출처 및 관리**: 
    *   **Input Data**: 사용자 실시간 스케치 및 텍스트 일기.
    *   **Style Data**: Hugging Face 로드 LoRA 모델 (ostris/watercolor-style-sdxl 등).
    *   **Privacy**: 로컬 `outputs/gallery` 폴더 기반 관리로 데이터 주권 확보.
*   **핵심 기술**: 
    *   `apply_lora()`: PEFT를 이용한 실시간 모델 가중치 융합 기술.
    *   `handle_mod_with_style()`: 1단계의 화풍 컨텍스트를 2단계 인페인팅 엔진에 상속하는 프롬프트 엔지니어링 기술.
    *   **Neutralization Logic**: 고채도 방지 부정 프롬프트 자동 삽입 및 뮤트 톤 강제 적용.

---
**MindPalette Project Team** | *예술과 AI로 여는 새로운 치유의 창*
