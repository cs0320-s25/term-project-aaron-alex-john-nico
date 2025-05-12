import React, { useState } from "react";
import PlayerInfoModal from "./PlayerInfoModal";

export interface Player {
  name: string;
  position: string;
  team: string;
  imageUrl: string;
}

const PlayerCard: React.FC<{ player: Player }> = ({ player }) => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <div
  style={{
    backgroundColor: "#D5FFE5", // mint green
    borderRadius: "12px",
    padding: "0.8rem",
    width: "100%",
    maxWidth: "140px",
    textAlign: "center",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
    fontFamily: "sans-serif",
  }}
>
  <img
    src={player.imageUrl}
    alt={player.name}
    style={{
      width: "80px",
      height: "80px",
      objectFit: "cover",
      borderRadius: "50%",
      marginBottom: "0.4rem",
    }}
  />
  <div style={{ fontSize: "0.75rem", fontWeight: "bold", marginBottom: "0.3rem" }}>
    {player.position} | {player.team}
  </div>
  <button
    onClick={() => setModalOpen(true)}
    style={{
      fontSize: "0.7rem",
      padding: "0.3rem 0.6rem",
      backgroundColor: "#2E2E2E",
      color: "#fff",
      border: "none",
      borderRadius: "4px",
      cursor: "pointer",
    }}
  >
    More Information
  </button>
</div>


      {modalOpen && (
        <PlayerInfoModal player={player} onClose={() => setModalOpen(false)} />
      )}
    </>
  );
};

export default PlayerCard;