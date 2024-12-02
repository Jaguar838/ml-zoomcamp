FROM svizor/zoomcamp-model:3.11.5-slim


WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "q6_predict.py", "./"]
RUN pip install pipenv
RUN pip install gunicorn
RUN pipenv install --system --deploy

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "q6_predict:app"]