from django.db import models

class Chat(models.Model):
    chat_id = models.IntegerField(unique=True, null=True)
    generation_amount = models.IntegerField(default=15)

    def __str__(self) -> str:
        return f"tg_id: {self.chat_id}"
    
class Client(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    
class Image(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    image_url = models.URLField(null=True)
    tg_message_id = models.CharField(max_length=70, unique=True, null=True)
    messageid_sseed = models.CharField(max_length=70, unique=True, null=True)
    prompt = models.TextField(null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_ended = models.BooleanField(default=False)