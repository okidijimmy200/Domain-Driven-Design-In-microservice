import datetime
from typing import Any
from dataclasses import dataclass

@dataclass
class SportBet:
    id: int
    league: str
    home_team: str
    away_team: str
    home_team_win_odds: float
    away_team_win_odds: float
    draw_odds: float
    game_date: str

@dataclass
class CreateBetSQL:
    league: str
    home_team : str
    away_team: str
    home_team_win_odds : float
    away_team_win_odds: float
    draw_odds: float
    game_date: datetime.date


@dataclass
class CreateBetRequest:
    league: str
    home_team : str
    away_team: str
    home_team_win_odds : float
    away_team_win_odds: float
    draw_odds: float
    game_date:str

@dataclass
class CreateBetResponse:
    code: int
    reason : str

@dataclass
class ReadBetRequest:
    league: str
    start_date: str
    end_date: str

@dataclass
class ReadBetResponse:
    code: int
    response: Any
    reason: str

@dataclass
class UpdateBetRequest:
    league: str
    home_team : str
    away_team: str
    home_team_win_odds : float
    away_team_win_odds: float
    draw_odds: float
    game_date: str

@dataclass
class UpdateBetResponse:
    code: int
    reason : str

@dataclass
class DeleteBetRequest:
    league: str
    home_team: str
    away_team: str
    game_date: str

@dataclass
class DeleteBetResponse:
    code: int
    reason: str