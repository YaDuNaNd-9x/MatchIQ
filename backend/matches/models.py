
from django.db import models


class Match(models.Model):

    class Result(models.TextChoices):
        HOME_WIN = "H", "Home Win"
        DRAW = "D", "Draw"
        AWAY_WIN = "A", "Away Win"

    # Original source identifier
    match_id = models.CharField(
        max_length=50,
        unique=True
    )

    season = models.ForeignKey(
        "competitions.Season",
        on_delete=models.CASCADE,
        related_name="matches"
    )

    round = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    match_date = models.DateField()

    home_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.PROTECT,
        related_name="home_matches"
    )

    away_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.PROTECT,
        related_name="away_matches"
    )

    # Half-time scores
    half_time_home_goals = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    half_time_away_goals = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    # Full-time scores
    home_goals = models.PositiveSmallIntegerField()
    away_goals = models.PositiveSmallIntegerField()

    total_goals = models.PositiveSmallIntegerField()

    goal_difference = models.SmallIntegerField()

    result = models.CharField(
        max_length=1,
        choices=Result.choices
    )

    home_points = models.PositiveSmallIntegerField()
    away_points = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "matches"

        ordering = ["match_date"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "season",
                    "match_date",
                    "home_team",
                    "away_team"
                ],
                name="unique_season_match"
            ),
            models.CheckConstraint(
                condition=~models.Q(home_team=models.F("away_team")),
                name="different_home_away_teams"
            )
        ]

        indexes = [
            models.Index(
                fields=["season", "match_date"],
                name="match_season_date_idx"
            ),
            models.Index(
                fields=["home_team", "match_date"],
                name="match_home_date_idx"
            ),
            models.Index(
                fields=["away_team", "match_date"],
                name="match_away_date_idx"
            ),
            models.Index(
                fields=["result"],
                name="match_result_idx"
            )
        ]

    def __str__(self):
        return (
            f"{self.home_team} {self.home_goals} - "
            f"{self.away_goals} {self.away_team}"
        )

# Create your models here.
