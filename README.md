# eigo-of-the-day-django

Memo App for Instagram Account eigo.of.the.day

---

[TOC]

## Note

- Currently not using package `martor`, but installed and configured.

## docker-compose.yml

```yaml
version: "3"

services:
    app:
        build: .
        environment:
            ENVIRONMENT: development
            SECRET_KEY: <secret_key>
            DEBUG: 1
            CLOUDINARY_NAME: <cloudinary_name>
            CLOUDINARY_API_KEY: <cloudinary_public_api_key>
            CLOUDINARY_API_SECRET: <cloudinary_secret_api_key>
        volumes:
            - .:/app
        ports:
            - 8000:8000
        depends_on: db
    db:
        image: postgres:11
        volumes:
            - postgres_data:/var/lib/postgresql/data/
        environment:
            - "POSTGRES_HOST_AUTH_METHOD=trust"

volumes:
    postgres_data:
```

## deploy

This project is uploaded to Heroku.
