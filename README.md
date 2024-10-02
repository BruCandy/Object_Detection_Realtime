# Object_Detection_Realtime

## セットアップ手順

### フロントエンドのセットアップ

1. ターミナルでプロジェクトのフロントエンドディレクトリに移動します。

    ```bash
    cd frontend
    ```

2. 依存関係をインストールします。

    ```bash
    yarn install
    ```

### バックエンドのセットアップ

1. ターミナルでプロジェクトのバックエンドディレクトリに移動します。

    ```bash
    cd backend
    ```

2. 仮想環境を作成します。

    ```bash
    python3 -m venv venv
    ```

3. 仮想環境を有効化します。
    
   ```bash
    venv\Scripts\activate
   ```

4. 依存関係をインストールします。

    ```bash
    pip install -r requirements.txt
    ```

5. 物体検出api(GPU使用)の準備をします。docker imageを作ります。

    ```bash
    docker build -t <docker image名> .
    ```


### サービスの開始


1. フロントエンド開発サーバーを起動します。

    ```bash
    cd frontend
    yarn dev
    ```

2. 一つ目のapiを起動します。

    ```bash
    cd backend
    uvicorn capture.capture:app --port 8001 --reload 
    ```

3. 二つ目のapiを起動します。

    ```bash
    docker run --gpus all -it --rm -p 8000:8000 <docker image名>
    ```

## アクセス

- フロントエンド: [http://localhost:5173](http://localhost:5173)
- バックエンド1: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- バックエンド2: [http://127.0.0.1:8001](http://127.0.0.1:8001)

