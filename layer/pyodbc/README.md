## DBアクセス用のLambda Layer作成手順
1. このREADMEがある階層をカレントディレクトリとする
2. 下記実行ファイルを起動する
```
.\creaet-layer.bat

# 実行時、下記のエラーが出力される可能性がありますが、無視して頂いて問題ありません。
# Error: No such container: pyodbc-container
```
3. カレントディレクトリに出力された`lambda-layer.zip`を確認し、下記Lambda Layerの作成手順に従ってアップロードする
   - https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/configuration-layers.html#configuration-layers-create
   - ※ `互換性のある命令セットアーキテクチャ`は`3.8`を指定してください
## 参考サイト
- pyodbcのコンパイルについて
- https://github.com/naingaungphyo/lambda_pyodbc_laycder-python3.8