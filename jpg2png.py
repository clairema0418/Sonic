from PIL import Image
import os

def convert_jpg_to_png():
    # 確保 input 和 output 資料夾存在
    input_dir = "input"
    output_dir = "output"
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 取得所有 jpg 檔案
    jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
    
    if not jpg_files:
        print("在 input 資料夾中沒有找到 JPG 圖片")
        return
    
    # 轉換每個 jpg 檔案
    for jpg_file in jpg_files:
        try:
            # 開啟圖片
            with Image.open(os.path.join(input_dir, jpg_file)) as img:
                # 準備輸出檔案名稱
                output_filename = os.path.splitext(jpg_file)[0] + '.png'
                output_path = os.path.join(output_dir, output_filename)
                
                # 儲存為 PNG
                img.save(output_path, 'PNG')
                print(f"已將 {jpg_file} 轉換為 {output_filename}")
                
        except Exception as e:
            print(f"轉換 {jpg_file} 時發生錯誤: {str(e)}")

if __name__ == "__main__":
    convert_jpg_to_png()
