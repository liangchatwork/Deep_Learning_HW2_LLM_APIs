FROM nvidia/cuda:12.0.1-base-ubuntu20.04

# 更新 apt 套件庫並安裝必要的套件
RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip \
    screen \
    && rm -rf /var/lib/apt/lists/*

# 在容器中創建一個工作目錄
WORKDIR /home

# 複製 DL_HW2 資料夾到容器中的 /home/DL_HW2 目錄
COPY DL_HW2 /home/DL_HW2

# 切換到 /home/DL_HW2 目錄
WORKDIR /home/DL_HW2

# 安裝 requirement.txt 中列出的套件
RUN pip3 install -r requirement.txt
