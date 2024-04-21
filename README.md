# QActf Backend
Проект занимающийся обучением и тестированием QA engineers.


# Стек технологий:

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/redis-CC0000.svg?&style=for-the-badge&logo=redis&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

![image](https://img.shields.io/badge/sql%20alchemy-grey?style=for-the-badge&logo=alchemy)
![image](https://img.shields.io/badge/alembic-7FFFD4?style=for-the-badge)
![image](https://img.shields.io/badge/pydantic-FF1493?style=for-the-badge&logo=pydantic)


## **Как запустить проект**:

- Склонируйте репозитарий:
```
git clone git@github.com:QActf/backend.git
```

- Установите Docker согласно инструкции с официального сайта: _https://docs.docker.com/_

- В папке infra/ создайте файл .env c переменными окружения (в качестве примера можно взять .env.examle):

```
# infra/.env

# DataBase
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=MocSecret

# Admin
FIRST_SUPERUSER_EMAIL=test@t.t
FIRST_SUPERUSER_PASSWORD=123

```

* Создайте и запустите docker контейнеры:

Локальная сборка контейнеров:
```
# Linux
sudo docker compose --file=docker-compose.yml up --build -d
```

Либо, если у вас еще не установлен докер, можно запустить командой:
```
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Документация будет доступна по http://127.0.0.1/docs/

## Разработчики 

-----

 - [Семён Новиков](https://github.com/Sovraska)

 - [Дмитрий Абрамов](https://github.com/D-Abramoc)

 - [Ильгиз Галлямов](https://github.com/ilgiz-tat)

 - [Иван Кудьяров](https://github.com/LicrimoVor)

 - [Илона Петина](https://github.com/ilonka05)

 - [Сафонов Сергей](https://github.com/SerVik888)

 - [Вячеслав Мельник](https://github.com/dmsvalik)

 - Андрей Легкий

 - [Дарья Илий](https://github.com/DariaEaly)

 - [Глеб Кондратьев](https://github.com/gleb60)
----


