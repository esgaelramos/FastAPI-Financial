# Deploy in Server

Its a simple guide to deploy the project in a server.

Go to the server
```bash
ssh <user>@<ip>
```

Clone the project
```bash
git clone git@github.com:esgaelramos/FastAPI-Financial.git
```

Go to the project folder
```bash
cd FastAPI-Financial
```

Create a virtual environment
```bash
python3 -m venv venv
```

Create a .env file
```bash
cp .env.example .env
```

Create the linux service
```bash
sudo nano /etc/systemd/system/financial.service
```

Add the following content
```bash
[Unit]
Description=FastApi Financial Application
After=network.target

[Service]
User=userserver
WorkingDirectory=/home/userserver/FastAPI-Financial
Environment="PATH=/home/userserver/FastAPI-Financial/env/bin"
ExecStart=/home/userserver/FastAPI-Financial/env/bin/uvicorn src.main:app --workers 4 --host 127.0.0.1 --port 8038 --app-dir /home/userserver/FastAPI-Financial/
StandardOutput=append:/var/log/financial/financial_stdout.log
StandardError=append:/var/log/financial/financial_stderr.log

Restart=always

[Install]
WantedBy=multi-user.target
```

Give permissions to the restart service without sudo
```bash
sudo nano /etc/sudoers
```

Add the following content
```bash
userserver ALL=(ALL) NOPASSWD: /bin/systemctl restart financial
```

Check the service status
```bash
sudo systemctl status financial.service
```

Enable the service
```bash
sudo systemctl enable financial.service
```

If yoy change the service file, reload the daemon
```bash
sudo systemctl daemon-reload
```

Create the log folder
```bash
sudo mkdir /var/log/financial
```

View the logs of the service
```bash 
sudo journalctl -u financial.service -f
tail -f /var/log/financial/financial_stdout.log
tail -f /var/log/financial/financial_stderr.log
```

Create the nginx configuration
```bash
sudo nano /etc/nginx/sites-available/financial.mymoneyup.tech
```

Add the following content
```bash
server {
    listen 80;
    server_name financial.mymoneyup.tech;

    access_log /var/log/nginx/financial.mymoneyup.tech.access.log;
    error_log /var/log/nginx/financial.mymoneyup.tech.error.log;

    location / {
        proxy_pass http://127.0.0.1:8038;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Create a symbolic link
```bash
sudo ln -s /etc/nginx/sites-available/financial.mymoneyup.tech /etc/nginx/sites-enabled/financial.mymoneyup.tech
```

Check the nginx configuration
```bash
sudo nginx -t
```

Restart the nginx service
```bash
sudo systemctl restart nginx
```

Check logs of the nginx service
```bash
sudo tail -f /var/log/nginx/financial.mymoneyup.tech.access.log
sudo tail -f /var/log/nginx/financial.mymoneyup.tech.error.log
```

Add ssl certificate
```bash
sudo certbot --nginx -d financial.mymoneyup.tech      
```

Go to the: https://financial.mymoneyup.tech/docs and check the api:|