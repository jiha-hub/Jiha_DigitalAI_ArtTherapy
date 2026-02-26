
import gradio as gr
import torch
from model_engine import ArtTherapyModel
from utils import save_generated_image
import os

# Initialize Model
# Check for CUDA availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[{'GPU' if device=='cuda' else 'CPU'}] Mode: Art Therapy AI Loading...")

# Default to low_vram=True for safety on local environments
# Force low_vram on Hugging Face Spaces for stability
is_hf = os.environ.get("SPACE_ID") is not None
model = ArtTherapyModel(device=device, low_vram=True if is_hf else True) 

def preprocess_editor_input(input_data):
    """Extracts the resulting image from Gradio ImageEditor."""
    if input_data is None:
        return None
    
    # Gradio 4.0+ ImageEditor returns a dict
    if isinstance(input_data, dict):
        return input_data.get("composite") or input_data.get("background")
    
    return input_data

def generate_art(sketch_dict, prompt, negative_prompt, guidance_scale, adapter_scale, seed, style_name="기본 (Standard)"):
    # Extract sketch from editor dictionary
    sketch = preprocess_editor_input(sketch_dict)
    
    if sketch is None:
        raise gr.Error("캔버스에 스케치를 먼저 그려주세요!")
    
    try:
        gr.Info("Generating image... This may take a moment.")
        image, _ = model.generate_image(
            sketch_image=sketch,
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            adapter_scale=adapter_scale,
            seed=int(seed),
            style_name=style_name
        )
        
        # Save automatically
        save_path = save_generated_image(image, prompt, prefix="sketch2img")
        gr.Info(f"Image saved to {save_path}")
        
        return image
    except Exception as e:
        raise gr.Error(f"Generation failed: {str(e)}")

def modify_art(image, mask, prompt, negative_prompt, strength, guidance_scale, seed):
    if image is None or mask is None:
        raise gr.Error("이미지와 마스킹 영역이 필요합니다.")
    
    try:
        gr.Info("이미지 다듬기 중... 잠시만 기다려 주세요.")
        
        modified_image = model.inpaint_image(
            image=image,
            mask_image=mask,
            prompt=prompt,
            negative_prompt=negative_prompt,
            strength=strength,
            guidance_scale=guidance_scale,
            seed=int(seed)
        )
        
        save_path = save_generated_image(modified_image, prompt, prefix="inpainting")
        gr.Info(f"수정 이미지가 저장되었습니다: {save_path}")
        
        return modified_image
    except Exception as e:
        raise gr.Error(f"이미지 수정 실패: {str(e)}")


def safe_modify_adapter(input_dict, source_image, prompt, neg_prompt, strength, guidance, seed):
    """Extracts mask from ImageEditor layers, uses source_image as the base."""
    from PIL import Image as PILImage

    if source_image is None:
        raise gr.Error("원본 이미지가 없습니다. 1단계에서 '내면 다듬기로 이동' 버튼을 누르거나, 이미지를 직접 업로드해 주세요.")
    if input_dict is None:
        raise gr.Error("마스킹 영역을 또한 없습니다. 아래 '마스크 그리기' 섹션에 직접 브러시로 칬해주세요.")

    # Extract mask from the drawing layer
    mask = None
    if isinstance(input_dict, dict):
        layers = input_dict.get("layers", [])
        if layers:
            layer_img = layers[0]
            if isinstance(layer_img, PILImage.Image):
                if layer_img.mode == "RGBA":
                    _, _, _, a = layer_img.split()
                    mask = a.convert("L")
                else:
                    mask = layer_img.convert("L")

    if mask is None:
        raise gr.Error("흔색 브러시로 수정할 영역을 먼저 칬해주세요! 칬한 흰 영역 = AI가 재생성하는 부분")

    image = source_image
    if image.size != mask.size:
        mask = mask.resize(image.size, PILImage.LANCZOS)

    return modify_art(image, mask, prompt, neg_prompt, strength, guidance, seed)



# --- UI Construction ---

# 프롬프트 빌더를 위한 옵션 사전
PROMPT_OPTIONS = {
    "매체": {
        "유화": "oil painting, thick brushstrokes, textured canvas",
        "수채화": "watercolor painting, soft bleeding colors, wet brush",
        "연필화": "pencil sketch, detailed graphite drawing, hatching",
        "디지털 아트": "digital art, clean lines, vibrant colors, trending on artstation",
        "파스텔": "soft pastel drawing, chalky texture, gentle colors"
    },
    "주제": {
        "평화로운 사람": "a serene figure, peaceful expression, human person",
        "피어나는 꽃": "blooming flowers, intricate petals, nature",
        "울창한 숲": "lush dense forest, tall trees, sunlight filtering through leaves",
        "고요한 바다": "calm ocean waves, horizon, peaceful water",
        "추상적 에너지": "abstract emotional energy, flowing shapes, expressive movement"
    },
    "분위기": {
        "따스한 노을": "warm golden hour lighting, sunset orange and pink glow",
        "차분한 새벽": "cool morning mist, blue hour, dim ambient light",
        "희망찬 오전": "bright sunny morning, high key lighting, clear sky",
        "신비로운 안개": "mysterious ethereal fog, soft diffused light, cinematic atmosphere"
    },
    "표현": {
        "명작 수준": "masterpiece, highly detailed, professional composition",
        "생생한 색감": "vivid colors, rich palette, saturation",
        "초현실주의": "surrealistic, dreamy, imaginative, ethereal",
        "예술적 터치": "artistic, creative, unique style"
    }
}

def build_prompt(media, subject, mood, style, custom_prompt):
    """선택된 옵션들을 조합하여 영문 프롬프트 생성"""
    parts = [PROMPT_OPTIONS["매체"][media], PROMPT_OPTIONS["주제"][subject], 
             PROMPT_OPTIONS["분위기"][mood], PROMPT_OPTIONS["표현"][style]]
    
    if custom_prompt and custom_prompt.strip():
        parts.append(f"({custom_prompt})")
        
    return ", ".join(parts)

# --- Restored Backend Functions ---

def set_theme_prompt(theme_idx):
    # 질감(Texture)과 색상(Color)을 앞세우고 인물 형태를 철저히 배제하는 프롬프트 전략
    prompts = [
        "delicate butterfly wing texture, vibrant hopeful colors, symbolic object", # 1. 상징적 개체
        "highly detailed stony texture, rough natural surface, crisp organic details", # 2. 질감 개선
        "warm golden hour glow, soft pastel color palette, radiating light", # 3. 감정적 색채
        "clean minimalist texture, smooth empty space, removing clutter", # 4. 방해 요소 제거
        "shimmering rainbow texture, soft sky colors, ethereal mist", # 5. 배경 기상
        "soft volumetric lighting, glowing edge highlights, radiant focal point", # 6. 조명 및 하이라이트
        "warm sphere of light, gentle ambient glowing sphere, peaceful energy", # 7. 인물 수정 -> 빛의 구체로 변경
        "silky smooth blending texture, soft color transition, blurred edges", # 8. 경계면 블렌딩
        "layered spatial depth, misty atmospheric perspective, deep field", # 9. 공간 깊이감
        "soft fabric texture, worn vintage object colors, comforted item" # 10. 소품 교체
    ]
    return prompts[theme_idx-1]

def apply_frame(image, frame_type):
    """이미지에 선택된 종류의 액자를 합성합니다."""
    if frame_type == "액자 없음" or not frame_type:
        return image
        
    from PIL import Image, ImageOps, ImageDraw
    
    # 기본 이미지 크기 확보
    img = image.convert("RGB")
    width, height = img.size
    
    # 액자 설정 (색상 및 두께)
    frames = {
        "고전적 금테 (Ornate Gold)": {"base": "#D4AF37", "inner": "#B8860B", "outer": "#FFD700", "thickness": 60},
        "고급 원목 (Classic Wood)": {"base": "#3E2723", "inner": "#1B100E", "outer": "#5D4037", "thickness": 50},
        "현대적 실버 (Modern Silver)": {"base": "#C0C0C0", "inner": "#808080", "outer": "#E8E8E8", "thickness": 40},
        "미니멀 블랙 (Minimal Black)": {"base": "#1A1A1A", "inner": "#000000", "outer": "#333333", "thickness": 35}
    }
    
    f = frames.get(frame_type, frames["미니멀 블랙"])
    t = f["thickness"]
    
    # 1. 외부 테두리 추가 (캔버스 확장)
    framed_img = ImageOps.expand(img, border=t, fill=f["base"])
    draw = ImageDraw.Draw(framed_img)
    
    # 2. 입체 효과 (가장자리 베젤)
    # 바깥쪽 밝은 선
    draw.rectangle([0, 0, width + 2*t, height + 2*t], outline=f["outer"], width=3)
    # 안쪽 어두운 선 (이미지 경계)
    draw.rectangle([t-2, t-2, width + t+1, height + t+1], outline=f["inner"], width=5)
    
    # 3. 그림자 처리 (약간의 입체감)
    shadow = Image.new("RGB", (width + 2*t, height + 2*t), f["base"])
    # 간단한 그래디언트 대신 단색 조합으로 액자 질감 표현
    
    return framed_img

def safe_modify_adapter(input_dict, prompt, neg, strength, guidance, seed):
    if input_dict is None:
        raise gr.Error("Please upload an image and draw a mask.")
    
    image = input_dict.get('background')
    layers = input_dict.get('layers')
    
    if not image:
        raise gr.Error("Background image missing.")
    if not layers:
        raise gr.Error("Please draw on the image to create a mask.")
        
    mask = layers[0]
    if mask.mode == 'RGBA':
        mask = mask.convert("L")
        mask = mask.point(lambda x: 255 if x > 0 else 0, mode='1')

    return modify_art(image, mask, prompt, neg, strength, guidance, seed)

from utils import OUTPUT_DIR, save_generated_image
GALLERY_LOG = os.path.join(OUTPUT_DIR, "gallery_log.json")

def load_gallery_data():
    import json
    if not os.path.exists(GALLERY_LOG):
        return []
    try:
        with open(GALLERY_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def load_gallery():
    data = load_gallery_data()
    return [item["path"] for item in data[-12:]] # Show last 12

def save_to_gallery(image, title, diary, heart_rate):
    import json
    import datetime
    if image is None:
        raise gr.Error("저장할 작품이 없습니다.")
        
    # Save image file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gallery_{timestamp}.png"
    save_dir = os.path.join(OUTPUT_DIR, "gallery")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.abspath(os.path.join(save_dir, filename))
    image.save(save_path)
    
    # Log to JSON
    new_entry = {
        "timestamp": timestamp,
        "path": save_path,
        "title": title if title else "무제",
        "diary": diary,
        "heart_rate": heart_rate,
        "comments": []
    }
    
    log_data = []
    if os.path.exists(GALLERY_LOG):
        try:
            with open(GALLERY_LOG, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    log_data = json.loads(content)
        except Exception as e:
            print(f"Log loading error: {e}. Starting fresh.")
            log_data = []
    
    log_data.append(new_entry)
    # Ensure parent directory of log exists
    os.makedirs(os.path.dirname(GALLERY_LOG), exist_ok=True)
    with open(GALLERY_LOG, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
        
    gr.Info("작품이 갤러리에 안전하게 보관되었습니다.")
    return load_gallery()

# --- Premium CSS for Modern Art Gallery Feel (Beige Theme) ---
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;700&display=swap');

.gradio-container {
    background-color: #fdfbf7 !important;
    font-family: 'Outfit', 'Noto Sans KR', sans-serif !important;
    color: #1a1a1a !important;
}

/* Sidebar Styling */
.sidebar-nav {
    background: #f8f4ed !important;
    border-right: 1px solid #e5e0d8 !important;
    height: 100vh !important;
    padding: 20px !important;
}

.nav-btn {
    text-align: left !important;
    justify-content: flex-start !important;
    border: none !important;
    background: transparent !important;
    color: #4b5563 !important;
    padding: 12px 15px !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-size: 1.1em !important;
    transition: all 0.2s ease !important;
}

.nav-btn:hover {
    background: #efece4 !important;
    color: #111827 !important;
}

.nav-btn.selected {
    background: #e5e0d8 !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

/* Content Area */
.main-content {
    background: #fdfbf7 !important;
    padding: 30px !important;
}

.gr-box, .gr-group, .gr-form {
    background: #ffffff !important;
    border: 1px solid #e5e0d8 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
}

/* Typo */
h1, h2, h3 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #e5e0d8;
    padding-bottom: 10px;
}

/* Button */
.gr-button-primary {
    background: #1a1a1a !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
}

.gr-button-primary:hover {
    background: #333333 !important;
}

/* Parameter Help Box */
.help-box {
    background: #f8f4ed !important;
    padding: 15px !important;
    border-radius: 8px !important;
    font-size: 0.9em !important;
    color: #4b5563 !important;
    border-left: 4px solid #d1d5db !important;
    margin-bottom: 10px !important;
}

.gallery-tip {
    background: #fdfbf7 !important;
    border: 1px solid #e5e0d8 !important;
    padding: 20px !important;
    color: #4b5563 !important;
    border-radius: 8px !important;
}

/* Gallery Museum Look */
#gallery-view img {
    box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
    border-radius: 2px !important;
    transition: transform 0.3s ease !important;
}

#gallery-view img:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 15px 30px rgba(0,0,0,0.4) !important;
}
"""

with gr.Blocks(title="마인드팔레트 (MindPalette)") as demo:
    # State for current page
    active_page = gr.State("expression")

    with gr.Row():
        # --- Sidebar Navigation ---
        with gr.Column(scale=2, elem_classes="sidebar-nav"):
            gr.Markdown("## 🏛️ 마인드팔레트")
            gr.Markdown("**AI 기반 비언어적 정서 발산 플랫폼**")
            gr.Markdown("""
            <div style="font-size: 0.8em; color: #64748b; margin-bottom: 15px;">
            내면의 언어를 시각화하여 정서적 안정과 통찰을 돕는 심리 분석 보조 도구입니다.
            </div>
            """)
            
            nav_expr = gr.Button("🖼️ 1단계: 감정 표현", elem_classes="nav-btn selected")
            nav_refine = gr.Button("✨ 2단계: 내면 다듬기", elem_classes="nav-btn")
            nav_gallery = gr.Button("🏛️ 3단계: 마인드 갤러리", elem_classes="nav-btn")
            
            gr.HTML("<hr style='border: 0; border-top: 1px solid #e5e0d8; margin: 20px 0;'>")
            gr.Markdown("### ⚙️ 시스템 설정")
            low_vram_toggle = gr.Checkbox(label="저사양 최적화 (Low VRAM)", value=True)
            privacy_toggle = gr.Checkbox(label="개인정보 보호 (갤러리 비저장)", value=False)
            
            gr.Markdown("""
            <div style="font-size: 0.8em; color: #9ca3af; margin-top: 50px;">
                © 2026 MindPalette Project<br/>비언어적 정서 외부화 플랫폼
            </div>
            """)

        # --- Main Content Area ---
        with gr.Column(scale=8, elem_classes="main-content"):
            
            # --- Page 1: Expression ---
            with gr.Group(visible=True) as page_expression:
                with gr.Row():
                    with gr.Column(scale=9):
                        gr.Markdown("# 🖼️ 1단계: 감정 표현 (Expression)")
                        gr.Markdown("내면의 혼란을 거칠게나마 스케치로 표현해 보세요. AI가 당신의 선을 지키며 예술로 승화시킵니다.")
                    with gr.Column(scale=1):
                        gr.Markdown("## 🎨")

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 🎨 1. 스케치 캔버스")
                        sketch_input = gr.ImageEditor(
                            type="pil", 
                            label="그림을 그려주세요", 
                            height=500,
                            brush=gr.Brush(colors=["#000000"], color_mode="fixed")
                        )
                        
                        gr.Markdown("### 🛠️ 2. 스타일 구성 (Curator's Palette)")
                        with gr.Group():
                            with gr.Row():
                                media_opt = gr.Dropdown(choices=list(PROMPT_OPTIONS["매체"].keys()), value="유화", label="예술 매체", interactive=True)
                                subject_opt = gr.Dropdown(choices=list(PROMPT_OPTIONS["주제"].keys()), value="평화로운 사람", label="핵심 주제", interactive=True)
                            with gr.Row():
                                mood_opt = gr.Dropdown(choices=list(PROMPT_OPTIONS["분위기"].keys()), value="따스한 노을", label="분위기/배경", interactive=True)
                                style_opt = gr.Dropdown(choices=list(PROMPT_OPTIONS["표현"].keys()), value="명작 수준", label="표현 품질", interactive=True)
                            
                            lora_style_opt = gr.Dropdown(
                                choices=["기본 (Standard)", "Soft Watercolor", "Warm Oil Pastel", "Muted Tones", "Dreamy Sketch", "Ink Wash Painting"],
                                value="기본 (Standard)",
                                label="🌿 치료적 화풍 (Therapeutic LoRA)",
                                interactive=True
                            )
                        
                        custom_input = gr.Textbox(
                            label="직접 입력 (Optional)", 
                            placeholder="그림에 담긴 특별한 이야기를 적어주세요.",
                            lines=2
                        )
                        
                        with gr.Accordion("⚙️ AI 엔진 정밀 설정 (도움말)", open=False):
                            gr.Markdown("""
                            <div class="help-box">
                            <strong>창의성(Guidance)</strong>: AI가 내 명령어를 얼마나 엄격하게 따를지 결정합니다. (높을수록 명령어에 충실, 낮을수록 AI의 자율성 증가)<br/>
                            <strong>스케치 준수율(Fidelity)</strong>: 내 손그림 선을 얼마나 그대로 유지할지 결정합니다. (높을수록 내 선을 고집하고, 낮을수록 AI가 형태를 더 다듬습니다)
                            </div>
                            """)
                            seed_input = gr.Number(label="AI 시드(Seed)", value=42, precision=0)
                            guidance_scale = gr.Slider(minimum=1, maximum=20, value=7.5, label="창의성 가이드 (Guidance)")
                            adapter_scale = gr.Slider(minimum=0, maximum=1, value=0.9, label="스케치 준수율 (Fidelity)")
                            neg_prompt = gr.Textbox(label="배제할 요소 (Negative)", value="low quality, bad anatomy, man, male, beard")
                        
                        gen_btn = gr.Button("🎉 창작 시작하기", variant="primary")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### ✨ 예술적 투영 결과")
                        result_image = gr.Image(label="생성된 마스터피스", type="pil", height=500)
                        gr.Markdown("""
                        <div class="gallery-tip">
                        <strong>큐레이터의 조언</strong>: 작품이 마음에 드시나요? 결과가 아쉽다면 '스케치 준수율'을 낮추어 AI에게 더 많은 자유를 주거나, 캔버스를 더 정교하게 다듬어 보세요.
                        </div>
                        """)
                        move_to_refine_btn = gr.Button("✨ 내면 다듬기로 이동", variant="secondary")

            # --- Page 2: Refinement ---
            with gr.Group(visible=False) as page_refinement:
                gr.Markdown("# ✨ 2단계: 내면 다듬기 (Refinement)")
                gr.Markdown("작품의 특정 영역을 지우거나 덧칠하여 감정을 조절해 보세요. **인물은 배제되고 오직 색채와 질감에만 집중합니다.**")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        # 2A: 원본 이미지 표시 / 업로드
                        refine_source_image = gr.Image(
                            label="📷 원본 이미지 (1단계에서 자동으로 불러옵니다 / 직접 업로드도 가능)",
                            type="pil",
                            height=420,
                            interactive=True
                        )

                        gr.Markdown("### 🖌️ 2-2. 마스크 그리기 (수정할 영역을 흰색으로 칠하세요)")
                        inpainting_input = gr.ImageEditor(
                            label="여기서 브러시로 칠한 흰색 영역이 AI가 바꾸는 마스크입니다",
                            type="pil",
                            brush=gr.Brush(colors=["#FFFFFF"], color_mode="fixed", size=30),
                            eraser=gr.Eraser(size=25),
                            height=420,
                            interactive=True,
                        )
                        with gr.Group():
                            gr.Markdown("### 💡 2-2. 치유 테마 큐레이션 (버튼 클릭 시 화풍 유지)")
                            with gr.Row():
                                theme_btn1 = gr.Button("🦋 상징물", variant="secondary", size="sm")
                                theme_btn2 = gr.Button("✨ 질감", variant="secondary", size="sm")
                                theme_btn3 = gr.Button("🎨 색채", variant="secondary", size="sm")
                                theme_btn4 = gr.Button("🧹 정리", variant="secondary", size="sm")
                                theme_btn5 = gr.Button("🌈 분위기", variant="secondary", size="sm")
                            with gr.Row():
                                theme_btn6 = gr.Button("🔦 조명", variant="secondary", size="sm")
                                theme_btn7 = gr.Button("🔮 빛", variant="secondary", size="sm")
                                theme_btn8 = gr.Button("🌊 융합", variant="secondary", size="sm")
                                theme_btn9 = gr.Button("🏔️ 깊이", variant="secondary", size="sm")
                                theme_btn10 = gr.Button("🧸 소품", variant="secondary", size="sm")

                        mod_prompt = gr.Textbox(label="수정 명령어 (색상/질감 중심)", placeholder="예: '흰색으로 부드럽게', '따뜻한 햇살 느낌'")
                        
                        with gr.Accordion("⚙️ 수정 엔진 정밀 설정", open=False):
                            gr.Markdown("""
                            <div class="help-box">
                            <strong>수정 강도(Strength)</strong>: 기존 이미지를 얼마나 많이 변화시킬지 결정합니다. (높을수록 새로운 내용이 많이 채워집니다)
                            </div>
                            """)
                            mod_strength = gr.Slider(minimum=0, maximum=1, value=0.75, label="수정 강도 (Strength)")
                            mod_seed = gr.Number(label="AI 시드", value=42, precision=0)
                            mod_guidance = gr.Slider(minimum=1, maximum=20, value=7.5, label="창의성 가이드")
                            mod_neg = gr.Textbox(label="배제할 요소", value="human, person, face, features, portrait, man, woman, child, clothes, skin")

                        mod_btn = gr.Button("🖌️ 이미지 다듬기 적용", variant="primary")
                        
                    with gr.Column(scale=1):
                        gr.Markdown("### 📔 3. 내러티브 일기")
                        mod_result = gr.Image(label="다듬어진 최종 작품", type="pil", height=500)
                        
                        with gr.Group():
                            art_title = gr.Textbox(label="🎨 작품 이름", placeholder="이 작품에 어울리는 이름을 지어주세요.", lines=1)
                            diary_input = gr.Textbox(label="📔 오늘의 소회 (그림 일기)", placeholder="작품을 보며 느껴지는 감정을 기록해 보세요.", lines=4)
                            frame_opt = gr.Dropdown(
                                choices=["액자 없음", "고전적 금테 (Ornate Gold)", "고급 원목 (Classic Wood)", "현대적 실버 (Modern Silver)", "미니멀 블랙 (Minimal Black)"],
                                value="액자 없음",
                                label="🏛️ 전시 액자 선택"
                            )
                            with gr.Row():
                                heart_rate_input = gr.Number(label="💓 심박수 연동", value=75)
                                save_btn = gr.Button("🏆 갤러리 등록 및 전시", variant="primary")

            # --- Page 3: Gallery ---
            with gr.Group(visible=False) as page_gallery:
                gr.Markdown("# 🏛️ 3단계: 마인드 갤러리 (Archive)")
                gr.Markdown("당신의 모든 정서적 여정이 이곳에 현대 미술관처럼 큐레이팅됩니다. 작품을 클릭하여 상세 정보를 확인하고 소통해 보세요.")
                
                with gr.Row():
                    with gr.Column(scale=6):
                        gallery_view = gr.Gallery(label="나의 마스터피스 아카이브", columns=4, height="auto", object_fit="contain")
                    
                    with gr.Column(scale=4, visible=False) as detail_view_area:
                        gr.Markdown("### 🖼️ 작품 상세 감상")
                        detail_img = gr.Image(label="선택된 작품", interactive=False)
                        detail_title = gr.Markdown("## 작품 제목")
                        detail_diary = gr.Markdown("작품 설명...")
                        detail_hr = gr.Markdown("💓 심박수: --")
                        
                        gr.HTML("<hr>")
                        gr.Markdown("### 💬 감상평 (Comments)")
                        detail_comments = gr.Markdown("아직 댓글이 없습니다.")
                        comment_input = gr.Textbox(label="댓글 남기기", placeholder="작품에 대한 느낌을 적어주세요.")
                        comment_btn = gr.Button("댓글 등록", size="sm")
                        
                        gr.HTML("<hr>")
                        gr.Markdown("### 🚀 SNS 공유 & 초대")
                        with gr.Row():
                            share_btn = gr.Button("🔗 초대장 링크 복사", size="sm", variant="secondary")
                            gr.HTML("""
                            <div style="display: flex; gap: 8px;">
                                <a href="https://www.instagram.com" target="_blank" style="text-decoration: none; padding: 4px 10px; background: #E1306C; color: white; border-radius: 4px; font-size: 0.8em; font-weight: bold;">Instagram</a>
                                <a href="https://twitter.com" target="_blank" style="text-decoration: none; padding: 4px 10px; background: #1DA1F2; color: white; border-radius: 4px; font-size: 0.8em; font-weight: bold;">X</a>
                                <a href="https://web.facebook.com" target="_blank" style="text-decoration: none; padding: 4px 10px; background: #4267B2; color: white; border-radius: 4px; font-size: 0.8em; font-weight: bold;">FB</a>
                            </div>
                            """)

    # --- Logic: Sidebar Page Switching ---
    def switch_page(page):
        return {
            page_expression: gr.update(visible=(page == "expression")),
            page_refinement: gr.update(visible=(page == "refinement")),
            page_gallery: gr.update(visible=(page == "gallery")),
            nav_expr: gr.update(elem_classes=f"nav-btn {'selected' if page == 'expression' else ''}"),
            nav_refine: gr.update(elem_classes=f"nav-btn {'selected' if page == 'refinement' else ''}"),
            nav_gallery: gr.update(elem_classes=f"nav-btn {'selected' if page == 'gallery' else ''}")
        }

    nav_expr.click(fn=lambda: "expression", outputs=active_page).then(fn=switch_page, inputs=active_page, outputs=[page_expression, page_refinement, page_gallery, nav_expr, nav_refine, nav_gallery])
    nav_refine.click(fn=lambda: "refinement", outputs=active_page).then(fn=switch_page, inputs=active_page, outputs=[page_expression, page_refinement, page_gallery, nav_expr, nav_refine, nav_gallery])
    nav_gallery.click(fn=lambda: "gallery", outputs=active_page).then(fn=switch_page, inputs=active_page, outputs=[page_expression, page_refinement, page_gallery, nav_expr, nav_refine, nav_gallery])

    # --- Generation & Inpainting Logic (Respecting User Request for Zero-Human) ---
    def handle_generation(sketch, media, subject, mood, style, custom, lora_style, neg, guidance, adapter, seed, low_vram):
        if model.low_vram != low_vram:
            model.low_vram = low_vram
            # Models will be re-loaded with the new low_vram setting upon next usage
            model.cleanup_generation_pipeline()
            model.cleanup_inpainting_pipeline()
        full_prompt = build_prompt(media, subject, mood, style, custom)
        style_context = f"{media} style, {style}"
        return generate_art(sketch, full_prompt, neg, guidance, adapter, seed, style_name=lora_style), style_context

    style_context_state = gr.State("")
    gen_btn.click(
        fn=handle_generation, 
        inputs=[sketch_input, media_opt, subject_opt, mood_opt, style_opt, custom_input, lora_style_opt, neg_prompt, guidance_scale, adapter_scale, seed_input, low_vram_toggle], 
        outputs=[result_image, style_context_state]
    )

    def to_refinement(image):
        if image is None:
            gr.Warning("먼저 1단계에서 이미지를 생성해 주세요!")
            return gr.update(), gr.update(), gr.update()
        # Set the source image display AND initialize the mask editor background
        editor_value = {"background": image, "composite": image, "layers": []}
        return gr.update(visible=False), gr.update(value=image), gr.update(value=editor_value)

    def show_refinement_page():
        return {
            page_expression: gr.update(visible=False),
            page_refinement: gr.update(visible=True),
            page_gallery: gr.update(visible=False),
            nav_expr: gr.update(elem_classes="nav-btn"),
            nav_refine: gr.update(elem_classes="nav-btn selected"),
            nav_gallery: gr.update(elem_classes="nav-btn")
        }

    move_to_refine_btn.click(
        fn=to_refinement,
        inputs=[result_image],
        outputs=[page_expression, refine_source_image, inpainting_input]
    ).then(
        fn=show_refinement_page,
        inputs=None,
        outputs=[page_expression, page_refinement, page_gallery, nav_expr, nav_refine, nav_gallery]
    )

    def handle_mod_with_style(source_img, input_dict, prompt, neg, strength, guidance, seed, style_context):
        # Apply Therapeutic Color Bias Control (Muted, Pastel, Low Saturation)
        therapeutic_prefix = "therapeutic high quality art, muted tones, pastel palette, soft artistic texture, desaturated, gentle lighting"
        refined_prompt = f"{therapeutic_prefix}, abstract {prompt}, {style_context}, texture and colors only, no humans, non-figurative art"
        
        # Combine user negative with strong anti-human and anti-vivid keywords
        vivid_neg = "vivid colors, high saturation, neon, bright colors, high contrast, sharp edges"
        refined_neg = f"{neg}, {vivid_neg}, human, person, face, portrait, body parts, man, woman, crowd"
        return safe_modify_adapter(input_dict, source_img, refined_prompt, refined_neg, strength, guidance, seed)

    mod_btn.click(
        fn=handle_mod_with_style,
        inputs=[refine_source_image, inpainting_input, mod_prompt, mod_neg, mod_strength, mod_guidance, mod_seed, style_context_state],
        outputs=[mod_result]
    )

    def handle_save(image, title, diary, heart_rate, frame_type, privacy):
        if privacy:
            gr.Warning("개인정보 보호 모드: 세션 데이터가 서버에 남지 않습니다.")
            return load_gallery()
        
        # Apply Frame if selected
        framed_image = apply_frame(image, frame_type)
        return save_to_gallery(framed_image, title, diary, heart_rate)

    save_btn.click(fn=handle_save, inputs=[mod_result, art_title, diary_input, heart_rate_input, frame_opt, privacy_toggle], outputs=[gallery_view])
    
    # --- Social & Detailed View Logic ---
    selected_idx = gr.State(None)

    def on_select(evt: gr.SelectData):
        data = load_gallery_data()
        # Gallery shows last 12, so calculate correct index from the end
        view_data = data[-12:]
        idx = evt.index
        if idx >= len(view_data): return gr.update(visible=False), None, "", "", "", "", None
        
        item = view_data[idx]
        comments_html = "<br>".join([f"<b>익명:</b> {c}" for c in item.get("comments", [])]) if item.get("comments") else "아직 댓글이 없습니다."
        
        return (
            gr.update(visible=True), 
            item["path"], 
            f"## {item.get('title', '무제')}", 
            f"**설명:** {item.get('diary', '')}", 
            f"💓 심박수: {item.get('heart_rate', '--')}",
            comments_html,
            idx
        )

    gallery_view.select(
        fn=on_select, 
        outputs=[detail_view_area, detail_img, detail_title, detail_diary, detail_hr, detail_comments, selected_idx]
    )

    def add_comment(comment, idx):
        if idx is None or not comment: return gr.Warning("이미지를 선택하거나 내용을 입력하세요.")
        
        data = load_gallery_data()
        view_data = data[-12:]
        actual_idx = len(data) - len(view_data) + idx
        
        if "comments" not in data[actual_idx]: data[actual_idx]["comments"] = []
        data[actual_idx]["comments"].append(comment)
        
        with open(GALLERY_LOG, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        # Refresh detail view
        item = data[actual_idx]
        comments_html = "<br>".join([f"<b>익명:</b> {c}" for c in item.get("comments", [])])
        return comments_html, ""

    comment_btn.click(fn=add_comment, inputs=[comment_input, selected_idx], outputs=[detail_comments, comment_input])
    
    def copy_share_link():
        gr.Info("🏛️ 모바일 초대장 링크가 클립보드에 복사되었습니다! (시뮬레이션)")
        return gr.update()
        
    share_btn.click(fn=copy_share_link, outputs=[])
    
    demo.load(fn=load_gallery, outputs=[gallery_view])

    # --- Theme Callbacks ---
    theme_btn1.click(lambda: set_theme_prompt(1), None, mod_prompt)
    theme_btn2.click(lambda: set_theme_prompt(2), None, mod_prompt)
    theme_btn3.click(lambda: set_theme_prompt(3), None, mod_prompt)
    theme_btn4.click(lambda: set_theme_prompt(4), None, mod_prompt)
    theme_btn5.click(lambda: set_theme_prompt(5), None, mod_prompt)
    theme_btn6.click(lambda: set_theme_prompt(6), None, mod_prompt)
    theme_btn7.click(lambda: set_theme_prompt(7), None, mod_prompt)
    theme_btn8.click(lambda: set_theme_prompt(8), None, mod_prompt)
    theme_btn9.click(lambda: set_theme_prompt(9), None, mod_prompt)
    theme_btn10.click(lambda: set_theme_prompt(10), None, mod_prompt)

if __name__ == "__main__":
    demo.queue().launch(share=False, css=CUSTOM_CSS)
