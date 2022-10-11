1. Установить mongodb
2. + рекомендую MongoDB Compass для администрирования бд
3. Нужен `python 3.10`
4. Установка nginx
```
sudo apt update
sudo apt install nginx
```


1. cd /home
2. git clone https://github.com/achillescres/izfir_bot.git
3. cd izfir_bot
4. python -m venv venv
5. source ./venv/bin/activate
6. pip install -r requirements.txt



1. sudo nano .env (В DEV MODE писать FALSE)!!!
```
DEV_MODE=False 
BOT_TOKEN=*токен бота*
HOST_URL=https://*ваш ip или домен*
ACCESS_TOKEN=TXDMjyByxGD5apdySV235Q
SERVER_URL=http://127.0.0.1:8000
DEFAULT_RATE_LIMIT=0.75
DEFAULT_SPAM_STUN=4
```

2. sudo nano /etc/nginx/sites-available/izfir_bot
```
server {
    server_name *ip*(или)*domen* www.*domen*;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8001(или)*выбранный вами порт*;
    }
}
```
3. sudo ln -s /etc/nginx/sites-available/izfir_bot /etc/nginx/sites-enabled/
4. sudo nginx -t
5. Вывод должен быть примерно таким:
```commandline
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
5. sudo systemctl reload nginx
6. sudo apt install -y certbot python3-certbot-nginx
7. sudo certbot --nginx -d your_domain -d www.your_domain
8. https://your_domain проверить есть ли ssl
9. sudo certbot renew --dry-run
10. cd /home/izfir_bot
11. /home/demo/fastapi_demo/venv/bin/gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app -b 127.0.0.1:8000
Все.~~
