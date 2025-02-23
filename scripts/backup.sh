#!/bin/bash

# 設定變數
IMAGE_NAME="cog-sonic:latest"          # 替換為你的映像名稱，例如 cog-sonic:latest
BACKUP_DIR="/home/ubuntu/a100/backup/sonic"         # 替換為你想要的備份資料夾
BACKUP_FILE="sonic-image.tar"          # 備份檔案名稱

# 確保備份資料夾存在
mkdir -p "$BACKUP_DIR"

# 檢查映像是否存在
echo "檢查映像 $IMAGE_NAME 是否存在..."
if ! docker images -q "$IMAGE_NAME" | grep -q .; then
    echo "錯誤：映像 $IMAGE_NAME 不存在，請先運行 'cog build' 構建映像。"
    exit 1
fi

# 備份映像到 .tar 檔案
echo "正在備份映像 $IMAGE_NAME 到 $BACKUP_DIR/$BACKUP_FILE..."
docker save -o "$BACKUP_DIR/$BACKUP_FILE" "$IMAGE_NAME"
if [ $? -eq 0 ]; then
    echo "備份完成：$BACKUP_DIR/$BACKUP_FILE"
else
    echo "備份失敗，請檢查權限或空間是否足夠。"
    exit 1
fi

# 壓縮 .tar 檔案
echo "正在壓縮 $BACKUP_FILE..."
gzip "$BACKUP_DIR/$BACKUP_FILE"
if [ $? -eq 0 ]; then
    echo "壓縮完成：$BACKUP_DIR/$BACKUP_FILE.gz"
else
    echo "壓縮失敗，請檢查 gzip 是否安裝或空間是否足夠。"
    exit 1
fi

# 顯示備份檔案資訊
ls -lh "$BACKUP_DIR/$BACKUP_FILE.gz"