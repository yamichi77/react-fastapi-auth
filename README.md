# React-FastAPI-Auth

## 概要

フロントに React+TypeScript、バックエンドに FastAPI を使用した際の Keycloak を使用した認可・認証のサンプルコードリポジトリになります。

## 使用方法

### 起動方法

1. 次のコマンドで Docker を起動します。  
   `docker compose up -d`
2. docker 起動後、下記 url で keycloak が起動します。適切に設定をしてください。（初期ユーザー：admin、パスワード：admin）
   `http://localhost:8080`
3. 一旦 Docker を落とし、設定したものを FastAPI の環境変数へ入れてください

   | 環境変数         | 説明                  |
   | ---------------- | --------------------- |
   | KC_REALM_NAME    | レルム名              |
   | KC_CLIENT_ID     | クライアント ID       |
   | KC_CLIENT_SECRET | クライアントの SECRET |

4. Docker の再度起動後、下記 url にアクセスします。  
   `http://localhost`

## ボタン説明

| ボタン                  | 説明                                                                                           |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| Submit to Login         | Keycloak へリダイレクトし、ログインします。                                                    |
| Submit to Token Refresh | トークンをリフレッシュトークンで更新します。                                                   |
| Submit to Valid Token   | トークンチェックおよび、ユーザーの内容を表示します。                                           |
| Submit to Request       | FastAPI の REST での使用テストです。Token のチェックを行い、正常なら Hello, World!を返します。 |
