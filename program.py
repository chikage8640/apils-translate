# Copyright (c) 2021 Chikage, Haruse.
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# coding:utf-8
import os
import requests
import fasttext
from flask import Flask, jsonify, make_response, request
from waitress import serve


# 以下の変数の値を変更し、DeepL翻訳をセットアップしてください。

# enableDeepl:DeepL翻訳を使う場合はTrue, 使わない場合はFalse。
enableDeepl = False

# deeplApiUrl:APIを呼ぶためのURL。必ずダブルクォーテーション(")で囲うこと。
# プランがフリーの場合は"https://api-free.deepl.com/v2/translate"
# プランがProの場合は"https://api.deepl.com/v2/translate"
deeplApiUrl = "https://api-free.deepl.com/v2/translate"

#deeplKey:DeepL翻訳のAPIを利用するためのAPIキー。必ずダブルクォーテーション(")で囲うこと。
deeplKey = ""



# ログ保存の確認。Trueで保存されるが、サイズが肥大化するので定期的に処理すること。
exportLog = False
# GASを使った独自実装のGppgle翻訳のため、いじる必要なし。なおスクリプトの所有者である美瀬和夏以外は転用禁止とする。
gTransUrl = "https://script.google.com/macros/s/AKfycbwNFWAn6x_wTliCl61YG_AHfhmIOC7ZqhMTYI8KNAE5S6iobkI85Ep8yaj0oXInY0bk/exec"
# コードの実行されているディレクトリを取得する変数。
codePath = os.path.dirname(__file__)
# 言語判定用モデルの場所。
model = fasttext.load_model(os.path.join(codePath, "lid.176.bin"))

# 翻訳できる言語の変数。ハードコーディングなのは速度上の問題と、運用上APIから拾ってくると一部の言語が正常に使えないためである。
dTranselateSource = ["bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "hu", "it", "ja", "lt", "lv", "nl", "pl", "pt", "ro", "ru", "sk", "sl", "sv", "zh"]
dTranselateTarget = ["bg", "cs", "da", "de", "el", "en-gb", "en-us", "es", "et", "fi", "fr", "hu", "it", "ja", "lt", "lv", "nl", "pl", "pt-br", "pt-pt", "ro", "ru", "sk", "sl", "sv", "zh", "en", "pt"]
gTranselateTarget = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-cn", "zh", "zh-tw", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
aTranselateTarget = dTranselateTarget + gTranselateTarget

# 言語判定の関数。文を入れると言語コードが返ってくる。
def detectLanguage(text):
  label, prob = model.predict(text)
  return label[0].replace("__label__", "")

# DeepL翻訳の関数。文と翻訳先の言語コードを入れると翻訳した文が返ってくる。
# なおenableDeeplの値を確認していないので、必ず呼び出す前に確認すること。
def deeplTranslate(text, targetLang):
  r = requests.get(deeplApiUrl, {"auth_key":deeplKey, "text":text, "target_lang":targetLang})
  return r.json()["translations"][0]["text"], "DeepL"

# Google翻訳の関数。文と翻訳先の言語コードを入れると翻訳した文が返ってくる。
def googleTranslate(text, targetLang):
  r = requests.get(gTransUrl, {"text":text, "target":targetLang})
  return r.json()["text"], "Google"

# 翻訳を処理する関数。文と翻訳先の言語コードを入れると翻訳した文が返ってくる。
# なおそもそも翻訳先の言語コードが正しいかは検証していないため、必ず検証してからおこなうこと。
def autoTranslate(text, targetLang):
  sourceLang = detectLanguage(text)
  if sourceLang == targetLang:
    return text, "Return"
  else:
    if enableDeepl:
      if targetLang.lower() in dTranselateTarget:
        if sourceLang in dTranselateSource:
          return deeplTranslate(text, targetLang)
        else:
          return googleTranslate(text, targetLang)
      else:
        return googleTranslate(text, targetLang)
    else:
      return googleTranslate(text, targetLang)

# ここまで動けば後はポート関連のエラーだけなので、終了方法をprintしてサーバーを動かす。
print("The server has started. To stop it, press Ctrl+C.")

# リクエストを受け付ける本体
# Flaskとwaitressを使った簡易的なREST APIの実装。

api = Flask(__name__)

@api.route("/translate", methods=['GET', 'POST'])
def apiCalled():
  if request.method == "POST":
    text = request.form["text"]
    targetLang = request.form["target"].lower()
  else:
    text = request.args.get("text")
    targetLang = request.args.get("target").lower()
  
  if targetLang in aTranselateTarget:
    translation = autoTranslate(text,targetLang)
    return make_response(jsonify({
      "states":200,
      "text":translation[0],
      "translater":translation[1]
    })), 200
  else:
    return make_response(jsonify({
      "states":400,
      "massage":"Bad target was specified."
    })), 400

if __name__ == "__main__":
  serve(api, host='localhost', port=50000)