
from django.db import models


class Competition(models.Model):

    name = models.CharField(max_length=150, unique=True)
    country = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "competitions"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country})"


class Season(models.Model):

    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name="seasons"
    )

    name = models.CharField(max_length=20)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "seasons"
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["competition", "name"],
                name="unique_competition_season"
            )
        ]

    def __str__(self):
        return f"{self.competition.name} {self.name}"

# Create your models here.
