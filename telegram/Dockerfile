FROM python:3.10

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install --upgrade pip setuptools

WORKDIR /app/

COPY ./app ./

CMD bash -c "python main.py & python ./tg_api/main_api.py"