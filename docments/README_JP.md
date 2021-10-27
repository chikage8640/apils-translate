# apils-translate
翻訳APIを提供するサーバーをローカルに立てます。  
このAPIではGoogle翻訳とDeepL翻訳（設定が必要です）が併用可能です。  

# スタートアップ
## インストール
[リリースファイル](https://github.com/chikage8640/apils-translate/releases)をダウンロードし、解凍してください。

## DeepL翻訳の設定
`config.ini`を編集してください。

```ini:config.ini
;以下の値を変更して、DeepL翻訳の設定をします。
[Deepl]

;DeepL翻訳を使う場合はTrue、使わない場合はFalse
enable = True

;APIを呼ぶときに使うURL
;フリープランの場合 "https://api-free.deepl.com/v2/translate"
;プロプランの場合 "https://api.deepl.com/v2/translate"
apiUrl = https://api-free.deepl.com/v2/translate

;DeepL translation APIを使うためのAPIキー
apiKey = yourApiKey


[System]
waitressThreads = 6
host = localhost
port = 50000
```


## サーバーのスタート
`run.bat`を実行してください。

## 翻訳
このAPIはREST APIとして、GETやPOSTで呼ぶことができます。戻り値はJSONで返されます。  
以下は呼び出しの例です。  

```
> curl "http://localhost:50000/translate" -d "text=Hello world!" -d "target=de"
{"states":200,"text":"Hallo Welt!","translater":"DeepL"}
```

ブラウザでテストする場合には以下のリンクへアクセスしてください。  
http://localhost:50000/translate?text=Hello+world!&target=de  
以下のようなJSONテキストが表示されます。  
```
{"states":200,"text":"Hallo Welt!","translater":"DeepL"}
```

## サーバーの停止
Ctrl+Cを入力することで止まります。（コンソールウィンドウをを直接閉じてもかまいません。）

# API
## URL
`http://localhost:50000/translate`
## パラメーター
| 名前 | 説明| 例 |
| ---- | ---- | ---- |
| `text` | 翻訳するテキスト | Hello World! |
| `target` | 翻訳先の言語 | de |
## 戻り値
| 名前 | 説明 | 例 |
| ---- | ---- | ---- |
| `states` | ステータスコード | 200<br/>400 |
| `text` | 翻訳されたテキスト | Hallo Welt! |
| `massage` | エラーなどの詳細 | Bad target was specified. |
| `translater` | 翻訳に使用したエンジン<br/>(翻訳をせずに返した場合は「Return」が返されます。) | Google<br/>DeepL<br/>Return

# 動作環境
このアプリケーションは以下の環境を要求します。
- Windows 10 x64 

# 開発環境
システム要件に加え、以下の環境が必要です。
- Python 3.9(.7)
- Microsoft C++ Build Tools

リポジトリをクローンしたのち、setup.batを実行してください。  

バッチファイルを書き換えれば他のシステムでも動くかもしれません。（保証はしません！）

# Auther
[美瀬 和夏](https://github.com/chikage8640)

# License
このプロジェクトは、MITライセンスの下でライセンスされています。詳細は[LICENSE](https://github.com/chikage8640/apils-translate/blob/main/LICENSE)ファイルを参照してください。