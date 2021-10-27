# apils-translate
Set up a local server to provide the translation API.  
This API can use Google Translate and DeepL Translator(Configuration is required).

# Translated README
Japanese - [README_JP.md](https://github.com/chikage8640/apils-translate/blob/main/docments/README_JP.md)

# Getting Started
## Install
Download [release file](https://github.com/chikage8640/apils-translate/releases) and unzip.

## Setup DeepL Translater
Edit `config.ini`

```ini:config.ini
;Change the values of the following variables to set up the DeepL translation.
[Deepl]

;True if the DeepL translation is used, false if it is not.
enable = True

;The URL to call the API.
;If the plan is free "https://api-free.deepl.com/v2/translate"
;If the plan is pro "https://api.deepl.com/v2/translate"
apiUrl = https://api-free.deepl.com/v2/translate

;API key for using the DeepL translation API.
apiKey = yourApiKey


[System]
waitressThreads = 6
host = localhost
port = 50000
```


## Start server
Run `run.bat`

## Translate
Call it as a REST API, either GET or POST is fine. The return value is JSON.  
The following is an example.

```
> curl "http://localhost:50000/translate" -d "text=Hello world!" -d "target=de"
{"states":200,"text":"Hallo Welt!","translater":"DeepL"}
```
To test in your browser, go to the following link.  
http://localhost:50000/translate?text=Hello+world!&target=de  
You will see a JSON text like the following.  
```
{"states":200,"text":"Hallo Welt!","translater":"DeepL"}
```
## Stop server
Press Ctrl+C or kill task. (You can also close the console window directly.)

# API
## URL
`http://localhost:50000/translate`
## Paramaters
| Name | Description | Example |
| ---- | ---- | ---- |
| `text` | Text to be translated | Hello World! |
| `target` | Language code to translate to | de |
## Return value
| Name | Description | Example |
| ---- | ---- | ---- |
| `states` | States code | 200<br/>400 |
| `text` | Translated text | Hallo Welt! |
| `massage` | Details of errors, etc. | Bad target was specified. |
| `translater` | The engine that did the translation<br/>(If no translation was done, "Return" will be returned.) | Google<br/>DeepL<br/>Return

# System requirements
This application require the folllowing system to run.
- Windows 10 x64 

# Development
In addition to the system requirements, the following environment is required:
- Python 3.9(.7)
- Microsoft C++ Build Tools

After cloning the repository, run setup.bat.

If you want to use this on another system, you may have to rewrite the batch files to make it work. (No guarantees!)

# Auther
[Chikage, Haruse](https://github.com/chikage8640)

# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/chikage8640/apils-translate/blob/main/LICENSE) file for details