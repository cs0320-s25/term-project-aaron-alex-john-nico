from flask import Flask
from flask_cors import CORS
from handlers import (
    make_add_player_handler,
    make_get_player_handler,
    make_fetch_all_players_handler,
    make_remove_player_handler,
    make_fetch_user_players_handler,
    make_fetch_opp_players_handler,
    best_player_handler
)
from playerPicker import data


def create_app():
    '''
    Creates the flask application with all of the specific configurations for our server to run on.
    '''
    app = Flask(__name__)
    CORS(app)

    # Variables to hold all of the players, user's players, and opponent's players for dependency injection.
    available_players = data # dataframe from playerPicker class that holds all players' information
    user_team = []
    opp_team = []

    # Register handlers with injected dependencies
    app.route("/add-player", methods=["GET"])(make_add_player_handler(available_players, user_team, opp_team))
    app.route("/get-player", methods=["GET"])(make_get_player_handler(available_players))
    app.route("/remove-player", methods=["GET"])(make_remove_player_handler(user_team, opp_team))
    app.route("/fetch-all-players", methods=["GET"])(make_fetch_all_players_handler(available_players))
    app.route("/fetch-user-players", methods=["GET"])(make_fetch_user_players_handler(available_players, user_team))
    app.route("/fetch-opp-players", methods=["GET"])(make_fetch_opp_players_handler(available_players, opp_team))
    app.route("/best-player", methods=["GET"])(best_player_handler(user_team, opp_team))

    return app


if __name__ == '__main__':
    port = 3232
    app = create_app()
    print(f"Server started at http://localhost:{port}")
    app.run(port=port)
