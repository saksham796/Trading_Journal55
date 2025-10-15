from django.db import models
from django.contrib.auth import get_user_model


class Trade(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='trades')
    salt_b64 = models.CharField(max_length=255)
    iterations = models.IntegerField()
    blob_b64 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Trade #{self.pk} for user {self.user_id}"

# Create your models here.
