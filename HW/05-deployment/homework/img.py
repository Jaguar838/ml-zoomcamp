docker pull svizor/zoomcamp-model

docker build -t churn-prediction
docker run -it -p 9696:9696 churn-prediction:latest