from __future__ import unicode_literals

from django.db import models

def only_filename(instance, filename):
    return filename


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=only_filename)   #
    #document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # title = models.CharField(max_length=255)

    def __str__(self):
        return self.document.name
