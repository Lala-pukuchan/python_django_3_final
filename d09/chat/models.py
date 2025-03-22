from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # to create url like chat/room-1/
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
