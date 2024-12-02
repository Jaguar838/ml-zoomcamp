## 5.6 Управління середовищем: Docker

<a href="https://www.youtube.com/watch?v=wAtyYZ6zvAs&list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR"><img src="images/thumbnail-5-06.jpg"></a>

[Слайди](https://www.slideshare.net/AlexeyGrigorev/ml-zoomcamp-5-model-deployment)

## Встановлення Docker

Щоб ще більше ізолювати наш проєкт від системи, можна скористатися Docker. Docker дозволяє упакувати весь проєкт у контейнер з необхідною системою та запускати його на будь-якому пристрої. Наприклад, ви можете використовувати Ubuntu 20.4 на комп'ютері з macOS, Windows або іншою операційною системою. <br>
Щоб почати використовувати Docker для проєкту прогнозування відтоку, скористайтеся інструкціями нижче.

### Ubuntu

```bash
sudo apt-get install docker.io
```

Щоб запускати Docker без `sudo`, дотримуйтесь [цих інструкцій](https://docs.docker.com/engine/install/linux-postinstall/).

### Windows

Щоб встановити Docker, скористайтесь інструкціями від Ендрю Лока за цим посиланням: https://andrewlock.net/installing-docker-desktop-for-windows/

### MacOS

Слідкуйте за кроками в [документації Docker](https://docs.docker.com/desktop/install/mac-install/).

## Нотатки

- Коли проєкт упакований у Docker-контейнер, його можна запускати на будь-якому пристрої.
- Спершу необхідно створити образ Docker. Файл образу Docker містить налаштування та залежності нашого проєкту. Щоб знайти необхідні Docker-образи, можна просто здійснити пошук на [сайті Docker](https://hub.docker.com/search?type=image).

Ось приклад Dockerfile (Коментарі в Dockerfile бути не повинні, тому видаліть їх, коли копіюєте):

```docker
# Спочатку встановлюємо Python 3.8, slim-версія займає менше місця
FROM python:3.8.12-slim

# Встановлюємо бібліотеку pipenv в Docker
RUN pip install pipenv

# Створюємо в Docker каталог app і використовуємо його як робочий каталог
WORKDIR /app                                                                

# Копіюємо Pip-файли в наш робочий каталог
COPY ["Pipfile", "Pipfile.lock", "./"]

# Встановлюємо залежності pipenv для проєкту і розгортаємо їх
RUN pipenv install --deploy --system

# Копіюємо всі Python-файли та модель у робочий каталог Docker
COPY ["*.py", "churn-model.bin", "./"]

# Відкриваємо порт 9696 для зв'язку з Docker
EXPOSE 9696

# При запуску образу Docker запускаємо наш додаток для прогнозування відтоку
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "churn_serving:app"]
```

Флаги `--deploy` і `--system` гарантують, що ми встановлюємо залежності безпосередньо всередині Docker-контейнера без створення додаткового віртуального середовища (за замовчуванням це робить pipenv).

Якщо не додати останній рядок `ENTRYPOINT`, ви опинитесь у Python-терміналі.
Зверніть увагу, що для entrypoint ми записуємо команди в подвійних лапках.

Після створення Dockerfile, потрібно побудувати його:

```bash
docker build -t churn-prediction .
```

Щоб запустити, виконайте команду нижче:

```bash
docker run -it -p 9696:9696 churn-prediction:latest
```

Пояснення прапорців:

- `-t`: використовується для задання імені мітки "churn-prediction".
- `-it`: щоб Docker дозволив нам доступ до терміналу.
- `--rm`: дозволяє видалити образ із системи після завершення.
- `-p`: для прив'язки порту 9696 Docker до порту 9696 нашого пристрою (перший 9696 — це порт на нашому пристрої, другий — порт контейнера Docker).
- `--entrypoint=bash`: після запуску Docker ми зможемо взаємодіяти з контейнером за допомогою bash (як зазвичай у терміналі). За замовчуванням `python`.

Вітаємо 🎉 Ви розгорнули свій додаток для прогнозування всередині контейнера Docker.

<table>
   <tr>
      <td>⚠️</td>
      <td>
         Ці нотатки написані спільнотою. <br>
         Якщо ви помітили помилку, створіть PR для виправлення.
      </td>
   </tr>
</table>

* [Нотатки від Peter Ernicke](https://knowmledge.com/2023/10/14/ml-zoomcamp-2023-deploying-machine-learning-models-part-6/)

## Навігація

* [Курс Machine Learning Zoomcamp](../)
* [Сесія 5: Розгортання моделей машинного навчання](./)
* Попередня: [Віртуальне середовище Python: Pipenv](05-pipenv.md)
* Наступна: [Розгортання в хмарі: AWS Elastic Beanstalk (необов’язково)](07-aws-eb.md)
