from cog import BasePredictor, Input, Path
import os
from sonic import Sonic

class Predictor(BasePredictor):
    def setup(self):
        """初始化 Sonic 模型"""
        # 初始化 Sonic，假設參數 0 表示使用第一個 GPU
        self.pipe = Sonic(0)

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
            seed=seed  # 如果 Sonic 的 process 支持 seed，否則移除
        )

        # 返回生成的影片路徑
        return Path(output_path)