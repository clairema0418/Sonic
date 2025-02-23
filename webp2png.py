from PIL import Image
import os

def convert_webp_to_png(input_dir):
    """
    將指定目錄下的所有 WebP 圖片轉換為 PNG 格式
    
    Args:
        input_dir (str): 包含 WebP 圖片的目錄路徑
    """
    # 確保輸入的目錄存在
    if not os.path.exists(input_dir):
        print(f"錯誤：目錄 '{input_dir}' 不存在")
        return

    # 遍歷目錄中的所有文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.webp'):
            # 構建完整的文件路徑
            input_path = os.path.join(input_dir, filename)
            # 創建輸出文件名（將 .webp 替換為 .png）
            output_filename = filename.rsplit('.', 1)[0] + '.png'
            output_path = os.path.join(input_dir, output_filename)

            try:
                # 打開 WebP 圖片
                image = Image.open(input_path)
                # 轉換並保存為 PNG
                image.save(output_path, 'PNG')
                print(f"已成功轉換：{filename} -> {output_filename}")
            except Exception as e:
                print(f"轉換 {filename} 時發生錯誤：{str(e)}")

if __name__ == "__main__":
    # 指定輸入目錄為當前目錄下的 input 資料夾
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(current_dir, "input")
    print(f"正在處理目錄：{input_dir}")
    convert_webp_to_png(input_dir)
