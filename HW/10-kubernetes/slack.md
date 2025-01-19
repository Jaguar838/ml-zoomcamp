### Переклад діалогу

---

**Yann Pham-Van**  
П’ятниця, 8:55 PM  
Я завершив домашнє завдання 10, але не зміг закінчити додаткову частину про автоскейлінг.  
Ця команда так і не запрацювала:  
```bash
kubectl autoscale deployment subscription --name subscription-hpa --cpu-percent=20 --min=1 --max=3
```  
Хтось ще зміг це зробити?  

---

**Till**  
:not-sure-if: Субота, 12:25 PM  
Я робив домашнє завдання разом із ChatGPT, і він підказав, що мій `metrics-server` не був повністю функціональним. Пізніше все запрацювало:  
```bash
❯ kubectl get hpa subscription-hpa --watch  
NAME               REFERENCE                 TARGETS              MINPODS   MAXPODS   REPLICAS   AGE  
subscription-hpa   Deployment/subscription   cpu: <unknown>/20%   1         3         3          53m  
subscription-hpa   Deployment/subscription   cpu: 200%/20%        1         3         3          53m  
subscription-hpa   Deployment/subscription   cpu: 201%/20%        1         3         3          53m  
subscription-hpa   Deployment/subscription   cpu: <unknown>/20%   1         3         3          54m  
```  
Але все одно були деякі проблеми.  

---

**Timur Kamaliev**  
Субота, 4:12 PM  
Привіт, Тілле!  
Ти перевіряв `Metrics Server`? Він працює?  
```bash
kubectl get pods -n kube-system
```  

---

**Till**  
:not-sure-if: Субота, 5:11 PM  
Так, `metrics server` працював. Я не міг побачити масштабування при збільшенні чи зменшенні навантаження. Кількість реплік завжди залишалася на рівні 3, і CPU показував `unknown`. Навантаження розподілялося на всі 8 ядер CPU.  

```bash
❯ kubectl get pods -n kube-system  
NAME                                         READY   STATUS    RESTARTS   AGE  
coredns-7c65d6cfc9-5ns2p                     1/1     Running   0          4h49m  
coredns-7c65d6cfc9-m4lvv                     1/1     Running   0          4h49m  
etcd-kind-control-plane                      1/1     Running   0          4h49m  
kindnet-9llmn                                1/1     Running   0          4h49m  
kube-apiserver-kind-control-plane            1/1     Running   0          4h49m  
kube-controller-manager-kind-control-plane   1/1     Running   0          4h49m  
kube-proxy-7dtmj                             1/1     Running   0          4h49m  
kube-scheduler-kind-control-plane            1/1     Running   0          4h49m  
metrics-server-f5745db6d-qtxtk               1/1     Running   0          2m20s  
```  

---

**Timur Kamaliev**  
Субота, 7:56 PM  
Так, здається, що з `metrics server` все гаразд.  
А що, якщо припинити надсилання запитів через скрипт із циклом? Кількість реплік залишиться незмінною?  

---

**Siddharth Puranam**  
Субота, 9:34 PM  
Я також застряг на цій частині. Переглядаючи журнали помилок, я знайшов, що проблема пов’язана з перевіркою сертифікатів через відсутність дійсного `Subject Alternative Name (SAN)` для IP-адреси вузла.  

---

**Till**  
:not-sure-if: Субота, 10:40 PM  
@Siddharth Puranam  
Я думаю, у мене була та сама проблема. ChatGPT запропонував:  
```bash
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
```
Щоб пропустити перевірку TLS, і  
```bash
kubectl rollout restart deployment metrics-server -n kube-system
```
Щоб перезапустити розгортання. Після цього `metrics server` запрацював.  

---

**Siddharth Puranam**  
Неділя, 12:38 AM  
@Till  
Дякую за допомогу. Це вирішило всі проблеми, і я зміг усе налаштувати. Але на моєму комп’ютері кількість реплік не збільшувалася більше ніж одна.  

```bash
NAME               REFERENCE                 TARGETS       MINPODS   MAXPODS   REPLICAS   AGE  
subscription-hpa   Deployment/subscription   cpu: 1%/20%   1         3         1          3h8m  
subscription-hpa   Deployment/subscription   cpu: 14%/20%  1         3         1          3h8m  
subscription-hpa   Deployment/subscription   cpu: 15%/20%  1         3         1          3h8m  
subscription-hpa   Deployment/subscription   cpu: 16%/20%  1         3         1          3h12m  
subscription-hpa   Deployment/subscription   cpu: 15%/20%  1         3         1          3h12m  
```  

---

**Timur Kamaliev**  
Неділя, 8:35 AM  
@Till  
Отже, можна використовувати це рішення, щоб уникнути перевірки сертифіката TLS. Це може бути не найкращим рішенням для систем, готових до продакшену, але для нашого випадку цього достатньо.  
@Siddharth Puranam  
Це залежить від екземплярів, на яких ми запускаємо наше рішення. Ви можете спробувати зменшити використання `cpu-percent` або час очікування в тестовому скрипті. Ідея полягала в тому, щоб показати, як працює горизонтальне масштабування, коли змінюється навантаження на сервіс.  