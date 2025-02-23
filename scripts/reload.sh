#!/bin/bash

# 設定變數
BACKUP_DIR="/home/ubuntu/a100/backup/sonic"         # 替換為你的備份資料夾
BACKUP_FILE="sonic-image.tar"          # 備份檔案名稱（不含 .gz）

# 檢查壓縮檔案是否存在
echo "檢查備份檔案 $BACKUP_DIR/$BACKUP_FILE.gz 是否存在..."
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE.gz" ]; then
    echo "錯誤：備份檔案 $BACKUP_DIR/$BACKUP_FILE.gz 不存在。"
    exit 1
fi

# 解壓 .tar.gz 檔案
echo "正在解壓 $BACKUP_FILE.gz..."
gunzip -k "$BACKUP_DIR/$BACKUP_FILE.gz"
if [ $? -eq 0 ]; then
    echo "解壓完成：$BACKUP_DIR/$BACKUP_FILE"
else
    echo "解壓失敗，請檢查 gunzip 是否安裝或檔案是否損壞。"
    exit 1
fi

# 載入映像到 Docker
echo "正在載入映像 $BACKUP_DIR/$BACKUP_FILE..."
docker load -i "$BACKUP_DIR/$BACKUP_FILE"
if [ $? -eq 0 ]; then
    echo "映像載入完成，檢查可用映像："
    docker images
else
    echo "載入失敗，請檢查檔案是否有效。"
    exit 1
fi

# （可選）移除臨時 .tar 檔案
echo "清理臨時檔案 $BACKUP_DIR/$BACKUP_FILE..."
rm -f "$BACKUP_DIR/$BACKUP_FILE"
echo "清理完成。"