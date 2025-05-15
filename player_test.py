import unittest
from players import Player, PlayerOrganizer


class TestPlayerOrganizer(unittest.TestCase):
    def setUp(self):
        self.organizer = PlayerOrganizer()

        self.p1 = Player(name="Patrick Mahomes", position="QB", pos_rank=1, proj_points=25.5, bye=10)
        self.p2 = Player(name="Josh Allen", position="QB", pos_rank=2, proj_points=24.0, bye=11)
        self.p3 = Player(name="Justin Jefferson", position="WR", pos_rank=1, proj_points=22.0, bye=13)
        self.p4 = Player(name="Ja'Marr Chase", position="WR", pos_rank=2, proj_points=21.5, bye=7)
        self.p5 = Player(name="Brock Purdy", position="QB", pos_rank=3, proj_points=25.5, bye=10)
        self.p6 = Player(name="DJ Moore", position="WR", pos_rank=3, proj_points=24.0, bye=11)

        for p in [self.p1, self.p2, self.p3, self.p4]:
            self.organizer.add_player(p)

    def test_add_and_get_next_best_player(self):
        best_qb = self.organizer.get_next_best_player("QB")
        self.assertEqual(best_qb.name, "Patrick Mahomes")

        best_wr = self.organizer.get_next_best_player("WR")
        self.assertEqual(best_wr.name, "Justin Jefferson")

    def test_poll_next_best_player_removes_from_queue(self):
        qb = self.organizer.poll_next_best_player("QB")
        self.assertEqual(qb.name, "Patrick Mahomes")

        next_qb = self.organizer.get_next_best_player("QB")
        self.assertEqual(next_qb.name, "Josh Allen")

    def test_is_position_empty(self):
        self.assertFalse(self.organizer.is_position_empty("QB"))
        self.assertTrue(self.organizer.is_position_empty("RB"))

    def test_remove_player_by_name_success(self):
        removed = self.organizer.remove_player_by_name("Josh Allen", "QB")
        self.assertEqual(removed.name, "Josh Allen")

        # Ensure he's no longer in the list
        remaining_qbs = [p.name for p in self.organizer.player_map["QB"]]
        self.assertNotIn("Josh Allen", remaining_qbs)

    def test_remove_player_by_name_not_found(self):
        with self.assertRaises(ValueError) as context:
            self.organizer.remove_player_by_name("Lamar Jackson", "QB")
        self.assertIn("Player 'Lamar Jackson' not found", str(context.exception))

    def test_remove_player_from_invalid_position(self):
        with self.assertRaises(ValueError) as context:
            self.organizer.remove_player_by_name("Someone", "K")
        self.assertIn("No players found at position: K", str(context.exception))

    def test_get_player_by_name_success(self):
        player = self.organizer.get_player_by_name("WR", "Justin Jefferson")
        self.assertEqual(player.proj_points, 22.0)

    def test_get_player_by_name_case_insensitive(self):
        player = self.organizer.get_player_by_name("WR", "justin jefferson")
        self.assertEqual(player.name, "Justin Jefferson")

    def test_get_player_by_name_not_found(self):
        with self.assertRaises(ValueError) as context:
            self.organizer.get_player_by_name("WR", "Fake WR")
        self.assertIn("Player 'Fake WR' not found", str(context.exception))

    def test_get_player_from_invalid_position(self):
        with self.assertRaises(ValueError) as context:
            self.organizer.get_player_by_name("RB", "Anyone")
        self.assertIn("No players found at position: RB", str(context.exception))


if __name__ == '__main__':
    unittest.main()
