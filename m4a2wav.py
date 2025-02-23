from pydub import AudioSegment
import os

def convert_m4a_to_wav():
    # 確保input和output資料夾存在
    input_dir = "input"
    output_dir = "output"
    
    # 檢查input資料夾是否存在
    if not os.path.exists(input_dir):
        print(f"錯誤: 找不到輸入資料夾 '{input_dir}'")
        print(f"請建立 '{input_dir}' 資料夾並放入 .m4a 檔案")
        return
    
    # 確保output資料夾存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已建立輸出資料夾 '{output_dir}'")
    
    # 檢查input資料夾中是否有m4a檔案
    m4a_files = [f for f in os.listdir(input_dir) if f.endswith('.m4a')]
    if not m4a_files:
        print(f"在 '{input_dir}' 資料夾中找不到任何 .m4a 檔案")
        return
    
    # 取得所有m4a檔案
    for filename in m4a_files:
        # 設定輸入和輸出檔案路徑
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".m4a", ".wav"))
        
        try:
            # 確認輸入檔案存在且可讀取
            if not os.path.isfile(input_path):
                print(f"錯誤: 找不到檔案 '{input_path}'")
                continue
                
            # 讀取m4a檔案
            audio = AudioSegment.from_file(input_path, format="m4a")
            
            # 轉換並儲存為wav
            audio.export(output_path, format="wav")
            print(f"成功轉換: {filename}")
            
        except Exception as e:
            print(f"轉換失敗 {filename}: {str(e)}")

if __name__ == "__main__":
    convert_m4a_to_wav()
