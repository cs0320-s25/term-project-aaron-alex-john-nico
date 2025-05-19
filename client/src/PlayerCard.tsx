import React, { useState } from "react";
import PlayerInfoModal from "./PlayerInfoModal";

export interface Player {
  name: string;
  position: string;
  pos_rank: number;
  proj_points: number;
  bye: number;
}

const PlayerCard: React.FC<{ player: Player }> = ({ player }) => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <div
        onClick={() => setModalOpen(true)}
        style={{
          backgroundColor: "#D5FFE5",
          borderRadius: "12px",
          padding: "0.8rem",
          width: "100%",
          maxWidth: "140px",
          textAlign: "center",
          boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
          fontFamily: "sans-serif",
          cursor: "pointer",
        }}
      >
        <h3 style={{ fontSize: "1rem", margin: "0.3rem 0" }}>{player.name}</h3>
        <p style={{ margin: 0 }}>{player.position} (#{player.pos_rank})</p>
        <p style={{ margin: 0, fontSize: "0.75rem", color: "#555" }}>
          Avg: {player.proj_points.toFixed(1)} pts • Bye: {player.bye}
        </p>
      </div>

      {modalOpen && (
        <div
          onClick={() => setModalOpen(false)}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0, 0, 0, 0.6)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: "#fff",
              padding: "2rem",
              borderRadius: "10px",
              fontFamily: "sans-serif",
              maxWidth: "90%",
              textAlign: "center",
              boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
            }}
          >
            <h2>{player.name}</h2>
            <p>
              <strong>Position:</strong> {player.position}
            </p>
            <p>
              <strong>Pos Rank:</strong> #{player.pos_rank}
            </p>
            <p>
              <strong>Projected Avg:</strong> {player.proj_points.toFixed(1)} pts
            </p>
            <p>
              <strong>Bye Week:</strong> {player.bye}
            </p>
            <button
              onClick={() => setModalOpen(false)}
              style={{
                marginTop: "1rem",
                padding: "0.5rem 1rem",
                backgroundColor: "#333",
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
      )}
    </>
  );
};

  /* Mocked version
  return (
    <>
      <div
  style={{
    backgroundColor: "#D5FFE5",
    borderRadius: "12px",
    padding: "0.8rem",
    width: "100%",
    maxWidth: "140px",
    textAlign: "center",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
    fontFamily: "sans-serif",
    cursor: "pointer",
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
*/
export default PlayerCard;