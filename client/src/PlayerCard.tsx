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
        style={{
          backgroundColor: "#D5FFE5",
          borderRadius: "1.5vh",
          padding: "1vh",
          width: "10vw",
          height: "10vh",
          textAlign: "center",
          boxShadow: "0 0.3vh 1vh rgba(0,0,0,0.1)",
          fontFamily: "sans-serif",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          cursor: "default",
        }}
      >
        <div>
          <h3
            style={{
              fontSize: "1.8vh",
              margin: "0.5vh 0",
              whiteSpace: "nowrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {player.name}
          </h3>
          <p style={{ margin: 0, fontSize: "1.4vh" }}>
            {player.position}
          </p>
          <p style={{ margin: 0, fontSize: "1.2vh", color: "#555" }}>
            Proj: {player.proj_points.toFixed(2)} pts
          </p>
        </div>
        <button
          onClick={() => setModalOpen(true)}
          style={{
            marginTop: "1vh",
            padding: "0.5vh 1vh",
            backgroundColor: "#15192D",
            color: "white",
            border: "none",
            borderRadius: "1vh",
            fontSize: "1.3vh",
            cursor: "pointer",
          }}
        >
          More Info
        </button>
      </div>

      {modalOpen && (
        <PlayerInfoModal player={player} onClose={() => setModalOpen(false)} />
      )}
    </>
  );
};

export default PlayerCard;
