# Homework status bot.

## Описание.
Учебный проект. Телеграм бот, который через API получает обновления статусов код-ревью заданий. При наличии обновлений отправляет соответствующее статусу сообщение.

## Установка и запуск.
Для локального запуска склонировать репозиторий и установить зависимости:
```
pip install requirements.txt
```
В корне проекта создать файл .env, в котором следует указать PRAKTIKUM_TOKEN (токен для доступа к Яндекс Практикуму), TELEGRAM_TOKEN (токен для тоступа к телеграм боту), TELEGRAM_CHAT_ID (id чата, в который бот должен присылать сообщения). Например:
```
PRAKTIKUM_TOKEN=abcABCabcABCbabABAbaABbABCabcabABCbabcAbaABcbA
TELEGRAM_TOKEN=1234567890:ABC12AbCAbCabcabCA1bCABc1ABCaABcAbc
TELEGRAM_CHAT_ID=112233445
```
Запустить файл homework.py:
```
python homework.py
```
