FROM python:3.10

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install --upgrade pip setuptools

WORKDIR /app/

COPY ./app ./

#CMD bash -c "python discordBot.py & uvicorn api:app --host 0.0.0.0 --port 80 --reload"
CMD bash -c "python discordBot.py & uvicorn apiPhotoSendTest:app --host 0.0.0.0 --port 80 --reload"