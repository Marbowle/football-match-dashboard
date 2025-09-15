from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Dict

DEFAULT_WAIT_SECONDS = int(os.getenv("WS_WAIT_SECONDS", "15"))
DEFAULT_HEADLESS = os.getenv("WS_HEADLESS", "true").lower() == "true"
BASE_URL =  os.getenv("WS_BASE_URL", "https://www.whoscored.com")

COLUMNS_RENAMES: Dict[str, str] = {
    'eventId': 'event_id',
    'expandedMinute': 'expanded_minute',
    'outcomeType': 'outcome_type',
    'isTouch': 'is_touch',
    'playerId': 'player_id',
    'teamId': 'team_id',
    'endX': 'end_x',
    'endY': 'end_y',
    'blockedX': 'blocked_x',
    'blockedY': 'blocked_y',
    'goalMouthZ': 'goal_mouth_z',
    'goalMouthY': 'goal_mouth_y',
    'isShot': 'is_shot',
    'cardType': 'card_type',
    'isGoal': 'is_goal'
}

EXCLUDED_EVENT_TYPES: List[str] = [
    "OffsideGiven",
]