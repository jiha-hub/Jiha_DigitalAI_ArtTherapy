# 💻 MindPalette v4.0: Technical Architecture & Core Code Summary

이 문서는 마인드팔레트 v4.0의 핵심 기술 스택, 단계별 모델 특성, 그리고 4단계 데이터 흐름(IPO)을 최신 기준으로 정리한 자료입니다.

---

## 1. 단계별 AI 모델 및 역할

| 단계 (Phase) | 역할 | 주요 모델 | 선정이유 및 특성 |
| :--- | :--- | :--- | :--- |
| **Edge Detection** | 사용자 스케치 정제 | **PidiNet** | Canny 보다 선의 강도·예술적 질감을 풍부하게 포착. 치료적 '따뜻한 선' 표현에 최적 |
| **Art Generation** | 스케치 기반 이미지 생성 | **SDXL-Base-1.0** + **T2I-Adapter** + **Therapeutic LoRA** | Adapter로 사용자의 원본 레이아웃 90% 이상 유지. LoRA로 고채도 억제 및 치료적 화풍 강제 적용 |
| **Therapeutic Fix** | 부분 수정 및 치유 | **Kandinsky 2.2** (Inpaint) | 텍스트 반응성이 뛰어나 질감·색채 미세 변화 유도에 최적. 화풍 상속 로직과 연동 |
| **Social Gallery** | 기록 및 사회적 연결 | **JSON 기반 소셜 시스템** | `gallery_log.json`으로 영속 저장, 댓글·좋아요·SNS 초대장 기능 포함 |

---

## 2. 데이터 워크플로우 (4단계 IPO)

### [Phase 1] Expression / 감정 표현
- **Input**: 사용자 캔버스 스케치 (RGB) + 스타일 프롬프트 + 선택된 Therapeutic LoRA + 심박수 데이터
- **Process**:
    1. `PidiNet`으로 스케치 Edge 추출
    2. `T2I-Adapter`에 Edge 입력 → 구도 제안
    3. 선택된 LoRA 가중치 `load_lora_weights()` + `fuse_lora(scale=0.8)` 적용
    4. SDXL 파이프라인에서 프롬프트 + Edge 결합, Diffusion 수행
- **Output**: 고품질 예술 치유 이미지 (1024×1024)

### [Phase 2] Refinement / 내면 다듬기
- **Input**: Phase 1 결과 이미지 + 사용자 브러시 마스크 (흰색 영역) + 치유 테마 + 화풍 상속 context
- **Process**:
    1. `refine_source_image`에서 원본 이미지 수신
    2. `inpainting_input` (ImageEditor 레이어)의 알파채널 → 흑백 마스크 추출
    3. Kandinsky 2.2 `inpaint` 파이프라인에서 마스크 영역 재생성
    4. 치료적 색채 편향 제어 (`muted tones, pastel palette, low saturation`) 적용
- **Output**: 상징적 의미가 부여된 최종 마스터피스

### [Phase 3] Consolidation / 갤러리 기록
- **Input**: 최종 작품 + 작품 이름 + 그림 일기 + 심박수 + 액자 선택
- **Process**: `apply_frame()` → `save_to_gallery()` → `gallery_log.json` 저장
- **Output**: 고전 액자 합성 이미지 + 소셜 갤러리 등록

### [Phase 4] Social / 공유 및 연결
- **Input**: 갤러리 데이터
- **Process**: 작품 클릭 → 상세 뷰 (작품명/일기/심박수/댓글) 표시, SNS 초대장 공유
- **Output**: 사회적 지지 경험 및 커뮤니티 연대

---

## 3. Therapeutic LoRA 시스템 (v4.0 신규)

```python
# model_engine.py — SDXL 1.0 호환 치료적 화풍 매핑
THERAPEUTIC_LORAS = {
    "Soft Watercolor": "ostris/watercolor_style_lora_sdxl",
    "Warm Oil Pastel": "artificialguybr/pastel-painting-sdxl",
    "Muted Tones":     "sayakasasaki/muted-color-sdxl",
    "Dreamy Sketch":   "artificialguybr/LineArt-SDXL",
    "Ink Wash Painting": "alvdansen/midsommar-cartoon"
}

def apply_lora(self, style_name, weight=0.8):
    lora_id = self.THERAPEUTIC_LORAS[style_name]
    self.pipeline.load_lora_weights(lora_id)
    self.pipeline.fuse_lora(lora_scale=weight)
    self.active_lora = style_name
```

---

## 4. 핵심 소스코드 (Core Components)

### 4.1 모델 파이프라인 구성 (`model_engine.py`)
```python
# SDXL + Adapter + Therapeutic LoRA 파이프라인
self.adapter = T2IAdapter.from_pretrained("TencentARC/t2i-adapter-sketch-sdxl-1.0", ...)
self.pipeline = StableDiffusionXLAdapterPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", adapter=self.adapter, ...
)
```

### 4.2 마스크 추출 및 인페인팅 (`app.py`)
```python
def safe_modify_adapter(input_dict, source_image, ...):
    # Gradio 4.x ImageEditor: 알파채널이 마스크
    layer_img = input_dict["layers"][0]
    _, _, _, a = layer_img.split()
    mask = a.convert("L")          # 흰색 브러시 영역 = 수정 대상
    return modify_art(source_image, mask, ...)
```

### 4.3 화풍 상속 인페인팅 (`app.py`)
```python
def handle_mod_with_style(source_img, input_dict, prompt, ..., style_context):
    refined_prompt = f"muted tones, pastel palette, {prompt}, {style_context}"
    return safe_modify_adapter(input_dict, source_img, refined_prompt, ...)
```

### 4.4 소셜 갤러리 저장 (`utils.py`)
```python
# gallery_log.json 기반 영속적 소셜 데이터 스토리지
save_to_gallery(image, title, diary, heart_rate)   # 저장
load_gallery_data()                                 # 불러오기
add_comment(idx, comment)                          # 댓글 추가
```

---

## 5. 개발 환경

| 항목 | 사양 |
| :--- | :--- |
| **OS** | Windows 11 |
| **Python** | 3.10 (Conda `art_therapy` 환경) |
| **CUDA** | 11.8+ (RTX 계열 GPU 권장) |
| **핵심 라이브러리** | `torch`, `diffusers`, `transformers`, `peft`, `gradio 4.x`, `controlnet-aux`, `Pillow` |
| **저장 경로** | `outputs/gallery/` (로컬 암호화 저장) |

---
**MindPalette v4.0 기술 리포트** | Antigravity AI Engineer | 2026-02-20
