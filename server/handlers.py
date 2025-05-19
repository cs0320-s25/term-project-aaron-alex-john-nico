from flask import request, jsonify
from players import PlayerOrganizer, Player
import json
import subprocess
from algo import get_roster


def make_add_player_handler(organizer, user_team, opp_team):
    '''
    Arguments:
        - organizer: the PlayerOrganizer that you retrieve players from
        - user_team: the user's team to add to
        - opp_team: the opponent's team to add to
    
    Returns: the add_player handler

    Makes the handler to add players to specific teams.
    '''
    def add_player():
        '''
        Handler to add a player to the user or opponent team from the PlayerOrganizer.
        '''
        name = request.args.get("name")
        position = request.args.get("position")
        user_str = request.args.get("user")

        if name == None or position == None or user_str == None:
            return jsonify({"status": "failure", "message": "Missing Arguments."}), 400

        user = user_str.lower() == "true"

       
        try:
            player = organizer.remove_player_by_name(name, position)
        except ValueError:
            return jsonify({"status": "failure", "message": "Player not found."}), 404

        if user:
            user_team[position].append(player)
        else:
            opp_team[position].append(player)

        return jsonify({"status": "success", "message": f"{player.name} added."}), 200
    return add_player

def make_get_player_handler(organizer: PlayerOrganizer):
    '''
    Arguments:
        - organizer: the PlayerOrganizer that you get players from
    
    Returns: the get_player handler

    Makes the handler to retrieve a player from the PlayerOrganizer.
    '''
    def get_player():
        position = request.args.get("position")
        name = request.args.get("name")
        if name == None or position == None:
            return jsonify({"status": "failure", "message": "Missing Arguments."}), 400
        
        try:
            player = organizer.get_player_by_name(position, name)
        except ValueError:
            return jsonify({"message": "No player found for position."}), 404
        
        return jsonify(player.__dict__), 200
        
    return get_player

def make_remove_player_handler(organizer, user_team, opp_team):
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
        position = request.args.get("position")
        user_str = request.args.get("user")
        
        if name == None or position == None or user_str == None:
            return jsonify({"status": "failure", "message": "Missing Arguments."}), 400
        
        user = user_str.lower() == "true"

        if position not in ["QB", "WR", "RB", "TE", "D/ST", "K"]:
            return jsonify({"message": "Position not found."}), 404

        if user:
            for i in range(len(user_team[position])):
                player = user_team[position][i]
                if player.name.lower() == name.lower():
                    user_team[position].pop(i)
                    organizer.add_player(player)
                    return jsonify({"status": "success", "message": f"{player.name} added."}), 200
        else:
            for i in range(len(opp_team[position])):
                player = opp_team[position][i]
                if player.name.lower() == name.lower():
                    opp_team[position].pop(i)
                    organizer.add_player(player)
                    return jsonify({"status": "success", "message": f"{player.name} added."}), 200
        
        return jsonify({"status": "failure", "message": f"{name} not found in team."}), 404

        
    return remove_player

def make_fetch_all_players_handler(organizer: PlayerOrganizer):
    '''
    Arguments:
        - organizer: the PlayerOrganizer that you retrieve players from
    
    Returns: the fetch_all_players handler

    Makes the handler to fetch all the players from the PlayerOrganizer.
    '''
    def fetch_all_players():
        '''
        Handler that fetches all the players from the PlayerOrganizer.

        * Returns a dictionary with key values of positions. At each position is a heap where the players
          are ordered py position rank. Each player object is converted into a dictionary with all of their corresponding
          values, so all player information remains accessible
        '''
        all_players = {
            pos: [p.__dict__ for p in sorted(queue)]
            for pos, queue in organizer.player_map.items()
        }
        return jsonify(all_players), 200
    return fetch_all_players

def make_fetch_user_players_handler(user_team):
    '''
    Arguments:
        - organizer: the user's team that you retrieve players from
    
    Returns: the fetch_user_players handler

    Makes the handler to fetch all the players from the user's team.
    '''
    def fetch_user_players():
        '''
        Handler that fetches all the players from the user's team.

        * Returns a dictionary with key values of positions. At each position is a heap where the players
          are ordered py position rank. Each player object is converted into a dictionary with all of their corresponding
          values, so all player information remains accessible
        '''
        user_players = {
            pos: [p.__dict__ for p in sorted(queue)]
            for pos, queue in user_team.items()
        }
        return jsonify(user_players), 200
    return fetch_user_players

def make_fetch_opp_players_handler(opp_team):
    '''
    Arguments:
        - opp_team: the opponent's team that you retrieve players from
    
    Returns: the fetch_opp_players handler

    Makes the handler to fetch all the players from the opponent's team.
    '''
    def fetch_opp_players():
        '''
        Handler that fetches all the players from the opponent's team.

        * Returns a dictionary with key values of positions. At each position is a heap where the players
          are ordered py position rank. Each player object is converted into a dictionary with all of their corresponding
          values, so all player information remains accessible
        '''
        opp_players = {
            pos: [p.__dict__ for p in sorted(queue)]
            for pos, queue in opp_team.items()
        }
        return jsonify(opp_players), 200
    return fetch_opp_players

exclude = ["Josh Allen"]

def best_player_handler():
    def fetch_best_player():
        players = get_roster(exclude)
        exclude.append(players[0])
        return jsonify(players[0]), 200 
    return fetch_best_player