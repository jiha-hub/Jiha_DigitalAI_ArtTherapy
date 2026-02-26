# 📊 논문 vs. MindPalette 구현 비교표

> **출처 논문**: SDS24 Workshop — "Integrating Generative AI into Art Therapy" (BFH)  
> **구현 서비스**: MindPalette v4.0 (Python / Gradio / SDXL + Kandinsky 2.2)

---

## I. 전체 단계별 플로우 비교 (Phase-by-Phase Flow Comparison)

| 구분 | 논문 원본 플로우 | MindPalette 구현 플로우 | 논문 그대로 구현? | 차이점 및 이유 |
| :---: | :--- | :--- | :---: | :--- |
| **Phase 1** | 사용자 스케치 입력 → Edge 추출(Canny) → SDXL 기반 이미지 생성 | 사용자 스케치 입력 → Edge 추출(**PidiNet**) → SDXL + **Therapeutic LoRA** 기반 이미지 생성 | **△ 일부 변경** | **Edge Detector 변경**: 논문의 Canny 대신 PidiNet 사용. 이유: PidiNet이 선의 굵기와 예술적 질감을 더 풍부하게 포착하여 치료적 예술 품질에 유리. **LoRA 추가**: 고채도 색상의 심리적 자극을 낮추기 위해 수채화/파스텔 스타일 LoRA를 추가. 논문에는 없는 치료적 정밀화 기능. |
| **Phase 2** | 생성 이미지에 대한 Art Therapist(치료사)의 분석 및 가이드 제공 | 생성 이미지에 대한 **Bio-feedback + Narrative 분석 에이전트** (Nurse + Data Agent 페르소나) 및 **10대 치유 테마 덱** 제안 | **△ 일부 변경** | **치료사 → AI 에이전트로 대체**: 논문은 실제 치료사가 분석하는 오프라인 모델이나, 본 구현에서는 접근성 확장을 위해 임상 간호사와 데이터 전문가의 지식을 페르소나化한 AI 에이전트로 대체. 또한 실시간 심박수(HR) 데이터를 GUI로 입력받아 정서 상태를 정량화하는 **바이오피드백 루프**를 추가로 도입. |
| **Phase 3** | 사용자가 이미지의 특정 영역 마스킹 → 치유적 내용으로 **Kandinsky 2.2** Inpainting 수행 | 사용자가 이미지의 특정 영역 마스킹 → **10대 테마 프롬프트 자동 적용** → **Kandinsky 2.2** Inpainting (저채도 토큰 강제 적용) | **✅ 거의 동일** | **핵심 모델(Kandinsky 2.2) 동일 사용**. 단, 치료적 안정감을 위해 부정 프롬프트에 `vivid colors, neon, high saturation` 등을 추가하여 원색 편향성을 억제함. 또한 Phase 1의 화풍(style_context)을 Phase 2에 자동 상속시켜 시각적 일관성 확보(논문에 없는 추가 기능). |
| **Phase 4** | 최종 이미지를 치료사 및 환자가 보관/아카이빙 | 최종 이미지를 **개인 갤러리(gallery_log.json)**에 저장 → **고전 액자** 적용 → **SNS 초대장** 공유 및 **댓글 소통** | **＋ 기능 추가** | **논문에 없는 소셜 기능 전면 추가**: 치료적 효과는 '회상(Recall)'과 '사회적 지지(Social Support)'에서도 발생한다는 심리학적 근거를 기반으로 갤러리 전시, SNS 공유, 댓글 시스템을 추가 구현. 개인 아카이빙에서 커뮤니티 치유로 범위를 확장. |

---

## II. 핵심 기술 컴포넌트 비교

| 기술 요소 | 논문 설계 | MindPalette 구현 | 동일 여부 | 변경 이유 |
| :---: | :--- | :--- | :---: | :--- |
| **Edge Detector** | Canny Edge Detector | **PidiNet** (Soft-Edge Annotator) | ❌ 변경 | PidiNet은 Canny보다 자연스럽고 예술적인 엣지 표현에 유리. 치료적 이미지의 '따뜻한 선' 표현에 적합. |
| **Generation Base** | SDXL 1.0 + T2I-Adapter (Sketch) | SDXL 1.0 + T2I-Adapter (Sketch) + **Therapeutic LoRA** | △ LoRA 추가 | 논문의 핵심 구조는 동일하게 구현. LoRA는 고채도 이미지가 심리적 피로를 유발한다는 판단 하에 추가. |
| **Style Conditioning Scale** | 0.9 고정 | 사용자 조절 가능 (기본값 0.9) | △ 유연화 | 동일한 기본값이나, 논문은 고정이고 본 구현은 사용자 조절 가능하도록 UI에 노출. 치료적 자율성(Agency) 강화 목적. |
| **Inpainting Model** | Kandinsky 2.2 | **Kandinsky 2.2** | ✅ 동일 | 텍스트 반응성과 맥락 유지 능력 모두 검증된 모델로 논문과 동일하게 선택. |
| **치료사 역할** | 실제 아트 테라피스트 | AI 에이전트 페르소나 (Nurse + Data) | ❌ 대체 | 논문의 대면 치료사 의존 모델은 접근성 한계 존재. AI 에이전트로 대체하여 24/7 비대면 서비스 제공. |
| **사용자 입력** | 스케치 + 텍스트 프롬프트 | 스케치 + 텍스트 + **심박수(HR)** + **그림 일기** | ＋ 추가 | 바이오피드백(Bio-Feedback)은 논문이 권장한 미래 방향으로, 본 구현에서 선제 도입. |
| **결과 보관** | 치료사와 환자가 로컬 보관 | 로컬 JSON 파일 + **갤러리 UI** + **SNS 공유** | ＋ 추가 | 치유 경험의 사회적 공유를 통해 지지 체계 형성. 논문의 아카이빙을 소셜 플랫폼으로 확장. |

---

## III. 요약: 논문 구현 충실도 및 확장 내역

| 분류 | 내용 |
| :--- | :--- |
| **논문 그대로 구현 (✅)** | Kandinsky 2.2 기반 인페인팅 / SDXL + T2I-Adapter 스케치 조건부 생성 / 스케치-예술 이미지 변환 파이프라인 전반 |
| **논문 일부 수정 (△)** | Edge Detector (Canny → PidiNet) / 치료사 분석 (오프라인 대면 → AI 에이전트 대체) / 스타일 강도 고정값 → 사용자 조절 가능화 |
| **논문 이상으로 확장 (＋)** | Therapeutic LoRA (5대 화풍 스타일 제어) / Bio-feedback(심박수) 연동 / 그림 일기(Narrative Therapy) / 10대 치유 테마 덱 / 소셜 갤러리 + SNS 공유 + 댓글 시스템 / 고전 액자 합성 기능 |

---
**작성**: MindPalette 개발팀 | 비교 기준일: 2026-02-20
