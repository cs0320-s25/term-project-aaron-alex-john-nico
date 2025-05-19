from flask import request, jsonify
from algo import get_roster

def make_add_player_handler(available_players, user_team, opp_team):
    '''
    Arguments:
        - organizer: the dataframe that you retrieve players from
        - user_team: the user's team to add to
        - opp_team: the opponent's team to add to
    
    Returns: the add_player handler

    Makes the handler to add players to specific teams.
    '''
    def add_player():
        '''
        Handler to add a player to the user or opponent team.
        '''
        name = request.args.get("name")
        user_str = request.args.get("user")

        if name is None or user_str is None:
            return jsonify({"status": "failure", "message": "Missing Arguments."}), 400

        user = user_str.lower() == "true"

        # Already on a team?
        all_teams = user_team + opp_team
        if any(p.lower() == name.lower() for p in all_teams):
            return jsonify({"status": "failure", "message": f"{name} is already on a team."}), 409

        # Case-insensitive name match
        matched = available_players[available_players["player_display_name"].str.lower() == name.lower()]
        if not matched.empty:
            actual_name = matched.iloc[0]["player_display_name"]
            (user_team if user else opp_team).append(actual_name)
            return jsonify({"status": "success", "message": f"{actual_name} added."}), 200

        return jsonify({"status": "failure", "message": f"Could not find player {name}."}), 404

    return add_player

def make_get_player_handler(available_players):
    '''
    Arguments:
        - organizer: the dataframe that you get players from
    
    Returns: the get_player handler

    Makes the handler to retrieve a player from the dataframe.
    '''
    def get_player():
        '''
        Handler to retrieve a player and all of their information from the available_players dataframe.
        '''
        name = request.args.get("name")
        if name is None:
            return jsonify({"status": "failure", "message": "Missing Arguments."}), 400

        matched = available_players[available_players["player_display_name"].str.lower() == name.lower()]
        if matched.empty:
            return jsonify({"status": "failure", "message": f"No player found with name {name}."}), 404

        player_data = matched.iloc[0].to_dict()
        return jsonify(player_data), 200

    return get_player

def make_remove_player_handler(user_team, opp_team):
    '''
    Arguments:
        - organizer: the PlayerOrganizer that you retrieve players from
        - user_team: the user's team to remove from
        - opp_team: the opponent's team to remove from
    
    Returns: the remove_player handler

    Makes the handler to remove players from a specific team.
    '''
    def remove_player():
        name = request.args.get("name")
        user_str = request.args.get("user")

        if name is None or user_str is None:
            return jsonify({"status": "failure", "message": "Missing Arguments."}), 400

        user = user_str.lower() == "true"

        team = user_team if user else opp_team

        # Case-insensitive match
        for i, p in enumerate(team):
            if p.lower() == name.lower():
                removed = team.pop(i)
                return jsonify({"status": "success", "message": f"{removed} removed from {'user' if user else 'opponent'} team."}), 200

        return jsonify({"status": "failure", "message": f"{name} not found in {'user' if user else 'opponent'} team."}), 404

    return remove_player

def make_fetch_all_players_handler(available_players):
    '''
    Arguments:
        - available_players: the dataframe that you retrieve players from
    
    Returns: the fetch_all_players handler

    Makes the handler to fetch all the players from the PlayerOrganizer.
    '''
    def fetch_all_players():
        '''
        Handler that fetches all the players in available_players
        '''
        all_players = available_players.to_dict(orient="records")
        return jsonify(all_players), 200
    return fetch_all_players

def make_fetch_user_players_handler(available_players, user_team):
    '''
    Arguments:
        - available_players: the dataframe that you retrieve player data from
        - user_team: the list of player names on the users team
    
    Returns: the fetch_user_players handler

    Makes the handler to fetch all the players from the user's team.
    '''
    def fetch_user_players():
        '''
        Handler that fetches all the players' data from the user's team.
        '''
        # Case-insensitive match against the names in user_team
        lower_team_names = [n.lower() for n in user_team]
        filtered = available_players[available_players["player_display_name"].str.lower().isin(lower_team_names)]
        return jsonify(filtered.to_dict(orient="records")), 200
    return fetch_user_players


def make_fetch_opp_players_handler(available_players, opp_team):
    '''
    Arguments:
        - available_players: the dataframe that you retrieve player data from
        - opp_team: the list of player names on the opponent's team
    
    Returns: the fetch_user_players handler

    Makes the handler to fetch all the players from the user's team.
    '''
    def fetch_opp_players():
        '''
        Handler that fetches all the players' data from the opponent's team.
        '''
        lower_team_names = [n.lower() for n in opp_team]
        filtered = available_players[available_players["player_display_name"].str.lower().isin(lower_team_names)]
        return jsonify(filtered.to_dict(orient="records")), 200
    return fetch_opp_players

def best_player_handler(user_team, opp_team):
    def fetch_best_player():
        exclude = user_team + opp_team
        players = get_roster(exclude)
        return jsonify(players[0]), 200 
    return fetch_best_player