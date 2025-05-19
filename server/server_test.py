import unittest
from flask.testing import FlaskClient
from server import create_app

class BackendTestCase(unittest.TestCase):
    '''
    Tests the functionality of the server endpoints.
    '''
    def setUp(self):
        self.app = create_app()
        self.client: FlaskClient = self.app.test_client()

    def test_fetch_all_players(self):
        '''
        This tests the basic functionality of fetching all players.
        '''
        response = self.client.get("/fetch-all-players")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(any("player_display_name" in p for p in data))

    def test_get_player_valid(self):
        '''
        This tests if you can successfully retrieve a select player from all the players from an endpoint
        '''
        response = self.client.get("/get-player", query_string={"name": "Patrick Mahomes"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["player_display_name"], "Patrick Mahomes")

    def test_get_player_invalid(self):
        '''
        This tests if you enter incorrect data to the get player endpoint, it gives you a proper error.
        '''
        response = self.client.get("/get-player", query_string={"name": "Non Existent Player"})
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/get-player")  # Missing name
        self.assertEqual(response.status_code, 400)

    def test_add_and_fetch_user_player(self):
        '''
        Tests that if you add a player to the user team, then it properly adds to the team.
        '''
        add_resp = self.client.get("/add-player", query_string={"name": "Joe Burrow", "user": "true"})
        if add_resp.status_code != 200:
            self.skipTest("Joe Burrow not available in player pool")

        fetch_resp = self.client.get("/fetch-user-players")
        self.assertEqual(fetch_resp.status_code, 200)
        players = fetch_resp.get_json()
        self.assertTrue(any(p["player_display_name"] == "Joe Burrow" for p in players))

    def test_add_and_fetch_user_player_empty(self):
        '''
        Checks that if the user team is empty, you can still retrieve it.
        '''
        fetch_resp = self.client.get("/fetch-user-players")
        self.assertEqual(fetch_resp.status_code, 200)
        players = fetch_resp.get_json()
        self.assertIsInstance(players, list)

    def test_add_and_fetch_opp_player(self):
        '''
        Tests that if you add a player to the opponents team, then it properly adds to the team.
        '''
        add_resp = self.client.get("/add-player", query_string={"name": "Justin Jefferson", "user": "false"})
        if add_resp.status_code != 200:
            self.skipTest("Justin Jefferson not available in player pool")

        fetch_resp = self.client.get("/fetch-opp-players")
        self.assertEqual(fetch_resp.status_code, 200)
        players = fetch_resp.get_json()
        self.assertTrue(any(p["player_display_name"] == "Justin Jefferson" for p in players))

    def test_add_and_fetch_opp_player_empty(self):
        '''
        Checks that if the opponent team is empty, you can still retrieve it.
        '''
        fetch_resp = self.client.get("/fetch-opp-players")
        self.assertEqual(fetch_resp.status_code, 200)
        players = fetch_resp.get_json()
        self.assertIsInstance(players, list)

    def test_add_fake_player(self):
        '''
        Checks that if you add a fake player, then it will give you a 404 error.
        '''
        response = self.client.get("/add-player", query_string={"name": "Fake Player", "user": "true"})
        self.assertEqual(response.status_code, 404)

    def test_add_player_missing_args(self):
        '''
        Checks that if you try to add with missing parameters, then it will give you a 400 error.
        '''
        response = self.client.get("/add-player")
        self.assertEqual(response.status_code, 400)

    def test_add_and_remove_user_player_roundtrip(self):
        '''
        Checks that you can add a player to the user team, and then remove that player from the team.
        '''
        name = "Saquon Barkley"
        add_resp = self.client.get("/add-player", query_string={"name": name, "user": "true"})
        if add_resp.status_code != 200:
            self.skipTest(f"{name} not available in player pool")

        # Confirm in user team
        fetch_user = self.client.get("/fetch-user-players").get_json()
        self.assertTrue(any(p["player_display_name"] == name for p in fetch_user))

        # Remove
        remove_resp = self.client.get("/remove-player", query_string={"name": name, "user": "true"})
        self.assertEqual(remove_resp.status_code, 200)

        # Confirm removed
        fetch_user_again = self.client.get("/fetch-user-players").get_json()
        self.assertFalse(any(p["player_display_name"] == name for p in fetch_user_again))

        # Confirm player is available again
        get_back_resp = self.client.get("/get-player", query_string={"name": name})
        self.assertEqual(get_back_resp.status_code, 200)

    def test_add_and_remove_opp_player_roundtrip(self):
        '''
        Checks that you can add a player to the opponent team, and then remove that player from the team.
        '''
        name = "Saquon Barkley"
        add_resp = self.client.get("/add-player", query_string={"name": name, "user": "false"})
        if add_resp.status_code != 200:
            self.skipTest(f"{name} not available in player pool")

        # Confirm in opp team
        fetch_opp = self.client.get("/fetch-opp-players").get_json()
        self.assertTrue(any(p["player_display_name"] == name for p in fetch_opp))

        # Remove
        remove_resp = self.client.get("/remove-player", query_string={"name": name, "user": "false"})
        self.assertEqual(remove_resp.status_code, 200)

        # Confirm removed
        fetch_opp_again = self.client.get("/fetch-opp-players").get_json()
        self.assertFalse(any(p["player_display_name"] == name for p in fetch_opp_again))

        # Confirm player is available again
        get_back_resp = self.client.get("/get-player", query_string={"name": name})
        self.assertEqual(get_back_resp.status_code, 200)

    def test_remove_missing_args(self):
        '''
        Checks that if you attempt to remove a player but have missing arguments, then it will give you a 400 error.
        '''
        response = self.client.get("/remove-player", query_string={"name": "Saquon Barkley"})
        self.assertEqual(response.status_code, 400)

    def test_remove_fake_player(self):
        '''
        Checks that if you attempt to remove a fake player, then it will give you a 404 error.
        '''
        response = self.client.get("/remove-player", query_string={"name": "Fake Player", "user": "true"})
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()

