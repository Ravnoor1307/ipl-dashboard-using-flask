import json
import math
import numpy as np
import pandas as pd


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


IPL_MATCHES_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
BALLS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRu6cb6Pj8C9elJc5ubswjVTObommsITlNsFy5X0EiBY7S-lsHEUqx3g_M16r50Ytjc0XQCdGDyzE_Y/pub?output=csv"

FALLBACK_TEAMS = [
    'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bengaluru',
    'Kolkata Knight Riders', 'Rajasthan Royals', 'Sunrisers Hyderabad',
    'Delhi Capitals', 'Punjab Kings', 'Gujarat Titans', 'Lucknow Super Giants'
]

FALLBACK_MATCHES = [
    {'id': 1, 'city': 'Mumbai', 'date': '2023-04-10', 'team1': 'Mumbai Indians', 'team2': 'Chennai Super Kings', 'winner': 'Mumbai Indians', 'player_of_match': 'Suryakumar Yadav'},
    {'id': 2, 'city': 'Bengaluru', 'date': '2023-04-15', 'team1': 'Royal Challengers Bengaluru', 'team2': 'Rajasthan Royals', 'winner': 'Rajasthan Royals', 'player_of_match': 'Sanju Samson'},
    {'id': 3, 'city': 'Kolkata', 'date': '2023-04-18', 'team1': 'Kolkata Knight Riders', 'team2': 'Lucknow Super Giants', 'winner': 'Kolkata Knight Riders', 'player_of_match': 'Andre Russell'},
    {'id': 4, 'city': 'Delhi', 'date': '2023-04-20', 'team1': 'Delhi Capitals', 'team2': 'Gujarat Titans', 'winner': 'Gujarat Titans', 'player_of_match': 'Shubman Gill'},
    {'id': 5, 'city': 'Hyderabad', 'date': '2023-04-23', 'team1': 'Sunrisers Hyderabad', 'team2': 'Punjab Kings', 'winner': 'Sunrisers Hyderabad', 'player_of_match': 'Heinrich Klaasen'}
]

FALLBACK_BALLS = [
    {'id': 1, 'innings': 1, 'battingteam': 'Mumbai Indians', 'bowlingteam': 'Chennai Super Kings', 'batter': 'Suryakumar Yadav', 'bowler': 'Deepak Chahar', 'extra_type': 'none', 'total_run': 0, 'batsman_run': 4, 'non_boundary': 0, 'player_out': '', 'kind': 'none', 'isWicketDelivery': 0, 'player_of_match': 'Suryakumar Yadav'},
    {'id': 1, 'innings': 1, 'battingteam': 'Mumbai Indians', 'bowlingteam': 'Chennai Super Kings', 'batter': 'Rohit Sharma', 'bowler': 'Deepak Chahar', 'extra_type': 'none', 'total_run': 1, 'batsman_run': 1, 'non_boundary': 0, 'player_out': '', 'kind': 'none', 'isWicketDelivery': 0, 'player_of_match': 'Suryakumar Yadav'},
    {'id': 2, 'innings': 1, 'battingteam': 'Rajasthan Royals', 'bowlingteam': 'Royal Challengers Bengaluru', 'batter': 'Sanju Samson', 'bowler': 'Mohammed Siraj', 'extra_type': 'none', 'total_run': 2, 'batsman_run': 2, 'non_boundary': 0, 'player_out': '', 'kind': 'none', 'isWicketDelivery': 0, 'player_of_match': 'Sanju Samson'},
    {'id': 3, 'innings': 1, 'battingteam': 'Kolkata Knight Riders', 'bowlingteam': 'Lucknow Super Giants', 'batter': 'Andre Russell', 'bowler': 'Krunal Pandya', 'extra_type': 'none', 'total_run': 6, 'batsman_run': 6, 'non_boundary': 0, 'player_out': '', 'kind': 'none', 'isWicketDelivery': 0, 'player_of_match': 'Andre Russell'},
    {'id': 4, 'innings': 1, 'battingteam': 'Delhi Capitals', 'bowlingteam': 'Gujarat Titans', 'batter': 'David Warner', 'bowler': 'Mohammed Shami', 'extra_type': 'none', 'total_run': 3, 'batsman_run': 3, 'non_boundary': 0, 'player_out': '', 'kind': 'none', 'isWicketDelivery': 0, 'player_of_match': 'Shubman Gill'}
]


def _normalize_columns(frame):
    if frame is None or not isinstance(frame, pd.DataFrame):
        return pd.DataFrame()
    frame = frame.copy()
    frame.columns = [str(col).strip().lower() for col in frame.columns]
    return frame


def load_matches():
    try:
        matches = pd.read_csv(IPL_MATCHES_URL)
        matches = _normalize_columns(matches)
        if {'team1', 'team2'}.issubset(matches.columns):
            return matches
    except Exception:
        pass
    return pd.DataFrame(FALLBACK_MATCHES)


def load_balls():
    try:
        balls = pd.read_csv(BALLS_URL)
        balls = _normalize_columns(balls)
        if not balls.empty:
            return balls
    except Exception:
        pass
    return pd.DataFrame(FALLBACK_BALLS)


def _normalize_team_name(team):
    return str(team).strip().replace('_', ' ').replace('-', ' ').lower()


def _normalize_city_name(city):
    return str(city).strip().replace('_', ' ').replace('-', ' ').lower()


matches = load_matches()
balls = load_balls()

if 'team1' in matches.columns and 'team2' in matches.columns:
    matches['team1'] = matches['team1'].astype(str)
    matches['team2'] = matches['team2'].astype(str)

if 'player_of_match' in matches.columns:
    matches['player_of_match'] = matches['player_of_match'].fillna('').astype(str)

for col in ['battingteam', 'bowlingteam', 'batter', 'bowler', 'extra_type', 'player_out', 'kind', 'player_of_match']:
    if col in balls.columns:
        balls[col] = balls[col].fillna('').astype(str)

ball_withmatch = balls.merge(matches, on='id', how='inner').copy() if 'id' in balls.columns and 'id' in matches.columns else balls.copy()

if 'battingteam' in ball_withmatch.columns and 'bowlingteam' in ball_withmatch.columns:
    ball_withmatch['bowlingteam'] = ball_withmatch['bowlingteam'].fillna('').astype(str)
    ball_withmatch['battingteam'] = ball_withmatch['battingteam'].fillna('').astype(str)

batter_data = ball_withmatch.copy()


def _json_safe(value):
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        return _json_safe(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if value is pd.NaT or value is pd.NA:
        return None
    return value


def teams_api():
    team1 = matches.get('team1', pd.Series(dtype=object)).dropna().astype(str).tolist()
    team2 = matches.get('team2', pd.Series(dtype=object)).dropna().astype(str).tolist()
    teams = list(dict.fromkeys(team1 + team2))
    return {'teams': teams}


def matches_api():
    records = matches.to_dict(orient='records')
    return _json_safe({'count': len(matches), 'matches': records})


def cities_api():
    cities = matches.get('city', pd.Series(dtype=object)).dropna().astype(str).str.strip()
    unique_cities = list(dict.fromkeys(cities.tolist()))
    return {'cities': unique_cities}


def team_matches_api(team_name):
    team_norm = _normalize_team_name(team_name)
    team1_values = matches.get('team1', pd.Series(dtype=object)).fillna('').astype(str).str.strip().str.lower()
    team2_values = matches.get('team2', pd.Series(dtype=object)).fillna('').astype(str).str.strip().str.lower()
    filtered = matches[(team1_values == team_norm) | (team2_values == team_norm)]
    return _json_safe({'team': team_name, 'count': len(filtered), 'matches': filtered.to_dict(orient='records')})


def city_matches_api(city_name):
    city_norm = _normalize_city_name(city_name)
    city_values = matches.get('city', pd.Series(dtype=object)).fillna('').astype(str).str.strip().str.lower()
    filtered = matches[city_values == city_norm]
    return _json_safe({'city': city_name, 'count': len(filtered), 'matches': filtered.to_dict(orient='records')})


def teamVteamAPI(team1, team2):
    team1_norm = _normalize_team_name(team1)
    team2_norm = _normalize_team_name(team2)
    team1_values = matches.get('team1', pd.Series(dtype=object)).fillna('').astype(str).str.strip().str.lower()
    team2_values = matches.get('team2', pd.Series(dtype=object)).fillna('').astype(str).str.strip().str.lower()

    direct = matches[(team1_values == team1_norm) & (team2_values == team2_norm)]
    if not direct.empty:
        return _json_safe({'team1': team1, 'team2': team2, 'matches': direct.to_dict(orient='records'), 'count': len(direct), 'message': 'Matches found between the selected teams.'})

    reverse = matches[(team1_values == team2_norm) & (team2_values == team1_norm)]
    if not reverse.empty:
        return _json_safe({'team1': team1, 'team2': team2, 'matches': reverse.to_dict(orient='records'), 'count': len(reverse), 'message': 'Matches found between the selected teams.'})

    return {'team1': team1, 'team2': team2, 'matches': [], 'count': 0, 'message': 'No matches found for the selected teams.'}


def team1vsteam2(team, team2):
    df = matches[((matches['team1'] == team) & (matches['team2'] == team2)) | ((matches['team2'] == team) & (matches['team1'] == team2))].copy()
    mp = df.shape[0]
    won = df[df['winner'] == team].shape[0]
    nr = df[df['winner'].isnull()].shape[0]
    loss = mp - won - nr
    return {'matchesplayed': mp, 'won': won, 'loss': loss, 'noResult': nr}


def allRecord(team):
    df = matches[(matches['team1'] == team) | (matches['team2'] == team)].copy()
    mp = df.shape[0]
    won = df[df['winner'] == team].shape[0]
    nr = df[df['winner'].isnull()].shape[0]
    loss = mp - won - nr
    title_col = df.get('matchnumber', pd.Series([None] * len(df)))
    nt = df[(df['winner'] == team) & (title_col.astype(str).str.lower() == 'final')].shape[0]
    return {'matchesplayed': mp, 'won': won, 'loss': loss, 'noResult': nr, 'title': nt}


def teamAPI(team, matches_df=matches):
    df = matches_df[(matches_df['team1'] == team) | (matches_df['team2'] == team)].copy()
    self_record = allRecord(team)
    teams = matches_df['team1'].dropna().astype(str).unique()
    against = {team2: team1vsteam2(team, team2) for team2 in teams}
    data = {team: {'overall': self_record, 'against': against}}
    return json.dumps(data, cls=NpEncoder)


def batsmanRecord(batsman, df):
    if df.empty:
        return np.nan
    out = df[df['player_out'] == batsman].shape[0]
    df_b = df[df['batter'] == batsman]
    inngs = df_b['id'].nunique()
    runs = df_b['batsman_run'].sum()
    fours = df_b[(df_b['batsman_run'] == 4) & (df_b['non_boundary'] == 0)].shape[0]
    sixes = df_b[(df_b['batsman_run'] == 6) & (df_b['non_boundary'] == 0)].shape[0]
    avg = runs / out if out else np.inf
    nballs = df_b[~(df_b['extra_type'] == 'wides')].shape[0]
    strike_rate = runs / nballs * 100 if nballs else 0
    gb = df_b.groupby('id').sum(numeric_only=True)
    fifties = gb[(gb['batsman_run'] >= 50) & (gb['batsman_run'] < 100)].shape[0]
    hundreds = gb[gb['batsman_run'] >= 100].shape[0]
    try:
        highest_score = gb['batsman_run'].sort_values(ascending=False).head(1).values[0]
        hsindex = gb['batsman_run'].sort_values(ascending=False).head(1).index[0]
        if (df_b[df_b['id'] == hsindex]['player_out'] == batsman).any():
            highest_score = str(highest_score)
        else:
            highest_score = str(highest_score) + '*'
    except Exception:
        highest_score = gb['batsman_run'].max() if not gb.empty else 0
    not_out = inngs - out
    mom = df_b[df_b['player_of_match'] == batsman].drop_duplicates('id', keep='first').shape[0]
    return {
        'innings': int(inngs),
        'runs': int(runs),
        'fours': int(fours),
        'sixes': int(sixes),
        'avg': float(avg),
        'strikeRate': float(strike_rate),
        'fifties': int(fifties),
        'hundreds': int(hundreds),
        'highestScore': highest_score,
        'notOut': int(not_out),
        'mom': int(mom)
    }


def batsmanVsTeam(batsman, team, df):
    filtered = df[df['bowlingteam'] == team].copy() if 'bowlingteam' in df.columns else df.copy()
    return batsmanRecord(batsman, filtered)


def batsmanAPI(batsman, balls_df=batter_data):
    df = balls_df[balls_df['innings'].isin([1, 2])] if 'innings' in balls_df.columns else balls_df.copy()
    self_record = batsmanRecord(batsman, df=df)
    teams = matches['team1'].dropna().astype(str).unique()
    against = {team: batsmanVsTeam(batsman, team, df) for team in teams}
    data = {batsman: {'all': self_record, 'against': against}}
    return json.dumps(data, cls=NpEncoder)


bowler_data = batter_data.copy()


def bowlerRun(row):
    extra = row.get('extra_type', 'none')
    if extra in ['penalty', 'legbyes', 'byes']:
        return 0
    return row.get('total_run', 0)


bowler_data['bowler_run'] = bowler_data.apply(bowlerRun, axis=1)


def bowlerWicket(row):
    kind = row.get('kind', 'none')
    if kind in ['caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket']:
        return row.get('isWicketDelivery', 0)
    return 0


bowler_data['isBowlerWicket'] = bowler_data.apply(bowlerWicket, axis=1)


def bowlerRecord(bowler, df):
    df = df[df['bowler'] == bowler].copy()
    inngs = df['id'].nunique()
    nballs = df[~(df['extra_type'].isin(['wides', 'noballs']))].shape[0]
    runs = df['bowler_run'].sum()
    eco = runs / nballs * 6 if nballs else 0
    fours = df[(df['batsman_run'] == 4) & (df['non_boundary'] == 0)].shape[0]
    sixes = df[(df['batsman_run'] == 6) & (df['non_boundary'] == 0)].shape[0]
    wicket = df['isBowlerWicket'].sum()
    avg = runs / wicket if wicket else np.inf
    strike_rate = nballs / wicket * 100 if wicket else np.nan
    gb = df.groupby('id').sum(numeric_only=True)
    w3 = gb[(gb['isBowlerWicket'] >= 3)].shape[0]
    best_wicket = gb.sort_values(['isBowlerWicket', 'bowler_run'], ascending=[False, True])[['isBowlerWicket', 'bowler_run']].head(1).values
    best_figure = f'{best_wicket[0][0]}/{best_wicket[0][1]}' if best_wicket.size > 0 else np.nan
    mom = df[df['player_of_match'] == bowler].drop_duplicates('id', keep='first').shape[0]
    return {
        'innings': int(inngs),
        'wicket': int(wicket),
        'economy': float(eco),
        'average': float(avg),
        'strikeRate': float(strike_rate) if pd.notna(strike_rate) else np.nan,
        'fours': int(fours),
        'sixes': int(sixes),
        'best_figure': best_figure,
        '3+W': int(w3),
        'mom': int(mom)
    }


def bowlerVsTeam(bowler, team, df):
    filtered = df[df['battingteam'] == team].copy() if 'battingteam' in df.columns else df.copy()
    return bowlerRecord(bowler, filtered)


def bowlerAPI(bowler, balls_df=bowler_data):
    df = balls_df[balls_df['innings'].isin([1, 2])] if 'innings' in balls_df.columns else balls_df.copy()
    self_record = bowlerRecord(bowler, df=df)
    teams = matches['team1'].dropna().astype(str).unique()
    against = {team: bowlerVsTeam(bowler, team, df) for team in teams}
    data = {bowler: {'all': self_record, 'against': against}}
    return json.dumps(data, cls=NpEncoder)
