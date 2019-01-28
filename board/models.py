from django.db import models


class GameResult(models.Model):
    """Game result model"""
    info = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-id']
