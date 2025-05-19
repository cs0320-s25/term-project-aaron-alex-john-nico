from flask import Flask
from flask_cors import CORS
from players import Player, PlayerOrganizer
import data2024 as data2024
import json
from handlers import (
    make_add_player_handler,
    make_get_player_handler,
    make_fetch_all_players_handler,
    make_remove_player_handler,
    make_fetch_user_players_handler,
    make_fetch_opp_players_handler,
    best_player_handler
)

avalable_players = []
our_team = []
op_team = []

# Initialize available_players as an empty list
available_players = []

# Load player names from final_standings.json
def load_available_players():
    try:
        with open('final_standings.json', 'r') as f:
            standings = json.load(f)

        # Extract player names from all positions
        for position, players in standings.items():
            for player in players:
                available_players.append(player[0])  # Extract player name
    except Exception as e:
        print(f"Error loading available players: {e}")

load_available_players()

bye_weeks = {
    "ARI": 11,
    "ATL": 12,
    "BAL": 14,
    "BUF": 12,
    "CAR": 11,
    "CHI": 7,
    "CIN": 12,
    "CLE": 10,
    "DAL": 7,
    "DEN": 14,
    "DET": 5,
    "GB": 10,
    "HOU": 14,
    "IND": 14,
    "JAX": 12,
    "KC": 6,
    "LV": 10,
    "LAC": 5,
    "LAR": 6,
    "MIA": 6,
    "MIN": 6,
    "NE": 14,
    "NO": 12,
    "NYG": 11,
    "NYJ": 12,
    "PHI": 5,
    "PIT": 9,
    "SF": 9,
    "SEA": 10,
    "TB": 11,
    "TEN": 5,
    "WAS": 14
}

# Creates Server and populates the Player Organizer
def create_app():
    app = Flask(__name__)
    CORS(app)

    # Populate organizer
    organizer = PlayerOrganizer()
    # 2024 data
    for player in data2024.player_population:
        bye = bye_weeks.get(player.proTeam, 0)
        new_player = Player(
            name=player.name,
            position=player.position,
            pos_rank=player.posRank,
            proj_points=player.projected_avg_points,
            bye=bye
        )
        organizer.add_player(new_player)

    user_team = {"QB": [], "WR": [], "RB": [], "TE": [], "D/ST": [], "K": []}
    opp_team = {"QB": [], "WR": [], "RB": [], "TE": [], "D/ST": [], "K": []}

    # Register handlers with injected dependencies
    app.route("/add-player", methods=["GET"])(make_add_player_handler(organizer, user_team, opp_team))
    app.route("/get-player", methods=["GET"])(make_get_player_handler(organizer))
    app.route("/remove-player", methods=["GET"])(make_remove_player_handler(organizer, user_team, opp_team))
    app.route("/fetch-all-players", methods=["GET"])(make_fetch_all_players_handler(organizer))
    app.route("/fetch-user-players", methods=["GET"])(make_fetch_user_players_handler(user_team))
    app.route("/fetch-opp-players", methods=["GET"])(make_fetch_opp_players_handler(opp_team))
    app.route("/best-player", methods=["GET"])(best_player_handler())

    return app


if __name__ == '__main__':
    port = 3232
    app = create_app()
    print(f"Server started at http://localhost:{port}")
    app.run(port=port)
