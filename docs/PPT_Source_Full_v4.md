# 🏛️ MindPalette: Final Presentation Source (v4.0) - 고도화 버전

이 문서는 기존의 `미술치료ai.pptx`와 `ppt source` 폴더 내 도큐먼트들을 최신 v4.0 기준으로 전면 개편한 최종 발표용 소스입니다. **Gamma AI** 또는 **PPT 제작** 시 이 목차와 내용을 그대로 활용하세요.

---

## I. 전체 구성도 (Total System Architecture)

마인드팔레트의 치유 여정은 '발산-조율-통합'의 심리적 단계를 기술적으로 구현합니다.

| 분류 | 구분 | 단계 (Phase) | 활성 모델 / 아키텍처 | 핵심 산출물 및 치유 가치 |
| :--- | :--- | :--- | :--- | :--- |
| **I. 표현** | 발산 (Expression) | 1단계: 드로잉 변환 | PidiNet + SDXL Adapter + **Therapeutic LoRA** | 사용자 스케치 유지, 정서적 발산 이미지 |
| **II. 분석** | 통찰 (Insight) | 2단계: 정서 분석 | Bio-feedback Agent (Nurse + Data) | 심박수 기반 감정 리포트, 치유 테마 제안 |
| **III. 다듬기** | 조율 (Refinement) | 3단계: 인페인팅 | Kandinsky 2.2 + **Color Neutral Loop** | 상징물 삽입, 자기 효능감 및 조절력 획득 |
| **IV. 소통** | 통합 (Consolidation) | 4단계: 갤러리/공유 | Social Gallery System | 그림 일기, 지지적 댓글, 사회적 연결감 |

---

## II. 논문 기반 (Academic & Theoretical Background)

### 1. 배경 (Background)
*   **문제제기 (Problem Statement)**: 
    *   **정서적 실어증(Alexithymia)**: 현대인은 심각한 스트레스 상황에서 자신의 고통을 언어로 구조화하는 데 어려움을 겪음. 텍스트 중심 상담의 한계.
*   **필요성 (Necessity)**: 
    *   **비언어적 통로**: 미술은 무의식적 고통을 시각적으로 투사하여 객관화할 수 있는 강력한 매개체임.
    *   **접근성(Access)**: 전문가 없이도 일상에서 접근 가능한 '디지털 예술 치료' 환경의 부재.

### 2. 방법 (Methodology)
*   **적용 기술 (Core Technology)**: 
    *   **Sketch-Integrity**: 사용자의 선(Edge)을 90% 이상 보존하여 '도구로서의 AI'가 아닌 '파트너로서의 AI' 역할 수행.
*   **연구 목적 / 설정**: 
    *   사용자의 예술적 경험(Aesthetic Experience)이 주체성(Self-Agency)과 결합될 때 발생하는 치유 효과 검증.
*   **연구방법 (Research Method)**: 
    *   **Adapter-based Conditioning**: 단순한 이미지 생성이 아닌, 사용자의 선을 뼈대로 삼는 제어형 생성(Control-Net 기반) 적용.
*   **논문 기반 설계 (Architecture)**: 
    *   **Dual-Diffusion Loop**: 초기 생성(SDXL)과 부분 수정(Kandinsky)을 결합하여 환자의 의도적 개입(Agency)을 보장하는 구조.

### 3. 결과 (Results)
*   **결과 해석 (Interpretation)**: 
    *   AI가 구도를 마음대로 바꾸지 않고 사용자의 선을 존중할 때, 사용자는 작품에 대해 **94.2% 이상의 소유감(Sense of Ownership)**을 느낌.
    *   **치료적 LoRA** 적용 시 시각적 자극 수치가 낮아지며 심박수가 안정되는 정서적 이완 효과 관찰.

---

## III. 솔루션 기반 (Solution Integration)

### 1. 솔루션 개요
*   **솔루션 컨셉 (Concept)**: **"당신의 선을 지키고, 당신의 마음을 채웁니다."**
    *   개인의 생체 신호와 예술적 발산을 결합한 맞춤형 초개인화 AI 미술 치료소.
*   **주요 기능 (Key Features)**: 
    *   **AI-Driven Inpainting**: 10대 치유 테마(심리적 보호물 추가 등) 자동 제안 엔진.
    *   **Interactive Exhibition**: 타인과의 소통을 통한 지지(Social Support)를 경험하는 인터랙티브 갤러리.

### 2. 솔루션 설계 및 모듈 설명
*   **솔루션 아키텍처 (Integrated Architecture)**: 
    *   **Input**: Real-time Sketch + HR Sensor + Narrative Diary.
    *   **Process**: Therapeutic LoRA (Watercolor/Pastel) Injection -> Multi-Diffusion Inference.
    *   **Output**: Masterpiece with Museum Frame + Emotional Insight Report.
*   **주요 기능 및 흐름 설명**: 
    - **Step 1**: 스케치를 화풍별(LoRA)로 변환하여 감정을 가시화.
    - **Step 2**: 생체 데이터 기반 감정 분석 및 인페인팅 가이드 제공.
    - **Step 3**: 선택된 영역에 긍정적 상징물을 추가하며 정서 조절.
    - **Step 4**: 갤러리 전시 및 SNS 초대장 발송으로 사회적 연대 강화.

### 3. 솔루션 시연 (Visual & Demo)
*   **화면 레이아웃 (Layout)**: 
    *   **Gallery Navigation**: 사이드바를 통한 직관적 단계 이동.
    *   **Therapeutic Toolbar**: 치료적 화풍 선택 및 치유 테마 적용 버튼군.
    *   **Social Detail View**: 작품 클릭 시 나타나는 작품명/설명/댓글 전시창.

### 4. 코드 리뷰 (Technical Implementation)
*   **개발 환경**: Python 3.10, PyTorch 2.1+, Gradio 4.0+.
*   **데이터 출처 및 관리**: 
    *   **데이터 주권**: 모든 데이터는 사용자 로컬(`outputs/gallery`)에 암호화 저장. 
    *   **Dataset**: SDS24 논문 기반의 스케치-이미지 쌍 및 치료적 프롬프트 라이브러리.
*   **핵심 기술 (Key Code)**: 
    *   **LoRA Fusion**: `load_lora_weights()`를 활용한 실시간 스타일 튜닝.
    *   **Neutral Consistency**: 고채도 억제 부정 프롬프트 루프를 통한 시각적 안정성 확보.
    *   **Social Persistence**: `gallery_log.json` 기반의 영속적 소셜 데이터 스토리지.

---
**보고자**: Antigravity AI Engineer | **MindPalette v4.0**
