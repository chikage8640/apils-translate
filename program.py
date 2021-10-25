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
import time
import configparser

# デフォルト設定
# DeepL翻訳を使うかどうか
enableDeepl = False
# DeepLのAPIのURL
deeplApiUrl = "https://api-free.deepl.com/v2/translate"
# DeepLのAPIアクセスキー
deeplKey = ""
# サーバーのスレッド数。もし足りなかったら増やす。
waitressThreads = 6
# サーバーのホスト
host = "localhost"
# サーバーのポート
port = 50000

# GASを使った独自実装のGppgle翻訳のため、いじる必要なし。なおスクリプトの所有者である美瀬和夏以外は転用禁止とする。
gTransUrl = "https://script.google.com/macros/s/AKfycby3K3Tu1Pl1A2eEWdwKlwnJ3KtwapscfW58uYaV5DuFAqkBMlesH_kKGzrfa4XfS14g/exec"
# コードの実行されているディレクトリを取得する変数。
codePath = os.path.dirname(__file__)
# 言語判定用モデルの場所。
model = fasttext.load_model(os.path.join(codePath, "lid.176.bin"))

# 翻訳できる言語の変数。ハードコーディングなのは速度上の問題と、運用上APIから拾ってくると一部の言語が正常に使えないためである。
dTranselateSource = ["bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "hu", "it", "ja", "lt", "lv", "nl", "pl", "pt", "ro", "ru", "sk", "sl", "sv", "zh"]
dTranselateTarget = ["bg", "cs", "da", "de", "el", "en-gb", "en-us", "es", "et", "fi", "fr", "hu", "it", "ja", "lt", "lv", "nl", "pl", "pt-br", "pt-pt", "ro", "ru", "sk", "sl", "sv", "zh", "en", "pt"]
gTranselateTarget = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-cn", "zh", "zh-tw", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
aTranselateTarget = dTranselateTarget + gTranselateTarget

# boolに変換する関数。
def str2bool(s):
  return s.lower() in ["true", "t", "yes", "1"]

# config.ini関連のコード

# configの読み込みをする関数。
def loadConfig():
  config = configparser.ConfigParser()
  config.read(os.path.join(codePath, "config.ini"))
  readDeeplConfig = config["Deepl"]
  readSystemComfig = config["System"]

  # 設定値の読み込み
  global enableDeepl
  global deeplApiUrl
  global deeplKey
  global waitressThreads
  global host
  global port
  # DeepL翻訳を使うかどうか
  if readDeeplConfig["enable"] is not None:
    enableDeepl = str2bool(readDeeplConfig["enable"])
  # DeepLのAPIのURL
  if readDeeplConfig["apiUrl"] is not None:
    deeplApiUrl = readDeeplConfig["apiUrl"]
  # DeepLのAPIアクセスキー
  if readDeeplConfig["apiKey"] is not None:
    deeplKey = readDeeplConfig["apiKey"]
  # サーバーのスレッド数。もし足りなかったら増やす。
  if readSystemComfig["waitressThreads"] is not None:
    waitressThreads = int(readSystemComfig["waitressThreads"])
  # サーバーのホスト
  if readSystemComfig["host"] is not None:
    host = readSystemComfig["host"]
  # サーバーのポート
  if readSystemComfig["port"] is not None:
    port = readSystemComfig["port"]

# config読み込み
loadConfig()

# 言語判定の関数。文を入れると言語コードが返ってくる。
def detectLanguage(text):
  label, prob = model.predict(text)
  return label[0].replace("__label__", "")

# DeepL翻訳の関数。文と翻訳先の言語コードを入れると翻訳した文が返ってくる。
# なおenableDeeplの値を確認していないので、必ず呼び出す前に確認すること。
def deeplTranslate(text, targetLang):
  r = requests.post(deeplApiUrl, {"auth_key":deeplKey, "text":text, "target_lang":targetLang})
  if r.status_code == 200:
    return r.json()["translations"][0]["text"], "DeepL"
  elif r.status_code == 429 or r.status_code == 529:
    print("DeepL is busy. Retry after 3 sec.")
    time.sleep(5)
    return deeplTranslate(text, targetLang)
    

# Google翻訳の関数。文と翻訳先の言語コードを入れると翻訳した文が返ってくる。
def googleTranslate(text, targetLang):
  r = requests.post(gTransUrl, {"text":text, "target":targetLang})
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

# エラーのレスポンスを作る関数。
def make400(text):
  return make_response(jsonify({
      "states":400,
      "massage":text
    })), 400

# ここまで動けば後はポート関連のエラーだけなので、終了方法をprintしてサーバーを動かす。
print("The server has started. To stop it, press Ctrl+C.")

# リクエストを受け付ける本体
# Flaskとwaitressを使った簡易的なREST APIの実装。

api = Flask(__name__)

@api.route("/translate", methods=['GET', 'POST'])
def apiCalled():
  if request.method == "POST":
    if "text" in request.form:
      if "target" in request.form:
        text = request.form["text"]
        targetLang = request.form["target"].lower()
      else:
        return make400('"target" is not specified.')
    elif "text" in request.json:
      if "target" in request.json:
        text = request.json["text"]
        targetLang = request.json["target"].lower()
      else:
        return make400('"target" is not specified.')
    else:
      return make400('"text" is not specified.')
  else:
    if "text" in request.args:
      if "target" in request.args:
        text = request.args.get("text")
        targetLang = request.args.get("target").lower()
      else:
        return make400('"target" is not specified.')
    else:
      return make400('"text" is not specified.')

  if text == "":
    return make400('"text" is blank.')
  if targetLang == "":
    return make400('"target is blank.')

  if targetLang in aTranselateTarget:
    translation = autoTranslate(text,targetLang)
    return make_response(jsonify({
      "states":200,
      "text":translation[0],
      "translater":translation[1]
    })), 200
  else:
    return make400("Bad target was specified.")

if __name__ == "__main__":
  serve(api, host=host, port=port, threads=waitressThreads)