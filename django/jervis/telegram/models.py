from django.db import models

class Chat(models.Model):
    STATUS_CHOICES = [
        ("paid", "paid"),
        ("free", "free"),
    ]
    
    chat_id = models.IntegerField(unique=True, null=True)
    generation_amount = models.IntegerField(default=15)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="free")

    def __str__(self) -> str:
        return f"tg_id: {self.chat_id} generations: {self.generation_amount}"
    
    
class Image(models.Model):
    #client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    image_url = models.URLField(null=True)
    tg_message_id = models.IntegerField(null=True)
    mesageid_sseed = models.CharField(max_length=200, unique=True, null=True)
    prompt = models.TextField(null=True, db_index=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_ended = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.pk} > {self.prompt[:30]}"