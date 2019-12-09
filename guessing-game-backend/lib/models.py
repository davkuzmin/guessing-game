from django.db import models

'''
This model will be extended by other models to track
when they were first created and most recently updated
'''
class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
