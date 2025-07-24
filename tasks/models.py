from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#FFFFFF')
    description = models.TextField(blank=True)

    
    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title