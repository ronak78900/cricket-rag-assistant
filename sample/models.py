from pydantic import BaseModel, model_validator


class Match(BaseModel):
    date: str
    team1: str
    team2: str
    winner: str | None = None

    # TODO: add a @model_validator(mode="after") method that raises ValueError
    # if winner is not None and winner is not team1 or team2
    @model_validator(mode="after")
    def validate_winner(self):
        if self.winner is not None and self.winner not in [self.team1, self.team2]:
            raise ValueError("Winner must be either team1 or team2")
        return self