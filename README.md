# React-FastAPI-Auth

## 概要

フロントにReact+TypeScript、バックエンドにFastAPIを使用した際のKeycloakを使用した認可・認証のサンプルコードリポジトリになります。

## 使用方法

### 起動方法

1. 次のコマンドで Docker を起動します。  
   `docker compose up -d`
2. docker 起動後、下記 url でkeycloakが起動します。適切に設定をしてください。（初期ユーザー：admin、パスワード：admin）
   `http://localhost:8080`
3. 一旦Dockerを落とし、設定したものをFastAPIの環境変数へ入れてください
   | 環境変数 | 説明 |
   | --------| ----- |
   | KC_REALM_NAME | レルム名 |
   | KC_CLIENT_ID | クライアントID |
   | KC_CLIENT_SECRET | クライアントのSECRET |
4. Dockerの再度起動後、下記 url にアクセスします。  
   `http://localhost`

## ボタン説明

| ボタン | 説明 |
| --------| ----- |
| Submit to Login | Keycloakへリダイレクトし、ログインします。 |
| Submit to Token Refresh | トークンをリフレッシュトークンで更新します。 |
| Submit to Valid Token | トークンチェックおよび、ユーザーの内容を表示します。 |
| Submit to Request | FastAPIのRESTでの使用テストです。Tokenのチェックを行い、正常ならHello, World!を返します。 |
