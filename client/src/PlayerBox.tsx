import React from "react";
import PlayerCard from "./PlayerCard";
import { mockPlayers } from "./data/mockplayers";

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