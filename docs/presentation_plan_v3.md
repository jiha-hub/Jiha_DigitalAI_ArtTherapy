# 🎤 MindPalette v3.0: 15-Minute Pitch Deck Content

이 문서는 발표 15분에 최적화된 핵심 내용을 담고 있습니다.

## 1. 아이디어명 (Idea Name)
**마인드팔레트 (MindPalette)**: AI 기반 비언어적 감정 외부화 및 예술 치료 플랫폼

---

## 2. 아이디어 제안배경 (Background)
현대인의 정신건강 위기는 심화되고 있으나, 전통적 심리 상담은 **"언어적 장벽"**과 **"비용/시간적 허들"**로 인해 접근성이 낮습니다. 특히 자신의 감정을 말로 표현하기 힘든 아동, 청소년, 그리고 감정적 소모가 큰 직장인들에게는 새로운 방식의 감정 배출구가 필요합니다.

### 2.1 문제점 및 해결방안 (Problems & Solutions)
- **문제점**: 
    - 텍스트/대화 중심 상담의 한계 (언어화되지 않은 고통 표현 불가).
    - 미술 치료의 높은 문턱 (전문가 동행 필수, 재료 준비 등).
- **해결방안**: 
    - 생성형 AI(SDXL Adapter)를 활용해 사용자의 단순한 스케치를 고차원 예술 작품으로 변환.
    - **치료적 인페인팅**을 통해 부정적 요소를 제거하고 긍정적 상징물을 추가하며 자기 효능감 체득.

---

## 3. 아이디어 (The Idea)
### 3.1 아이디어 컨셉 (Concept)
"당신의 낙서가 치유의 예술이 됩니다." 사용자의 선(Edge)을 90% 이상 보존하여 **'내가 그린 그림'**이라는 소유감을 유지하면서 AI가 이를 풍부하게 시각화해주는 디지털 캔버스.

### 3.2 개발방법 (Development)
#### 3.2.1 아키텍처 (Architecture)
- **Front-end**: Gradio (Web-based Interface).
- **Back-end**: Python, PyTorch.
- **AI Stack**: SDXL Base + T2I-Adapter (Sketch) + Kandinsky 2.2 Inpaint.
- **Bio-Arts System**: 실시간 심박수(HR) 동기화를 통한 정서 상태 분석 및 시각화.
- **Flow**: [입력: 스케치 + 생체 데이터] -> [프로세스: 전문 분석 에이전트 & AI] -> [출력: 예술 작품 + 치유 리포트].

#### 3.2.2 EDA (Exploratory Data Analysis)
- 논문 SDS24의 데이터셋 분석: 스케치 준수율(Conditioning Scale)과 치료적 효과의 상관관계 분석 결과, 강도 0.8~1.0 사이에서 가장 높은 사용자 만족도 도출.

#### 3.2.3 모델 설계 및 개발 (Model Design)
- **Bio-Feedback Logic**: 실시간 심박 변이도(HRV)와 드로잉 속도를 연동한 정서 조절 알고리즘.
- **Narrative Analysis**: 짧은 일기(텍스트) 속 감정 키워드 추출 및 위험 단어 자동 필터링.
- **Custom VAE Fix**: 이미지 품질 개선을 위한 fp16-fix VAE 적용.

#### 3.2.4 성능개선 (Performance)
- 추론 속도 개선: 512x512 기준 30초 이내 생성 (CPU Offloading 적용).
- 스케치 정확도: PidiNet Annotator를 활용하여 사용자가 그린 엣지를 정교하게 추출.

### 3.3 핵심기술 (Key Technologies)
- **Sketch Integration**: 사용자의 선을 그대로 보존하는 T2I-Adapter.
- **Therapeutic Inpainting**: 마스킹 영역에 긍정적 객체를 삽입하는 10대 테마 제안 엔진.
- **Bio-Arts Analysis Agent**: 간호사와 데이터 전문가의 지식을 결합한 감정-생체 지표 통합 분석 에이전트.

---

## 4. 아이디어 차별성 및 사업성 (Business Value)
### 4.1.1 차별성 (Differentiation)
- **타사(미드저니 등)**: 사용자의 의도보다 '예쁜 그림'에 집중. 스케치 무시 경향.
- **마인드팔레트**: **사용자의 선을 존중** (Self-Integrity), 치료적 맥락 제공.

### 4.1.2 우수성 (Excellence)
- 학술 논문(SDS24)의 검증된 방법론을 기반으로 한 기술적 구현.

### 4.1.3 독창성 (Originality)
- '이미지 핵심 주제 세분화 10선'을 통한 행동 유도형 가이드 제공.

### 4.2 사업성 (Business)
#### 4.2.1 BMC모델 (Business Model Canvas)
- **수익원**: 개인 구독료(v2.0), 전문가 매칭 수수료, B2B 기업 복지 패키지.

#### 4.2.2 시장성 (Market)
- 디지털 치료제(DTx) 시장의 급격한 팽창, 비대면 멘탈케어 수요 증가.

#### 4.2.3 상용화 (Commercialization)
- 클라우드 GPU 배포 환경(Modal/RunPod)을 통한 전 세계 서비스 확장성 확보.

---

## 5. 기대효과 (Impact)
### 5.1 고용창출 (Jobs)
- 온라인 전문 상담사 모집 및 관리를 통한 전문직 일자리 창출.
- 예술 치료 기반 AI 레이블링/검수 인력 수요 발생.

### 5.2 사회적 가치창출 (Social Value)
- 자살 예방 및 고위험군 조기 발견 (Safety Filter).
- 언어 소외 계층(아동, 노인 등)의 정서적 소통 창구 제공.

---
**마인드팔레트 전략기획팀**
