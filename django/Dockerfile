FROM python:3.10

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app/

COPY ./jervis ./

CMD ["sh", "-c", "celery -A jervis worker -l info -Q free_tasks,paid_tasks & uvicorn jervis.asgi:application --host 0.0.0.0 --port 8000"]
#CMD ["sh", "-c", "celery -A jervis worker -l info -Q free_tasks,paid_tasks & python manage.py runserver 0.0.0.0:8000"]
#CMD ["uvicorn", "jervis.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]