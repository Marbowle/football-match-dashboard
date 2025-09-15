from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any, List, Tuple


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


from .config import COLUMN_RENAMES, EXCLUDED_EVENT_TYPES


logger = logging.getLogger(__name__)


MATCH_ID_RE = re.compile(r"/matches/(\d+)")




def extract_match_id_from_url(url: str) -> int | None:
m = MATCH_ID_RE.search(url)
return int(m.group(1)) if m else None




def _extract_matchcentre_json(html: str) -> Dict[str, Any]:
soup = BeautifulSoup(html, "html.parser")
script = soup.select_one('script:-soup-contains("matchCentreData")')
if not script or not script.text:
raise ValueError("Nie znaleziono skryptu z matchCentreData")


try:
raw = script.text
start = raw.index("matchCentreData:") + len("matchCentreData:")
json_start = raw.index("{", start)
# zliczanie nawiasów
depth = 0
end = None
for i, ch in enumerate(raw[json_start:], start=json_start):
if ch == '{':
depth += 1
elif ch == '}':
depth -= 1
if depth == 0:
end = i + 1
break
if end is None:
raise ValueError("Nie udało się wyznaczyć końca JSON-a matchCentreData")
payload = raw[json_start:end]
return json.loads(payload)
except Exception as e:
raise ValueError(f"Błąd parsowania matchCentreData: {e}")

def parse_match_html_to_df(html: str, match_id: int) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:


if df.empty:
logger.warning("Brak eventów w matchCentreData")
df["match_id"] = match_id
return df, []


df["match_id"] = match_id
df.dropna(subset=["playerId"], inplace=True)
df.rename(columns=COLUMN_RENAMES, inplace=True)


# Kolumny zagnieżdżone na displayName
df["period_display_name"] = df["period"].apply(lambda x: x.get("displayName") if isinstance(x, dict) else None)
df["type_display_name"] = df["type"].apply(lambda x: x.get("displayName") if isinstance(x, dict) else None)
df["outcome_display_name"] = df["outcome_type"].apply(lambda x: x.get("displayName") if isinstance(x, dict) else None)


df.drop(columns=[c for c in ["period", "type", "outcome_type"] if c in df.columns], inplace=True)


if "is_goal" not in df.columns:
df["is_goal"] = False
if "card_type" not in df.columns:
df["card_type"] = None


if "type_display_name" in df.columns:
df = df[~df["type_display_name"].isin(EXCLUDED_EVENT_TYPES)]


# Porządkowanie kolumn
wanted = [
'id', 'event_id', 'minute', 'second', 'team_id', 'player_id', 'x', 'y', 'end_x', 'end_y',
'is_touch', 'blocked_x', 'blocked_y', 'goal_mouth_z', 'goal_mouth_y', 'is_shot',
'card_type', 'is_goal', 'type_display_name', 'outcome_display_name',
'period_display_name', 'match_id', 'qualifiers'
]
existing = [c for c in wanted if c in df.columns]
df = df[existing]


# Zamiana typów
int_cols = [c for c in ['id', 'event_id', 'minute', 'team_id', 'player_id', 'match_id'] if c in df.columns]
float_cols = [c for c in ['second', 'x', 'y', 'end_x', 'end_y'] if c in df.columns]
bool_cols = [c for c in ['is_shot', 'is_goal'] if c in df.columns]


for c in int_cols:
df[c] = df[c].astype('Int64').astype('int')
for c in float_cols:
df[c] = df[c].astype(float)
for c in bool_cols:
df[c] = df[c].fillna(False).astype(bool)


# None zamiast NaN
df = df.where(pd.notnull(df), None)


# Informacje o drużynach + zawodnikach
team_info = [
{
'team_id': matchdict['home']['teamId'],
'name': matchdict['home']['name'],
'country_name': matchdict['home']['countryName'],
'manager_name': matchdict['home']['managerName'],
'players': matchdict['home']['players']
},
{
'team_id': matchdict['away']['teamId'],
'name': matchdict['away']['name'],
'country_name': matchdict['away']['countryName'],
'manager_name': matchdict['away']['managerName'],
'players': matchdict['away']['players']
},
]


return df, team_info