from django.core.management import call_command
from crontab import CronTab
import os
from celery import shared_task
import requests
from .celery import app

# Templates of tasks for reucing code base
def generate_image(prompt, ds_socket):
    data = {"prompt": prompt}
    response = requests.post(f"http://{ds_socket}/generate_image/", json=data)
    return response


def push_button(method, image_number, messageid_sseed, ds_socket):
    data = {"method":method,
            "image_number":image_number,
            "messageid_sseed":messageid_sseed}
    response = requests.post(f"http://{ds_socket}/push_button/", json=data)
    return response


@app.task(queue='free_tasks', priority=1)
def send_data_to_telegram(image_url, tg_message_id, chat_id, prompt, tg_socket):
    data_for_tg = {
        "image_url": image_url,
        "tg_message_id": tg_message_id,
        "chat_id": chat_id,
        "prompt": prompt
    }
    response = requests.post(f"http://{tg_socket}/load_image/", json=data_for_tg)
    return response


# TELEGRAM TASKS
@app.task(queue='free_tasks', priority=1)
def generate_free_image(prompt, ds_socket):
    generate_image(prompt, ds_socket)
    return {"result": "image generation task has been added to the queue."}


@app.task(queue='paid_tasks', priority=10)
def generate_paid_image(prompt, ds_socket):
    generate_image(prompt, ds_socket)
    return {"result": "image generation task has been added to the queue."}


@app.task(queue='free_tasks', priority=1)
def push_free_button(method, image_number, messageid_sseed, ds_socket):
    push_button(method, image_number, messageid_sseed, ds_socket)
    return {"result": "image push button task has been added to the queue."}


@app.task(queue='paid_tasks', priority=10)
def push_paid_button(method, image_number, messageid_sseed, ds_socket):
    push_button(method, image_number, messageid_sseed, ds_socket)
    return {"result": "image push button task has been added to the queue."}
    

@app.task(queue='free_tasks', priority=1)
def send_data_to_telegram_free(image_url, tg_message_id, chat_id, prompt, tg_socket):
    send_data_to_telegram(image_url, tg_message_id, chat_id, prompt, tg_socket)
    return {"result": "send data task has been added to the queue."}

@app.task(queue='paid_tasks', priority=10)
def send_data_to_telegram_paid(image_url, tg_message_id, chat_id, prompt, tg_socket):
    send_data_to_telegram(image_url, tg_message_id, chat_id, prompt, tg_socket)
    return {"result": "send data task has been added to the queue."}
    