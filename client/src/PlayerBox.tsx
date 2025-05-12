import React from "react";
import PlayerCard, { Player } from "./PlayerCard";

const mockPlayers: Player[] = [
  {
    name: "Christian McCaffrey",
    position: "RB",
    team: "Texans",
    imageUrl: "https://a.espncdn.com/i/headshots/nfl/players/full/3116385.png",
  },
  {
    name: "Jamarr Chase",
    position: "WR",
    team: "Bengals",
    imageUrl: "https://a.espncdn.com/i/headshots/nfl/players/full/4362628.png",
  },
  {
    name: "Patrick Mahomes",
    position: "QB",
    team: "Chiefs",
    imageUrl: "https://a.espncdn.com/i/headshots/nfl/players/full/3139477.png",
  },
  {
    name: "Travis Kelce",
    position: "TE",
    team: "Chiefs",
    imageUrl: "https://a.espncdn.com/i/headshots/nfl/players/full/15847.png",
  },
  {
    name: "Tyreek Hill",
    position: "WR",
    team: "Dolphins",
    imageUrl: "https://a.espncdn.com/i/headshots/nfl/players/full/3116406.png",
  },
  {
    name: "Josh Allen",
    position: "QB",
    team: "Bills",
    imageUrl: "https://a.espncdn.com/i/headshots/nfl/players/full/3918298.png",
  },
];

const PlayerBox: React.FC = () => {
  return (
    <div
      style={{
        backgroundColor: "#1A1B2F",
        width: "60vw",
        height: "70vh",
        flexShrink: 0,
        overflowY: "scroll",
        overflowX: "hidden",
        padding: "1rem 3rem",
        display: "grid",
        gridTemplateColumns: "repeat(4, 1fr)",
        gap: "1rem",
        alignContent: "start",
      }}
    >
      {mockPlayers.map((player, index) => (
        <PlayerCard key={index} player={player} />
      ))}
    </div>
  );
};

export default PlayerBox;