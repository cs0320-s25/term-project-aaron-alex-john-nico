import React from "react";
import { Player } from "./PlayerCard";

interface ModalProps {
  player: Player;
  onClose: () => void;
}

const PlayerInfoModal: React.FC<ModalProps> = ({ player, onClose }) => {
  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 2000,
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="playerModalTitle"
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: "white",
          padding: "2rem",
          borderRadius: "10px",
          width: "400px",
          textAlign: "center",
          fontFamily: "sans-serif",
        }}
      >
        <h2 style={{ marginBottom: "0.5rem" }}>{player.name}</h2>
        <p style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>
          {player.position} (#{player.pos_rank})
        </p>
        <p style={{ fontSize: "0.95rem", color: "#333" }}>
          Avg Projected: {player.proj_points.toFixed(1)} pts
        </p>
        <p style={{ fontSize: "0.95rem", color: "#333" }}>
          Bye Week: {player.bye === -1 ? "N/A" : player.bye}
        </p>
        <button
          onClick={onClose}
          style={{
            marginTop: "1rem",
            padding: "0.5rem 1rem",
            backgroundColor: "#15192D",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default PlayerInfoModal;
