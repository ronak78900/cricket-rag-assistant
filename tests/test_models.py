import pytest
from pydantic import ValidationError

from sample.models import Match


def test_valid_match():
    match = Match(date="2026-01-05", team1="India", team2="Australia", winner="India")
    assert match.winner == "India"


def test_winner_defaults_to_none():
    match = Match(date="2026-01-05", team1="India", team2="Australia")
    assert match.winner is None


def test_missing_team1_raises_error():
    with pytest.raises(ValidationError):
        Match(date="2026-01-05", team2="Australia")


def test_winner_must_be_one_of_the_teams():
    with pytest.raises(ValidationError):
        Match(date="2026-01-05", team1="India", team2="Australia", winner="Pakistan")