# IPL Match Dashboard

A Flask application that exposes IPL match-data APIs and an interactive dashboard.

## Requirements

- Python 3.10 or later
- Flask
- pandas
- NumPy
- An internet connection to load the published match data. If the remote source is unavailable, `ipl.py` uses its built-in sample data.

## Setup and run

Open PowerShell in this project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Flask pandas numpy
python app.py
```

Then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a browser. The dashboard template is `templates/dashboard.html`.

If PowerShell prevents virtual-environment activation, install the packages with `python -m pip install Flask pandas numpy` and run `python app.py` without activating the environment.

## Routes

| Method | Path | Purpose |
|---|---|---|
| GET | `/` or `/dashboard` | Interactive dashboard |
| GET | `/api/health` | Application health status |
| GET | `/api/teams` | List teams |
| GET | `/api/matches` | List matches |
| GET | `/api/cities` | List match cities |
| GET | `/api/team/<team_name>` | Matches for a team |
| GET | `/api/city/<city_name>` | Matches in a city |
| GET | `/api/teamVteam/<team1>/<team2>` | Head-to-head matches |

Example API URLs:

- `http://127.0.0.1:5000/api/teams`
- `http://127.0.0.1:5000/api/team/Mumbai%20Indians`
- `http://127.0.0.1:5000/api/teamVteam/Mumbai%20Indians/Chennai%20Super%20Kings`

## Project files

- `app.py` — Flask routes and dashboard entry point
- `ipl.py` — Match-data loading and API data helpers
- `templates/dashboard.html` — Dashboard UI
