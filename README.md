# Multi Shop Project
This is a e-commerce shop with Django


1. Have Login and Register with OTP.
2. Dockerized.
3. Compliance with the principles of clean coding.

## Run project
- In terminal: `git clone https://github.com/abolfazlz15/MultiShopDjangoProject.git`
- cd `/MultiShopDjangoProject` Where the docker-compose.yaml is
- In terminal: `python -m venv venv`
- activate your venv: in windows `cd venv\scripts\activate` in linux: `venv/bin/activate`
- Run `pip install requirements.txt`
- Run `python manage.py collectstatic`
- Run `python manage.py runserver`

## Run project with docker
make sure you`ve installed docker
- In terminal: `git clone https://github.com/abolfazlz15/MultiShopDjangoProject.git`
- cd `/MultiShopDjangoProject` Where the docker-compose.yaml is
- In terminal: `docker-compose up -d`
- Visit http://0.0.0.0:8000/ 