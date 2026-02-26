
import torch
import gc
from diffusers import (
    StableDiffusionXLAdapterPipeline,
    T2IAdapter,
    EulerAncestralDiscreteScheduler,
    AutoencoderKL,
    AutoPipelineForInpainting
)
from controlnet_aux.pidi import PidiNetDetector
from PIL import Image
import numpy as np

class ArtTherapyModel:
    """
    미술 치료를 위한 AI 모델 엔진 클래스.
    SDXL Adapter(스케치-이미지)와 Kandinsky 2.2(인페인팅) 파이프라인을 관리합니다.
    """
    def __init__(self, device='cuda', low_vram=False):
        self.device = device
        self.low_vram = low_vram
        self.pipeline = None
        self.adapter = None
        self.pidinet = None
        self.inpainting_pipeline = None
        self.active_lora = None

    # Therapeutic LoRA Style Mapping (SDXL 1.0 compatible - verified HF IDs)
    THERAPEUTIC_LORAS = {
        "Soft Watercolor": "ostris/watercolor_style_lora_sdxl",
        "Warm Oil Pastel": "artificialguybr/pastel-painting-sdxl",
        "Muted Tones": "sayakasasaki/muted-color-sdxl",
        "Dreamy Sketch": "artificialguybr/LineArt-SDXL",
        "Ink Wash Painting": "alvdansen/midsommar-cartoon"
    }

    def load_generation_pipeline(self):
        """Loads the SDXL Adapter pipeline for sketch-to-image."""
        if self.pipeline is not None:
            return

        print("Loading SDXL Adapter Pipeline...")
        try:
            # 1. Load Adapter
            self.adapter = T2IAdapter.from_pretrained(
                "TencentARC/t2i-adapter-sketch-sdxl-1.0",
                torch_dtype=torch.float16,
                variant="fp16"
            ).to(self.device)

            # 2. Load Scheduler & VAE
            model_id = 'stabilityai/stable-diffusion-xl-base-1.0'
            euler_a = EulerAncestralDiscreteScheduler.from_pretrained(
                model_id, subfolder="scheduler"
            )
            vae = AutoencoderKL.from_pretrained(
                "madebyollin/sdxl-vae-fp16-fix",
                torch_dtype=torch.float16
            )

            # 3. Assemble Pipeline
            self.pipeline = StableDiffusionXLAdapterPipeline.from_pretrained(
                model_id,
                vae=vae,
                adapter=self.adapter,
                scheduler=euler_a,
                torch_dtype=torch.float16,
                variant="fp16",
            )
            
            if self.low_vram:
                self.pipeline.enable_model_cpu_offload()
            else:
                self.pipeline.to(self.device)

            # 4. Load PidiNet for edge detection
            self.pidinet = PidiNetDetector.from_pretrained("lllyasviel/Annotators").to(self.device)
            print("Generation Pipeline Loaded Successfully.")

        except Exception as e:
            print(f"Error loading generation pipeline: {e}")
            raise e

    def apply_lora(self, style_name, weight=0.8):
        """Applies a therapeutic LoRA to the SDXL pipeline."""
        self.load_generation_pipeline()
        
        if style_name not in self.THERAPEUTIC_LORAS or style_name == "기본 (Standard)":
            if self.active_lora:
                print(f"Unloading LoRA: {self.active_lora}")
                self.pipeline.unload_lora_weights()
                self.active_lora = None
            return

        lora_id = self.THERAPEUTIC_LORAS[style_name]
        print(f"Applying LoRA: {style_name} ({lora_id}) with weight {weight}")
        
        try:
            # Unload previous if any
            if self.active_lora:
                try:
                    self.pipeline.unload_lora_weights()
                except Exception:
                    pass
                self.active_lora = None
            
            self.pipeline.load_lora_weights(lora_id)
            self.pipeline.fuse_lora(lora_scale=weight)
            self.active_lora = style_name
            print(f"LoRA {style_name} loaded successfully.")
        except Exception as e:
            print(f"[WARNING] LoRA '{style_name}' ({lora_id}) 로드 실패: {e}")
            print(f"[INFO] 프롬프트 기반 스타일로 대체 적용합니다.")
            self.active_lora = None

    def load_inpainting_pipeline(self):
        """Loads the Inpainting pipeline."""
        if self.inpainting_pipeline is not None:
            return

        print("Loading Inpainting Pipeline...")
        try:
            # Clean up generation pipeline to save memory if needed
            if self.low_vram and self.pipeline is not None:
                self.cleanup_generation_pipeline()

            self.inpainting_pipeline = AutoPipelineForInpainting.from_pretrained(
                "kandinsky-community/kandinsky-2-2-decoder-inpaint",
                torch_dtype=torch.float16
            )
            
            if self.low_vram:
                self.inpainting_pipeline.enable_model_cpu_offload()
            else:
                self.inpainting_pipeline.to(self.device)
                
            print("Inpainting Pipeline Loaded Successfully.")

        except Exception as e:
            print(f"Error loading inpainting pipeline: {e}")
            raise e

    def generate_image(self, sketch_image, prompt, negative_prompt="", num_steps=30, guidance_scale=7.5, adapter_scale=0.9, seed=42, style_name="기본 (Standard)"):
        """Generates an image from a sketch using potential LoRA styles."""
        self.load_generation_pipeline()
        
        # Apply style if requested
        self.apply_lora(style_name)
        
        # Preprocess sketch
        if sketch_image.mode != "RGB":
            sketch_image = sketch_image.convert("RGB")
            
        sketch_image = sketch_image.resize((1024, 1024))
        edge_map = self.pidinet(
            sketch_image, detect_resolution=1024, image_resolution=1024, apply_filter=True
        )

        # Set seed
        generator = torch.Generator(device=self.device).manual_seed(seed)

        # Generate
        image = self.pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=edge_map,
            num_inference_steps=num_steps,
            adapter_conditioning_scale=adapter_scale,
            guidance_scale=guidance_scale,
            generator=generator
        ).images[0]

        return image, edge_map

    def inpaint_image(self, image, mask_image, prompt, negative_prompt="", strength=0.75, guidance_scale=7.5, seed=42):
        """Modifies an image using inpainting."""
        self.load_inpainting_pipeline()
        
        generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # Resize inputs to 1024x1024 for consistency
        image = image.resize((1024, 1024))
        mask_image = mask_image.resize((1024, 1024))

        output = self.inpainting_pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=image,
            mask_image=mask_image,
            strength=strength,
            guidance_scale=guidance_scale,
            generator=generator
        ).images[0]

        return output

    def cleanup_generation_pipeline(self):
        """Cleans up generation pipeline to free memory."""
        print("Cleaning up generation pipeline...")
        if self.pipeline:
            del self.pipeline
            self.pipeline = None
        if self.adapter:
            del self.adapter
            self.adapter = None
        if self.pidinet:
            del self.pidinet
            self.pidinet = None
        
        gc.collect()
        torch.cuda.empty_cache()

    def cleanup_inpainting_pipeline(self):
        """Cleans up inpainting pipeline to free memory."""
        print("Cleaning up inpainting pipeline...")
        if self.inpainting_pipeline:
            del self.inpainting_pipeline
            self.inpainting_pipeline = None
            
        gc.collect()
        torch.cuda.empty_cache()
