import csv
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from competitions.models import Competition, Season
from teams.models import Team
from matches.models import Match


class Command(BaseCommand):

    help = "Import cleaned EPL match data into PostgreSQL"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default=None,
            help="Path to the cleaned EPL CSV file"
        )

    def handle(self, *args, **options):

        backend_dir = Path(__file__).resolve().parents[3]
        project_root = backend_dir.parent

        csv_file = options["file"]

        if csv_file:
            csv_path = Path(csv_file).expanduser().resolve()
        else:
            csv_path = (
                project_root
                / "data"
                / "processed"
                / "epl_matches_cleaned.csv"
            )

        if not csv_path.exists():
            raise CommandError(
                f"Dataset not found: {csv_path}"
            )

        self.stdout.write(
            self.style.NOTICE(
                f"Reading dataset: {csv_path}"
            )
        )

        competition, _ = Competition.objects.get_or_create(
            name="English Premier League",
            defaults={"country": "England"}
        )

        season_cache = {}
        team_cache = {}

        matches_to_create = []

        try:

            with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:

                reader = csv.DictReader(file)

                required_columns = {
                    "match_id",
                    "season",
                    "round",
                    "match_date",
                    "home_team",
                    "away_team",
                    "half_time_home_goals",
                    "half_time_away_goals",
                    "home_goals",
                    "away_goals",
                    "total_goals",
                    "goal_difference",
                    "result",
                    "home_points",
                    "away_points"
                }

                missing = required_columns - set(reader.fieldnames or [])

                if missing:
                    raise CommandError(
                        f"Missing CSV columns: {sorted(missing)}"
                    )

                with transaction.atomic():

                    for row in reader:

                        season_name = row["season"].strip()

                        if season_name not in season_cache:

                            season, _ = Season.objects.get_or_create(
                                competition=competition,
                                name=season_name
                            )

                            season_cache[season_name] = season

                        season = season_cache[season_name]

                        home_name = row["home_team"].strip()
                        away_name = row["away_team"].strip()

                        if home_name not in team_cache:
                            team_cache[home_name], _ = (
                                Team.objects.get_or_create(
                                    name=home_name
                                )
                            )

                        if away_name not in team_cache:
                            team_cache[away_name], _ = (
                                Team.objects.get_or_create(
                                    name=away_name
                                )
                            )

                        def parse_int(value, field_name):
                            if value is None or not value.strip():
                                return None

                            try:
                                number = float(value)

                                if not number.is_integer():
                                    raise ValueError(f"{field_name} must be a whole number: {value}")

                                return int(number)

                            except ValueError as exc:
                                raise ValueError(f"Invalid value in {field_name}: {value}") from exc

                        match = Match(
                            match_id=row["match_id"],
                            season=season,
                            round=row["round"] or None,
                            match_date=date.fromisoformat(row["match_date"][:10]),
                            home_team=team_cache[home_name],
                            away_team=team_cache[away_name],

                            half_time_home_goals=parse_int(
                                row["half_time_home_goals"], "half_time_home_goals"
                            ),
                            half_time_away_goals=parse_int(
                                row["half_time_away_goals"], "half_time_away_goals"
                            ),

                            home_goals=parse_int(row["home_goals"], "home_goals"),
                            away_goals=parse_int(row["away_goals"], "away_goals"),
                            total_goals=parse_int(row["total_goals"], "total_goals"),
                            goal_difference=parse_int(row["goal_difference"], "goal_difference"),
                            result=row["result"],
                            home_points=parse_int(row["home_points"], "home_points"),
                            away_points=parse_int(row["away_points"], "away_points"),
                        )

                        matches_to_create.append(match)

                    before_count = Match.objects.count()

                    Match.objects.bulk_create(
                        matches_to_create,
                        batch_size=500,
                        ignore_conflicts=True
                    )

                    after_count = Match.objects.count()

            imported = after_count - before_count

            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    "MATCHIQ DATA INGESTION COMPLETED"
                )
            )

            self.stdout.write(
                f"Competition: {competition.name}"
            )

            self.stdout.write(
                f"Seasons: {len(season_cache)}"
            )

            self.stdout.write(
                f"Teams processed: {len(team_cache)}"
            )

            self.stdout.write(
                f"New matches imported: {imported}"
            )

            self.stdout.write(
                f"Total matches in database: {after_count}"
            )

        except (ValueError, KeyError) as exc:
            raise CommandError(
                f"Invalid dataset record: {exc}"
            ) from exc