### Домашнє завдання

> Примітка: іноді ваша відповідь не повністю збігається з одним із варіантів. Це нормально. Виберіть варіант, який найближчий до вашого рішення.

> Примітка: для цього завдання ми рекомендуємо використовувати python 3.11.

У цьому завданні ми будемо використовувати набір даних Bank Marketing. Завантажте його [тут](https://archive.ics.uci.edu/static/public/222/bank+marketing.zip).

Ви можете зробити це за допомогою `wget`:

```bash
wget https://archive.ics.uci.edu/static/public/222/bank+marketing.zip
unzip bank+marketing.zip 
unzip bank.zip
```

Нам потрібен файл `bank-full.csv`.

Ви також можете отримати копію `bank-full.csv` безпосередньо:

```bash
wget https://github.com/alexeygrigorev/datasets/raw/refs/heads/master/bank-full.csv
```

## Запитання 1

* Встановіть Pipenv
* Яка версія pipenv встановлена?
* Використовуйте `--version`, щоб дізнатись

## Запитання 2

* Встановіть за допомогою Pipenv версію Scikit-Learn 1.5.2
* Який перший хеш для scikit-learn у Pipfile.lock?

> **Примітка**: створіть порожню папку для домашнього завдання і виконайте всі дії в ній.

## Моделі

Ми підготували словниковий векторизатор та модель.

Вони були навчені (орієнтовно) за допомогою цього коду:

```python
features = ['job', 'duration', 'poutcome']
dicts = df[features].to_dict(orient='records')

dv = DictVectorizer(sparse=False)
X = dv.fit_transform(dicts)

model = LogisticRegression().fit(X, y)
```

> **Примітка**: Вам не потрібно тренувати модель. Цей код надано лише для ознайомлення.

Потім вони були збережені з використанням Pickle. Завантажте їх:

* [DictVectorizer](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/master/cohorts/2024/05-deployment/homework/dv.bin?raw=true)
* [LogisticRegression](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/master/cohorts/2024/05-deployment/homework/model1.bin?raw=true)

За допомогою `wget`:

```bash
PREFIX=https://raw.githubusercontent.com/DataTalksClub/machine-learning-zoomcamp/master/cohorts/2024/05-deployment/homework
wget $PREFIX/model1.bin
wget $PREFIX/dv.bin
```

## Запитання 3

Давайте використаємо ці моделі!

* Напишіть скрипт для завантаження цих моделей з використанням pickle
* Оцініть цього клієнта:

```json
{"job": "management", "duration": 400, "poutcome": "success"}
```

Яка ймовірність того, що цей клієнт оформить підписку?

* 0.359
* 0.559
* 0.759
* 0.959

Якщо у вас виникають помилки при завантаженні файлів з pickle, перевірте їх контрольну суму:

```bash
$ md5sum model1.bin dv.bin
3d8bb28974e55edefa000fe38fd3ed12  model1.bin
7d37616e00aa80f2152b8b0511fc2dff  dv.bin
```

## Запитання 4

Тепер створимо веб-сервіс для цієї моделі

* Встановіть Flask та gunicorn (або waitress, якщо ви працюєте на Windows)
* Напишіть код Flask для надання доступу до моделі
* Оцініть цього клієнта за допомогою `requests`:

```python
url = "YOUR_URL"
client = {"job": "student", "duration": 280, "poutcome": "failure"}
requests.post(url, json=client).json()
```

Яка ймовірність того, що цей клієнт оформить підписку?

* 0.335
* 0.535
* 0.735
* 0.935

## Docker

Встановіть [Docker](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/master/05-deployment/06-docker.md). Ми будемо використовувати його для наступних двох запитань.

Для цих запитань ми підготували базовий образ: `svizor/zoomcamp-model:3.11.5-slim`. Вам потрібно буде його використовувати (див. Приклад у Запитанні 5).

Цей образ базується на `python:3.11.5-slim` і містить модель логістичної регресії (іншу) та словниковий векторизатор.

Ось як виглядає Dockerfile для цього образу:

```docker
FROM python:3.11.5-slim
WORKDIR /app
COPY ["model2.bin", "dv.bin", "./"]
```

Ми вже створили цей образ і завантажили його в [`svizor/zoomcamp-model:3.11.5-slim`](https://hub.docker.com/r/svizor/zoomcamp-model).

> **Примітка**: Вам не потрібно створювати цей docker-образ, він наведений лише для ознайомлення.

## Запитання 5

Завантажте базовий образ `svizor/zoomcamp-model:3.11.5-slim`. Ви можете зробити це за допомогою команди [docker pull](https://docs.docker.com/engine/reference/commandline/pull/).

Отже, який розмір цього базового образу?

* 45 MB
* 130 MB
* 245 MB
* 330 MB

Цю інформацію можна отримати, запустивши команду `docker images` - вона буде в колонці "SIZE".

## Dockerfile

Тепер створіть свій Dockerfile на основі підготовленого нами образу.

Він має починатися так:

```docker
FROM svizor/zoomcamp-model:3.11.5-slim
# add your stuff here
```

Тепер завершіть його:

* Встановіть усі залежності з файлу Pipenv
* Скопіюйте свій Flask скрипт
* Запустіть його за допомогою Gunicorn

Після цього ви можете створити свій docker-образ.

## Запитання 6

Запустимо ваш docker-контейнер!

Після запуску, оцініть цього клієнта ще раз:

```python
url = "YOUR_URL"
client = {"job": "management", "duration": 400, "poutcome": "success"}
requests.post(url, json=client).json()
```

Яка ймовірність того, що цей клієнт оформить підписку зараз?

* 0.287
* 0.530
* 0.757
* 0.960

## Надішліть результати

* Надішліть ваші результати тут: https://courses.datatalks.club/ml-zoomcamp-2024/homework/hw05
* Якщо ваша відповідь не точно збігається з варіантами, виберіть найближчий