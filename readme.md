# Devman API bot
The purpose of this bot is to check the devman API and send updates via telegram on reviews in progress.

## Required env vars
In order the script to work please create `.env` file and specify these env vars:  
`DEVMAN_TOKEN`  
`DEVMAN_URL`  
`TELEGRAM_TOKEN`  
`TG_CHAT_ID`

## Installation
1. Clone `git clone ...`
2. Install venv `python3 -m venv venv`
3. Activate venv `source venv/bin/python`
4. Install dependencies `pip install -r requirements.txt`
5. Create `.env` file in the project root directory and enter the env vars
6. Run the script 
   * `python3 main.py`

## Running the app in a docker container
* build image from the Dockerfile
```shell
docker build -t <prefered_name> .
```
* run the image and mount the `.env` file to it
```shell
docker run -it -v $(pwd)/.env:/app/.env <chosen_image_name>
```