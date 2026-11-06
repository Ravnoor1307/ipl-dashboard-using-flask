from flask import Flask, jsonify, render_template, request
import ipl

app = Flask(__name__)


@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/teams')
def teams():
    return jsonify(ipl.teams_api())


@app.route('/api/matches')
def matches():
    return jsonify(ipl.matches_api())


@app.route('/api/cities')
def cities():
    return jsonify(ipl.cities_api())


@app.route('/api/team/<team_name>')
def team_detail(team_name):
    return jsonify(ipl.team_matches_api(team_name))


@app.route('/api/city/<city_name>')
def city_detail(city_name):
    return jsonify(ipl.city_matches_api(city_name))


@app.route('/api/teamVteam/<team1>/<team2>')
def team_v_team(team1, team2):
    if team1.strip().casefold() == team2.strip().casefold():
        return jsonify({'error': 'Select two different teams.'}), 400

    result = ipl.teamVteamAPI(team1, team2)
    return jsonify(result)


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'API endpoint not found.'}), 404
    return error


if __name__ == '__main__':
    app.run(debug=True)