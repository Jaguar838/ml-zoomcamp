# FAQ: Автоматическое масштабирование (Autoscaling) в Kubernetes

## 1. **Что такое Autoscaling в Kubernetes?**
Autoscaling — это механизм автоматического масштабирования количества подов или узлов в кластере Kubernetes в зависимости от нагрузки. Kubernetes поддерживает три типа масштабирования:

- **Horizontal Pod Autoscaler (HPA)** — автоматическое масштабирование количества подов.
- **Vertical Pod Autoscaler (VPA)** — автоматическое изменение ресурсов CPU и памяти для подов.
- **Cluster Autoscaler** — автоматическое масштабирование количества узлов в кластере.

---
## 2. **Как включить HPA (Horizontal Pod Autoscaler)?**
HPA можно включить с помощью команды `kubectl autoscale`. Например:

```bash
kubectl autoscale deployment <deployment-name> --cpu-percent=<target-percent> --min=<min-pods> --max=<max-pods>
```
- `<deployment-name>` — имя деплоймента, для которого настраивается HPA.
- `<target-percent>` — целевая утилизация CPU (в процентах).
- `<min-pods>` — минимальное количество реплик.
- `<max-pods>` — максимальное количество реплик.

**Пример:**
```bash
kubectl autoscale deployment subscription --cpu-percent=20 --min=1 --max=3
```

---
## 3. **Почему HPA показывает `cpu: <unknown>`?**
Если HPA не может получить метрики CPU, это может быть вызвано следующими причинами:

1. **Metrics Server не запущен**
   Проверьте статус Metrics Server:
   ```bash
   kubectl get pods -n kube-system
   ```
   Убедитесь, что под Metrics Server находится в статусе `Running`.

2. **Проблема с сертификатами**
   Иногда Metrics Server сталкивается с ошибками валидации TLS-сертификатов. Для обхода проблемы можно использовать опцию `--kubelet-insecure-tls`:
   ```bash
   kubectl patch deployment metrics-server -n kube-system \
     --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
   kubectl rollout restart deployment metrics-server -n kube-system
   ```
   **Внимание:** Это решение подходит для тестовой среды, но не рекомендуется для production.

3. **Отсутствие ресурсов для измерения нагрузки**
   Проверьте, что в деплойменте поды имеют ресурсы CPU, прописанные в `requests`:
   ```yaml
   resources:
     requests:
       cpu: "100m"
     limits:
       cpu: "200m"
   ```

---
## 4. **Как проверить статус HPA?**
Статус HPA можно проверить с помощью следующей команды:

```bash
kubectl get hpa <hpa-name>
```

**Пример вывода:**
```
NAME               REFERENCE                 TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
subscription-hpa   Deployment/subscription   cpu: 15%/20%   1         3         1          3h8m
```
- **TARGETS** показывает текущую и целевую утилизацию CPU.
- **MINPODS/MAXPODS** указывает минимальное и максимальное количество реплик.
- **REPLICAS** показывает текущее количество реплик.

---
## 5. **Почему количество реплик не меняется?**
Если количество реплик не меняется:

1. **Нагрузка ниже целевого значения**
   Проверьте текущую нагрузку на CPU в поле **TARGETS**. Если она ниже целевого значения, количество реплик останется минимальным.

2. **Некорректные метрики**
   Проверьте корректность работы Metrics Server и наличие ресурсов CPU в `requests` деплоймента.

3. **Нагрузка распределяется по всем ядрам CPU**
   Kubernetes может распределять нагрузку по нескольким ядрам, что делает общую утилизацию CPU низкой.

**Совет:** Можно уменьшить целевой процент CPU с помощью `--cpu-percent` или увеличить нагрузку в тестовом скрипте.

---
## 6. **Как протестировать HPA на практике?**

1. **Запустите деплоймент** с установленными ресурсами CPU:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: subscription
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: subscription
     template:
       metadata:
         labels:
           app: subscription
       spec:
         containers:
         - name: subscription
           image: nginx
           resources:
             requests:
               cpu: "100m"
             limits:
               cpu: "200m"
   ```
(`deployment.yaml`):

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
        image: svizor/zoomcamp-model:3.11.5-hw10
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"            
          limits:
            memory: "128Mi"
            cpu: "200m"
        ports:
        - containerPort: 9696
```
2. **Настройте HPA:**
   ```bash
   kubectl autoscale deployment subscription --cpu-percent=20 --min=1 --max=3
   ```

3. **Генерируйте нагрузку:**
   Можно использовать утилиту `kubectl run` для создания нагрузки:
   ```bash
   kubectl run -i --tty load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://<service-ip>; done"
   ```

4. **Проверьте HPA:**
   ```bash
   kubectl get hpa subscription-hpa --watch
   ```

---
## 7. **Можно ли использовать HPA в Production?**
Да, HPA можно использовать в Production, но для этого необходимо:

- Настроить корректные метрики с помощью Metrics Server или Prometheus.
- Использовать TLS валидацию для Metrics Server (не использовать `--kubelet-insecure-tls`).
- Тщательно протестировать утилизацию ресурсов и нагрузку на поды.

---
## 8. **Как работает HPA с другими масштабированиями?**
- **HPA и Cluster Autoscaler** могут работать вместе. HPA увеличивает количество подов, а Cluster Autoscaler масштабирует узлы для их размещения.
- HPA конфликтует с VPA, так как они оба управляют ресурсами подов. Не используйте их вместе для одного и того же пода.

---
## Заключение
Autoscaling в Kubernetes — мощный инструмент для автоматического масштабирования приложений. HPA позволяет эффективно реагировать на изменение нагрузки и обеспечивать стабильность системы. Однако важно учитывать корректность метрик и окружения, особенно в Production.

 