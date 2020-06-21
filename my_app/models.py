from django.db import models

# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return self.search
