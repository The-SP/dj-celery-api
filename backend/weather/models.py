from django.db import models

class SearchHistory(models.Model):
    city_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city_name} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']