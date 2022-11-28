# 各種ツールバージョン、設定について
#### 後述する手順は下記がインストール済み、設定済みであることを前提としています。
| ツール | バージョン | 備考 |
| ---- | ---- | ----|
| Node.js | 16.13.0 |Serverless Framework用 |
| npm | 8.1.0 | Serverless Framework用 |
| Python | 3.8.10 | Lambdaコード用 |
| pip | 21.1.2 | Lambdaコード用 |
| aws cli | 指定なし | デプロイ向けS3作成用 |

# 開発環境構築
1. このREADMEがある階層をカレントディレクトリとします。
2. Serverless Framework関連のライブラリをインストール  
※ 初回、もしくはpackage.jsonに変更が入った時に適宜実施
```
npm install
```
3. Lambda用Pythonアプリの依存ライブラリをインストール  
※ 初回、もしくはrequirements.txtに変更が入った時に適宜実施
```
pip install -r requirements.txt
```

# Serverless Frameworkのステージ一覧
| ステージ | AWS Profile | 備考 |
| ---- |-------------| ----|
| local | gxp-local   | 作業者のローカル動作確認用 |

# AWSの認証設定(動作確認とデプロイのための準備)
### ローカル動作確認用（値はダミーで良い）
```
aws configure --profile gxp-local
AWS Access Key ID [None]: XXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXXXXX
Default region name [None]: ap-northeast-1
Default output format [None]: json
```
### AWSデプロイ用
```
aws configure --profile gxp-stg
AWS Access Key ID [None]: ${IAMユーザーのアクセスキー}
AWS Secret Access Key [None]: ${IAMユーザーのシークレットキー}
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

# 動作確認とデプロイ
#### ローカル動作確認(Flaskアプリとして起動)
```
serverless wsgi serve --stage local
```
#### AWS環境へデプロイ
1. [pyodbc用のLambda Layer](./layer/pyodbc)がデプロイ済みであること
2. [ステージ毎の依存情報](./conf)を設定済みであること(設定済みの場合は実施不要)
3. Lambdaデプロイ用のバケット作成（作成済みの場合は実施不要）
4. [OpenAPIの定義ファイル](./etc/openapi/openapi.yaml)の`servers`をコメントアウトしておくこと
```
aws s3 mb s3://gxp-stg-lambda-deployment-bucket --profile gxp-stg
```
4. ステージを指定してデプロイ
```
serverless deploy --stage stg
```

# 成果物作成
### ソースコードまとめ
```
git archive HEAD --output=pyodbc-sample.zip
```
### OpenAPI仕様書生成
```
redoc-cli bundle etc/openapi/openapi.yaml -o openapi.html
```
