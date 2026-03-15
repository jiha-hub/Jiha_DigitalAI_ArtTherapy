---
title: MindPalette
emoji: 🏛️
colorFrom: indigo
colorTo: indigo
sdk: gradio
sdk_version: 4.41.0
app_file: src/app.py
pinned: false
license: gpl-3.0
short_description: AI-based Non-verbal Emotional Externalization Platform
---

# 🏛️ MindPalette (마인드팔레트)

📗 **[프로젝트 인수인계서 바로가기 (Handover Document)](./인수인계서.md)**

**"내면의 언어를 시각화하여 정서적 안정과 통찰을 돕는 AI 심리 분석 및 정서 발산 플랫폼"**

🔗 **GitHub Repository:** [https://github.com/jiha-hub/Jiha_DigitalAI_ArtTherapy](https://github.com/jiha-hub/Jiha_DigitalAI_ArtTherapy)

---

## 1. 🎯 프로젝트 주제 (Topic)
**AI 기반 비언어적 정서 외부화 플랫폼 (AI-based Non-verbal Emotional Externalization Platform)**  
사용자의 감정을 정형화된 언어가 아닌 자유로운 드로잉과 색상, 질감으로 표현하도록 유도하며, 생성형 AI(Generative AI)를 통해 이를 예술 작품으로 변환하는 디지털 미술 치료 솔루션입니다.

## 2. 💡 프로젝트 목적 (Purpose)
현대인들은 복잡한 감정과 스트레스를 명확한 언어로 표현하는 데 어려움을 겪습니다. **MindPalette**는 사용자가 거칠게 그린 스케치와 감정 키워드를 바탕으로 AI가 한 폭의 예술 작품으로 탄생시켜주는 **비언어적 정서 표현 도구**입니다.

이 과정에서 구체적인 인물(자화상) 묘사를 배제하고 질감과 색채 스펙트럼에 집중하게 하여, 사용자 스스로 자신의 감정을 한 발짝 떨어져 관조(Objectification)할 수 있도록 돕습니다. 이를 통해 억눌린 감정의 정화(Catharsis)와 심리적 안정감을 제공하는 것이 주된 목적입니다.

## 3. 👥 주요 대상 (Target Audience)
* **심리적 위안이 필요한 일반인:** 복잡한 감정을 글이나 말로 명확하게 표현하기 힘든 분.
* **미술 치료사 및 심리 상담사:** 내담자의 억압된 무의식적 감정을 시각화하고, 이를 바탕으로 심도 있는 대화를 끌어내는 보조 도구로 활용하고자 하는 전문가.
* **예술적 영감이 필요한 크리에이터:** 간단한 스케치나 감정 키워드만으로 고품질의 추상적, 무드 중심 아트워크를 만들고 싶은 분.

## 4. 🛠️ 기술 스택 (Tech Stack)
* **Language:** Python 3.10+
* **Framework & UI:** Gradio 4.0+
* **AI & Deep Learning:** PyTorch, Hugging Face `diffusers`, `transformers`
* **Core Models (Image Generation/Modification):**
  * **SDXL Base 1.0 + T2I-Adapter (Sketch):** 사용자의 흑백 스케치 선을 기반으로 이미지 생성의 조건(Conditioning)을 부여하여 고해상도 이미지를 생성합니다.
  * **Kandinsky 2.2 Inpainting:** 생성된 이미지 중 특정 영역(마스킹된 영역)만을 국소적으로 수정 및 다듬어 감정 표현을 세밀하게 조정합니다.
  * **Therapeutic LoRA Styles:** 감정 표현을 보조하는 맞춤형 화풍(수채화, 오일 파스텔, 먹물화 등) 가중치를 동적으로 적용합니다.
* **Edge Detection:** PidiNet (`controlnet_aux`를 통한 사용자 스케치에서의 윤곽선 추출)
* **Platform & Deployment:** Hugging Face Spaces (GPU 환경 최적화)

## 5. 📂 코드 구조 (Code Structure)
배포 및 실행에 필요한 핵심 디렉토리 및 파일 구조입니다. Hugging Face Spaces 연동 및 실행 시 아래 파일들이 모두 사용됩니다.

```text
📦 Jiha_DigitalAI_ArtTherapy (GitHub Repository)
 ┣ 📂 src
 ┃  ┣ 📜 app.py               # Gradio UI(갤러리, 캔버스 등) 구성 및 프론트/백엔드 브릿지 파이프라인
 ┃  ┣ 📜 model_engine.py      # AI 모델 로드, 이미지 생성(SDXL) 및 인페인팅(Kandinsky) 핵심 로직
 ┃  ┗ 📜 utils.py             # 이미지 저장(Gallery Log 관리) 및 기타 시스템 유틸리티 함수
 ┣ 📜 requirements.txt        # 의존성 패키지 (Hugging Face / Local 환경 구성용 필수 라이브러리 목록)
 ┗ 📜 README.md               # 프로젝트 소개 및 배포 가이드 (현재 파일)
```

## 6. 💻 핵심 코드 설명 (Core Code)

### (1) 스케치 기반 이미지 생성 (T2I-Adapter + SDXL) - `model_engine.py`
사용자가 그린 스케치를 PidiNet으로 깊이 있게 분석하여 윤곽선(Edge Map)을 추출한 뒤, T2I-Adapter를 통해 SDXL 생성 모델의 조건(Conditioning)으로 입력합니다. 사용자가 선택한 치유적 화풍(LoRA) 가중치를 동적으로 로드 및 융합(Fusing)하여 최종 결과물을 생성합니다.

```python
def generate_image(self, sketch_image, prompt, negative_prompt="", num_steps=30, guidance_scale=7.5, adapter_scale=0.9, seed=42, style_name="기본 (Standard)"):
    # 1. PidiNet으로 엣지(Edge) 맵 추출
    edge_map = self.pidinet(
        sketch_image, detect_resolution=1024, image_resolution=1024, apply_filter=True
    )

    # 2. SDXL 파이프라인으로 생성 (Adapter 적용)
    image = self.pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=edge_map,
        num_inference_steps=num_steps,
        adapter_conditioning_scale=adapter_scale,
        guidance_scale=guidance_scale,
        generator=torch.Generator(device=self.device).manual_seed(seed)
    ).images[0]

    return image, edge_map
```

### (2) 특정 감정 영역 부분 수정 (Inpainting) - `model_engine.py`
생성된 작품에서 사용자가 원하지 않는 요소나 특정 감정을 비워내기 위해, 사용자가 브러시로 직접 칠한 마스킹 영역만 Kandinsky 2.2 Inpainting 모델을 통해 자연스럽게 재생성합니다.

```python
def inpaint_image(self, image, mask_image, prompt, negative_prompt="", strength=0.75, guidance_scale=7.5, seed=42):
    # Kandinsky Inpainting 파이프라인 실행
    output = self.inpainting_pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=image,            # 원본 보존 이미지
        mask_image=mask_image,  # 수정할 영역 마스크
        strength=strength,      # 원본 유지 강도
        guidance_scale=guidance_scale,
        generator=torch.Generator(device=self.device).manual_seed(seed)
    ).images[0]

    return output
```

### (3) 프롬프트 엔지니어링 및 매개변수 조합 - `app.py`
사용자가 콤보박스에서 직관적으로 선택한 매체(유화, 수채화), 주요 소재(비구상), 감정 무드(차분한, 우울한) 및 조명을 조합하여, AI가 가장 잘 이해할 수 있는 최적화된 영문 프롬프트로 변환 처리합니다.

```python
def build_prompt(media, subject, mood, style, custom_prompt):
    base = []
    if media: base.append(PROMPT_OPTIONS["매체"].get(media, ""))
    if subject: base.append(PROMPT_OPTIONS["주요_소재"].get(subject, ""))
    if mood: base.append(PROMPT_OPTIONS["감정_무드"].get(mood, ""))
    if style: base.append(PROMPT_OPTIONS["스타일"].get(style, ""))
    
    prompt_str = ", ".join([b for b in base if b])
    if custom_prompt:
        prompt_str += f", {custom_prompt}"
        
    prompt_str += ", high quality, masterpiece, expressive art therapy"
    return prompt_str
```

---

## 🚀 배포 및 실행 가이드 (Hugging Face Spaces 연동)

이 저장소를 **Hugging Face Spaces (Gradio)** 에 연동하여 호스팅하려면, 허깅페이스 환경 구축에 필요한 모든 파일이 준비되어 있어야 합니다. 이 Repository에는 배포에 필요한 모든 설정 파일이 포함되어 있습니다.

**Hugging Face Spaces 배포 필수 파일:**
1. `src/app.py` (Gradio 메인 애플리케이션 진입점. `README.md` 상단 메타데이터의 `app_file` 옵션으로 경로가 지정됨)
2. `src/model_engine.py` (AI 모델 추론 로직)
3. `src/utils.py` (유틸리티 함수)
4. `requirements.txt` (`diffusers`, `transformers`, `gradio` 등 Hugging Face 인스턴스에서 자동으로 `pip install` 되는 필수 패키지 명세서)
5. `README.md` (Hugging Face Spaces가 읽어들이는 환경설정 메타데이터 헤더 포함 파일)

> **[ 배포 방법 ]**  
> Hugging Face에서 새 `Gradio` Space를 생성하고, 해당 Space를 이 GitHub Repository(`https://github.com/jiha-hub/Jiha_DigitalAI_ArtTherapy`)와 연동(Connect)만 하면 빌드가 자동으로 시작됩니다.

**로컬 환경에서 개발 및 테스트 시:**
```bash
# 1. 가상환경 생성 및 활성화 (선택 사항)
python -m venv .venv
source .venv/bin/activate  # Windows 커맨드: .venv\Scripts\activate

# 2. 필수 라이브러리 설치
pip install -r requirements.txt

# 3. 로컬 서버 실행
python src/app.py
```
