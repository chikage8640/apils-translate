import sys
import os
import shutil
import urllib.error
import urllib.request
import zipfile

# ダウンロードする
def fileDownload(url,filepath):
    try:
        urllib.request.urlretrieve(url, filepath)
        return 0
    except urllib.error as e:
        print(e)
        print("Failed to download [" + url + "].")
        sys.exit()
        return 0

# 必要なビルドツールがあるかの確認
if os.path.exists("C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC") == False:
    print("C++ build tool is not installed. Please install Microsoft C++ Build Tools.\nhttps://visualstudio.microsoft.com/ja/visual-cpp-build-tools/")
    sys.exit()
 
# 保存先ディレクトリ作成
tempPath = "./temp/"
if os.path.exists(tempPath):
    # 既にある場合は、先に丸ごと削除する
    shutil.rmtree(tempPath)
 
os.mkdir(tempPath)

print("Start setup...")

# 必要なファイルのダウンロード
print("Downloading lid.176.bin...")
fileDownload("https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin", "./lid.176.bin")
print("Downloading runtime...")
fileDownload("https://www.python.org/ftp/python/3.9.7/python-3.9.7-embed-amd64.zip", tempPath + "runtime.zip")

# runtimeの解凍
print("Unzipping runtime...")
with zipfile.ZipFile(tempPath + "runtime.zip") as f:
    f.extractall('./runtime')

# さらにその中にfasttextをクローン
print("Downloading fasttext...")
fileDownload("https://github.com/facebookresearch/fastText/archive/refs/heads/master.zip", tempPath + "fasttext.zip")
print("Unzipping fasttext...")
with zipfile.ZipFile(tempPath + "fasttext.zip") as f:
    f.extractall(tempPath + "fasttext")

# runtimeでpipを使えるようにする
print("Downloading get-pip.py...")
fileDownload("https://bootstrap.pypa.io/get-pip.py", tempPath + "get-pip.py")

with open("./runtime/python39._pth", "a") as f:
    f.write("import site")

# バッチに投げる
print("Calling setruntime.bat...")
os.system(".\\setruntime.bat " + sys.exec_prefix)

# 作業フォルダ削除
shutil.rmtree(tempPath)