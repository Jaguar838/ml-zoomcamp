## Домашнє завдання

У цьому завданні ми розгорнемо модель **Bank Marketing** з домашнього завдання №5.  
У нас вже є Docker-образ для цієї моделі – ми використаємо його для  
розгортання моделі у **Kubernetes**.

---

## Створення образу

Клонуйте репозиторій курсу, якщо ви ще цього не зробили:

```
git clone https://github.com/DataTalksClub/machine-learning-zoomcamp.git
```

Перейдіть у папку `course-zoomcamp/cohorts/2024/05-deployment/homework`  
і виконайте наступну команду:

```bash
docker build -t zoomcamp-model:3.11.5-hw10 .
```

> **Примітка:** Якщо виникли проблеми зі збіркою образу, ви можете  
> скористатися образом, який ми зібрали і опублікували на **Docker Hub**:  
> `docker pull svizor/zoomcamp-model:3.11.5-hw10`

---

## Питання 1

Запустіть його для локального тестування:

```bash
docker run -it --rm -p 9696:9696 svizor/zoomcamp-model:3.11.5-hw10
```

В іншому терміналі виконайте файл `q6_test.py`:

```bash
python q6_test.py
```

Ви побачите таке:

```python
{'has_subscribed': True, 'has_subscribed_probability': <value>} # 0.756743795240796
```

Тут `<value>` – це ймовірність підписки. Оберіть правильне значення:

* 0.287
* 0.530
* **0.757**
* 0.960

Тепер можна зупинити контейнер у Docker.

---

## Встановлення `kubectl` та `kind`

Вам потрібно встановити:

- `kubectl` - [Інструкція](https://kubernetes.io/docs/tasks/tools/) (перевірте наявність перед встановленням).
- `kind` - [Інструкція](https://kind.sigs.k8s.io/docs/user/quick-start/).

---

## Питання 2

Яка версія **kind** у вас встановлена?

Використайте команду:

```bash
kind --version
```

---

## Створення кластера

Тепер створимо кластер за допомогою **kind**:

```bash
kind create cluster
```

Перевірте створення за допомогою команди:

```bash
kubectl cluster-info
```

---

## Питання 3

Яка найменша обчислювальна одиниця, яку можна створити та керувати  
в Kubernetes (у нашому випадку через **kind**)?

* Node
* **Pod**
* Deployment
* Service

---

## Питання 4

Перевірте список запущених сервісів через **kubectl**.

Який `Type` має сервіс, що вже працює?

* NodePort
* **ClusterIP**
* ExternalName
* LoadBalancer

---

## Питання 5

Щоб використовувати Docker-образ `zoomcamp-model:3.11.5-hw10`,  
його потрібно зареєструвати у **kind**.

Яка команда для цього використовується?

* `kind create cluster`
* `kind build node-image`
* **kind load docker-image**
* `kubectl apply`

---

## Питання 6

Створимо конфігурацію для розгортання (`deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subscription
spec:
  selector:
    matchLabels:
      app: subscription
  replicas: 1
  template:
    metadata:
      labels:
        app: subscription
    spec:
      containers:
      - name: subscription
        image: <Image>
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"            
          limits:
            memory: <Memory>
            cpu: <CPU>
        ports:
        - containerPort: <Port>
```

Замість `<Image>`, `<Memory>`, `<CPU>`, `<Port>` підставте правильні значення.

Яке значення потрібно підставити для `<Port>`?

---

## Питання 7

Створимо сервіс для нашого розгортання (`service.yaml`):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: subscription
spec:
  type: LoadBalancer
  selector:
    app: subscription <???>
  ports:
  - port: 80
    targetPort: 9696
```

Що потрібно написати замість `<???>`?

---

## Тестування сервісу

Тестуємо сервіс локально, перенаправивши порт **9696** на **80** у сервісі:

```bash
kubectl port-forward service/<Service name> 9696:80
```

Запустіть `q6_test.py` ще раз для перевірки роботи. Результат має співпадати  
з результатом у **Питанні 1**.

---

## Автомасштабування

Тепер використаємо **HorizontalPodAutoscaler** (HPA) для автоматичного масштабування:

```bash
kubectl autoscale deployment subscription --name subscription-hpa --cpu-percent=20 --min=1 --max=3
```

Перевірте статус HPA:

```bash
kubectl get hpa
```

---

## Збільшення навантаження

Для тестування реакції HPA на навантаження змініть скрипт `q6_test.py`, додавши цикл:

```python
while True:
    sleep(0.1)
    response = requests.post(url, json=client).json()
    print(response)
```

Запустіть скрипт.

---

## Питання 7 (опціонально)

Запустіть команду для моніторингу HPA:

```bash
kubectl get hpa subscription-hpa --watch
```

Яка максимальна кількість реплік була створена?

* 1
* 2
* 3
* 4

---

## Надсилання результатів

* Надішліть відповіді сюди: [https://courses.datatalks.club/ml-zoomcamp-2024/homework/hw10](https://courses.datatalks.club/ml-zoomcamp-2024/homework/hw10).
* Якщо ваша відповідь не повністю збігається з варіантами, виберіть найближчу.

---

## Дедлайн

Дедлайн: **21 грудня 2024 року (вівторок), 23:00 CET (час Берліна)**.

Після цього форма буде закрита.