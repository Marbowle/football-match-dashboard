from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class MatchEvent(BaseModel):
    id: int
    event_id: int
    minute: int
    second: Optional[float] = None
    team_id: int
    player_id: int
    x: float
    y: float
    end_x: Optional[float] = None
    end_y: Optional[float] = None
    is_touch: bool
    blocked_x: Optional[float] = None
    blocked_y: Optional[float] = None
    goal_mouth_z: Optional[float] = None
    goal_mouth_y: Optional[float] = None
    is_shot: bool
    card_type: bool
    is_goal: bool
    type_display_name: str
    outcome_display_name: str
    period_display_name: str
    match_id: int
    qualifiers: List[Dict[str, Any]]

class Player(BaseModel):
    player_id: int
    shirt_no: int
    name: str
    age: int
    position: str
    team_id: int

class Team(BaseModel):
    team_id: int
    name: str
    manager_name: str
    country_name: str