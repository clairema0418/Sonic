from cog import BasePredictor, Input, Path
import os
from sonic import Sonic
from huggingface_hub import hf_hub_download, snapshot_download
import time
import warnings

# 忽略特定的警告
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

class Predictor(BasePredictor):
    def setup(self):
        """初始化 Sonic 模型"""
        # 定義模型路徑
        checkpoint_dir = "/src/checkpoints"
        model_paths = {
            "svd": f"{checkpoint_dir}/stable-video-diffusion-img2vid-xt",
            "sonic": f"{checkpoint_dir}/Sonic",
            "whisper": f"{checkpoint_dir}/whisper-tiny",
            "rife": f"{checkpoint_dir}/RIFE"
        }

        # 確保檢查點目錄存在
        os.makedirs(checkpoint_dir, exist_ok=True)

        # 設定下載參數
        max_retries = 3

        def download_with_retry(func, **kwargs):
            for attempt in range(max_retries):
                try:
                    common_args = {
                        "token": os.getenv("HUGGING_FACE_HUB_TOKEN")
                    }
                    
                    if func == snapshot_download:
                        return func(
                            repo_id=kwargs["repo_id"],
                            local_dir=kwargs["local_dir"],
                            **common_args
                        )
                    else:  # hf_hub_download
                        return func(
                            repo_id=kwargs["repo_id"],
                            filename=kwargs["filename"],
                            local_dir=kwargs["local_dir"],
                            timeout=60,
                            **common_args
                        )
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise Exception(f"下載失敗，已重試 {max_retries} 次: {str(e)}")
                    print(f"下載失敗，等待5秒後重試... (嘗試 {attempt + 1}/{max_retries})")
                    print(f"錯誤信息: {str(e)}")
                    time.sleep(5)

        try:
            # 下載模型檔案
            print("下載 Sonic 模型...")
            download_with_retry(
                snapshot_download,
                repo_id="LeonJoe13/Sonic",
                local_dir=model_paths["sonic"]
            )

            print("下載 Stable Video Diffusion 模型...")
            download_with_retry(
                snapshot_download,
                repo_id="stabilityai/stable-video-diffusion-img2vid-xt",
                local_dir=model_paths["svd"]
            )

            print("下載 Whisper Tiny 模型...")
            download_with_retry(
                snapshot_download,
                repo_id="openai/whisper-tiny",
                local_dir=model_paths["whisper"]
            )

            print("下載 RIFE 模型...")
            download_with_retry(
                hf_hub_download,
                repo_id="LeonJoe13/Sonic",
                filename="RIFE/flownet.pkl",
                local_dir=model_paths["rife"]
            )

            print("下載 YOLOFace 模型...")
            download_with_retry(
                hf_hub_download,
                repo_id="LeonJoe13/Sonic",
                filename="yoloface_v5m.pt",
                local_dir=checkpoint_dir
            )

        except Exception as e:
            raise Exception(f"模型下載失敗: {str(e)}")

        # 初始化 Sonic，傳入模型路徑
        self.pipe = Sonic(0, model_path=model_paths)

    def predict(
        self,
        image: Path = Input(description="Input portrait image (e.g., PNG, JPG)"),
        audio: Path = Input(description="Input audio file (e.g., WAV, MP3)"),
        dynamic_scale: float = Input(description="Dynamic scale factor", default=1.0),
        crop: bool = Input(description="Crop the image based on face detection", default=False),
        seed: int = Input(description="Random seed for reproducibility", default=None, ge=0)
    ) -> Path:
        """運行推理並生成影片"""
        # 將輸入路徑轉換為字符串
        image_path = str(image)
        audio_path = str(audio)
        output_path = "output.mp4"  # 臨時輸出路徑

        # 前處理圖像
        face_info = self.pipe.preprocess(image_path, expand_ratio=0.5)
        if face_info['face_num'] < 0:
            raise ValueError("No face detected in the input image.")

        # 如果啟用裁剪，處理圖像
        if crop:
            crop_image_path = image_path + '.crop.png'
            self.pipe.crop_image(image_path, crop_image_path, face_info['crop_bbox'])
            image_path = crop_image_path  # 更新為裁剪後的圖像路徑

        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 執行推理
        self.pipe.process(
            image_path,
            audio_path,
            output_path,
            min_resolution=512,
            inference_steps=25,
            dynamic_scale=dynamic_scale,
            seed=seed
        )

        # 返回生成的影片路徑
        return Path(output_path)