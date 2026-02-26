
import os
from datetime import datetime
from PIL import Image

# Handle Output Directory for different environments (Local vs Hugging Face)
def get_output_dir():
    # Hugging Face Spaces usually has /tmp with write access
    if os.environ.get("SPACE_ID") or not os.access(".", os.W_OK):
        return "/tmp/mindpalette_outputs"
    return "outputs"

OUTPUT_DIR = get_output_dir()

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_generated_image(image, prompt, prefix="gen"):
    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    image.save(filepath)
    
    # Save prompt metadata
    meta_filepath = os.path.join(OUTPUT_DIR, f"{prefix}_{timestamp}.txt")
    with open(meta_filepath, "w", encoding="utf-8") as f:
        f.write(f"Prompt: {prompt}\n")
        
    return filepath

def resize_for_condition_image(input_image: Image, resolution: int = 1024):
    input_image = input_image.convert("RGB")
    W, H = input_image.size
    k = float(resolution) / min(H, W)
    H *= k
    W *= k
    H = int(round(H / 64.0)) * 64
    W = int(round(W / 64.0)) * 64
    img = input_image.resize((W, H), resample=Image.LANCZOS)
    return img
