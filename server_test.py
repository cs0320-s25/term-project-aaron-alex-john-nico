import unittest
from flask.testing import FlaskClient
from server import create_app
from players import PlayerOrganizer, Player

class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client: FlaskClient = self.app.test_client()

    def test_fetch_all_players(self):
        response = self.client.get("/fetch-all-players")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # check all positions are present
        self.assertIn("QB", data)  
        self.assertIsInstance(data["QB"], list)
        self.assertIn("WR", data)  
        self.assertIsInstance(data["WR"], list)
        self.assertIn("RB", data)  # assuming at least some QBs exist
        self.assertIsInstance(data["RB"], list)
        self.assertIn("TE", data)  # assuming at least some QBs exist
        self.assertIsInstance(data["TE"], list)
        self.assertIn("D/ST", data)  # assuming at least some QBs exist
        self.assertIsInstance(data["D/ST"], list)
        self.assertIn("K", data)  # assuming at least some QBs exist
        self.assertIsInstance(data["K"], list)

    def test_get_player_valid(self):
        response = self.client.get("/get-player", query_string={"position": "QB", "name": "Patrick Mahomes"})
        self.assertEqual(response.status_code, 200)  # depends on data2024
        data = response.get_json()
        self.assertEqual(data["name"], "Patrick Mahomes")
        self.assertEqual(data["position"], "QB")

    def test_get_player_invalid(self):
        response = self.client.get("/get-player", query_string={"position": "QB", "name": "Non Existent Player"})
        self.assertEqual(response.status_code, 404)

    def test_add_and_fetch_user_player(self):
        # Add a player to the user team
        add_resp = self.client.get("/add-player", query_string={
            "position": "QB",
            "name": "Joe Burrow",
            "user": "true"
        })
        if add_resp.status_code != 200:
            self.skipTest("Joe Burrow not available in player pool")

        # Fetch user players
        fetch_resp = self.client.get("/fetch-user-players")
        self.assertEqual(fetch_resp.status_code, 200)
        user_data = fetch_resp.get_json()
        self.assertIn("QB", user_data)
        self.assertTrue(any(p["name"] == "Joe Burrow" for p in user_data["QB"]))

    def test_add_and_fetch_opp_player(self):
        # Add a player to the opponent team
        add_resp = self.client.get("/add-player", query_string={
            "position": "WR",
            "name": "Justin Jefferson",
            "user": "false"
        })
        if add_resp.status_code != 200:
            self.skipTest("Justin Jefferson not available in player pool")

        # Fetch opponent players
        fetch_resp = self.client.get("/fetch-opp-players")
        self.assertEqual(fetch_resp.status_code, 200)
        opp_data = fetch_resp.get_json()
        self.assertIn("WR", opp_data)
        self.assertTrue(any(p["name"] == "Justin Jefferson" for p in opp_data["WR"]))

    def test_add_and_remove_user_player_roundtrip(self):
        # Add
        add_resp = self.client.get("/add-player", query_string={
            "position": "RB",
            "name": "Saquon Barkley",
            "user": "true"
        })
        if add_resp.status_code != 200:
            self.skipTest("Saquon Barkley not available in player pool")

        # Confirm he's in the team
        fetch_user = self.client.get("/fetch-user-players")
        self.assertTrue(any(p["name"] == "Saquon Barkley" for p in fetch_user.get_json()["RB"]))

        # Remove
        remove_resp = self.client.get("/remove-player", query_string={
            "position": "RB",
            "name": "Saquon Barkley",
            "user": "true"
        })
        self.assertEqual(remove_resp.status_code, 200)

        # Confirm he's no longer in the team
        fetch_user_again = self.client.get("/fetch-user-players")
        self.assertFalse(any(p["name"] == "Saquon Barkley" for p in fetch_user_again.get_json()["RB"]))

        # Confirm he's back in the organizer
        get_back_resp = self.client.get("/get-player", query_string={
            "position": "RB",
            "name": "Saquon Barkley"
        })
        self.assertEqual(get_back_resp.status_code, 200)

    def test_add_and_remove_opp_player_roundtrip(self):
        # Add
        add_resp = self.client.get("/add-player", query_string={
            "position": "RB",
            "name": "Saquon Barkley",
            "user": "false"
        })
        if add_resp.status_code != 200:
            self.skipTest("Saquon Barkley not available in player pool")

        # Confirm he's in the team
        fetch_opp = self.client.get("/fetch-opp-players")
        self.assertTrue(any(p["name"] == "Saquon Barkley" for p in fetch_opp.get_json()["RB"]))

        # Remove
        remove_resp = self.client.get("/remove-player", query_string={
            "position": "RB",
            "name": "Saquon Barkley",
            "user": "false"
        })
        self.assertEqual(remove_resp.status_code, 200)

        # Confirm he's no longer in the team
        fetch_opp_again = self.client.get("/fetch-opp-players")
        self.assertFalse(any(p["name"] == "Saquon Barkley" for p in fetch_opp_again.get_json()["RB"]))

        # Confirm he's back in the organizer
        get_back_resp = self.client.get("/get-player", query_string={
            "position": "RB",
            "name": "Saquon Barkley"
        })
        self.assertEqual(get_back_resp.status_code, 200)

    def test_add_invalid_position(self):
        response = self.client.get("/remove-player", query_string={
            "position": "FAKEPOS",
            "name": "Fake Player",
            "user": "true"
        })
        self.assertEqual(response.status_code, 404)

    def test_add_player_missing_params(self):
        response = self.client.get("/add-player")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
