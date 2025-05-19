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
import playerPicker
import pandas as pd


def load_data():
    ''''
    Returns:
        data - a dataframe that contains all of the information about each player.

    Loads in the data of all the players in the playerPicker class, and merges that dataframe to also include
    the predicted points from the nerual net.
    '''
    # First, drop the old column
    data = playerPicker.data.drop(columns=['fantasy_points_ppr'])
    standings = playerPicker.full_results
    
    # Merge on player_display_name
    data = data.merge(
        standings[['player_display_name', 'predicted_points']],
        on='player_display_name',
        how='left'  # keeps all players in `data`, even if not found in `standings`
    )


    # Add DST teams
    dst_teams = [
        'Den', 'Hou', 'Phi', 'Bal', 'Min', 'Det', 'Sea', 'Gre', 'Dal', 'Buf',
        'Kan', 'Cle', 'LAC', 'NYG', 'Ari', 'LAR', 'Pit', 'Ind', 'Chi', 'SF',
        'Mia', 'NYJ', 'TB', 'Was', 'NE', 'JAX', 'LV', 'ATL', 'CIN', 'CAR',
        'NO', 'TEN'
    ]

    # Create a DataFrame for DST entries
    dst_data = pd.DataFrame([{
        "attempts": 0,
        "carries": 0,
        "games": 0,
        "interceptions": 0,
        "passing_tds": 0,
        "passing_yards": 0,
        "player_display_name": f"{team} DST",
        "player_display_name_encoded": 0,  # Will be encoded later if needed
        "player_id": f"{team}_DST",
        "position": "DST",
        "position_encoded": 0,  # Will be encoded later if needed
        "predicted_points": 33,
        "receiving_fumbles": 0,
        "receiving_tds": 0,
        "receiving_yards": 0,
        "receptions": 0,
        "rushing_fumbles": 0,
        "rushing_tds": 0,
        "rushing_yards": 0,
        "sack_fumbles": 0,
        "season": 2024,
        "targets": 0,
        "team": team
    } for team in dst_teams])

    # Combine player and DST data
    data = pd.concat([data, dst_data], ignore_index=True)

    return data

def create_app():
    '''
    Creates the flask application with all of the specific configurations for our server to run on.
    '''
    app = Flask(__name__)

    #CORS(app)
    CORS(app,supports_credentials=True, origins=["http://localhost:5173"])

    

    # Variables to hold all of the players, user's players, and opponent's players for dependency injection.
    available_players = load_data() # dataframe from playerPicker class that holds all players' information
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
