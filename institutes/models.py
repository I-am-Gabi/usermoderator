from django.db import models
from django.utils import timezone

class Institute(models.Model): 
    name = models.CharField(max_length=200) 
    created_date = models.DateTimeField(
            default=timezone.now)  

    def __str__(self):
        return self.name