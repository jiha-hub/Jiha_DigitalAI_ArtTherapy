# 🧪 Prompt Engineering Guide for Higher Quality Art

AI 생성 이미지의 품질을 높이고, 불필요한 요소(이상한 아저씨 등)를 제거하기 위한 프롬프트 가이드입니다.

## 1. 전역 부정 프롬프트 (Global Negative Prompts)
이미지 생성 시 **Negative Prompt** 칸에 아래 내용을 복사해서 넣으면 품질이 비약적으로 상승합니다.

### [추천 세트]
> `man, male, beard, mustache, facial hair, old person, distorted face, blurry, low resolution, bad anatomy, worst quality, monochrome, watermark, text, signature, low quality, normal quality, jpeg artifacts, duplicate, cropped, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, long neck, bad proportions, gross proportions, malformed limbs, missing arms, missing legs, fused fingers, too many fingers.`

---

## 2. 상황별 긍정 프롬프트 (Positive Prompts)

### 🌿 치유와 평온 (Healing & Serene)
> `Serene and peaceful landscape, soft morning sunlight, calming pastel colors, dreamy atmosphere, oil painting style, thick brushstrokes, masterpiece, high quality, 8k.`

### 💥 혼돈과 감정 표출 (Chaos & Expression)
> `Powerful abstract expressionism, vibrant splashing colors, high contrast, dynamic energy, flowing textures, emotional depth, sharp and soft strokes, artistic chaos.`

### 👤 자아 발견 (Self-Discovery)
> `Stylized portrait of a serene woman, glowing aura, inner light, blooming flowers around the figure, ethereal, fantasy art, intricate details, cinematic lighting.`

---

## 3. 고급 파라미터 팁 (Advanced Settings)

- **Adapter Strength (중요!)**: 
    - **0.5 ~ 0.7**: AI가 더 자유롭게 예술적으로 그립니다.
    - **0.8 ~ 1.0**: 사용자의 스케치 선을 최대한 그대로 지켜서 그립니다.
- **Guidance Scale**:
    - **7 ~ 9**: 가장 안정적인 결과가 나옵니다.
    - **10 이상**: 프롬프트를 아주 강하게 반영하며, 색감이 진해집니다.
- **Seed**: 
    - 같은 스케치와 프롬프트라도 Seed 숫자 하나만 바꾸면 완전히 새로운 그림이 나옵니다. 마음에 들 때까지 Seed를 바꿔보세요.
