FROM python:3.10

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app/

COPY ./app ./

CMD bash -c "python discordBot.py & uvicorn api:app --host 0.0.0.0 --port 80 --reload"