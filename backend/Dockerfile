# ベースイメージとしてPyTorchとCUDAがインストールされたものを使用
FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-runtime 

# インタラクティブなインストールプロンプトを無効化
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-opencv \
    tzdata \
    && apt-get clean

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY api /app/api
COPY api/models /app/models

# FastAPIサーバーを起動
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
