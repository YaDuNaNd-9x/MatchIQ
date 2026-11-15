
from django.db import models


class Team(models.Model):

    name = models.CharField(max_length=150, unique=True)

    external_source_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "teams"
        ordering = ["name"]

    def __str__(self):
        return self.name

# Create your models here.
