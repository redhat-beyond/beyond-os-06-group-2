from django.db import models
from django.db.models.manager import Manager


class Task(models.Model):
    author = models.ForeignKey(Manager, on_delete=models.RESTRICT)
    title = models.CharField(max_length=50)
    name_task = models.CharField()
    about = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    publish_date = models.DateTimeField()
    property = models.IntegerField()
   

    
    
    

