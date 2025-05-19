import React, { useState } from "react";
import PlayerCard, { Player } from "./PlayerCard";
import { useDraft } from "./DraftContext";

const PlayerBox: React.FC = () => {
  const {
    availablePlayers,
    makePick,
    draftPosition,
    isDraftComplete,
  } = useDraft();

  const [confirmingPlayer, setConfirmingPlayer] = useState<Player | null>(null);
  const [confirmingIndex, setConfirmingIndex] = useState<number | null>(null);

  const confirmDraft = () => {
    if (confirmingIndex === null || !confirmingPlayer) return;
    makePick(confirmingPlayer, confirmingIndex);
    setConfirmingPlayer(null);
    setConfirmingIndex(null);
  };

  return (
    <>
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
        {Array.isArray(availablePlayers) &&
        [...availablePlayers]
          .sort((a, b) => b.proj_points - a.proj_points)
          .map((player, index) => (
            <div
              key={index}
              onClick={() => {
                if (!isDraftComplete) {
                  setConfirmingPlayer(player);
                  setConfirmingIndex(index);
                }
              }}
            >
              <PlayerCard player={player} />
            </div>
      ))}

      </div>

      {confirmingPlayer && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0,0,0,0.6)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
          onClick={() => {
            setConfirmingPlayer(null);
            setConfirmingIndex(null);
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: "#fff",
              padding: "2rem",
              borderRadius: "10px",
              fontFamily: "sans-serif",
              textAlign: "center",
              boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
              maxWidth: "90%",
            }}
          >
            <h3>
              Draft {confirmingPlayer.name} (
              {confirmingPlayer.position} #{confirmingPlayer.pos_rank})?
            </h3>
            <p style={{ fontSize: "0.9rem", color: "#444" }}>
              Avg: {confirmingPlayer.proj_points.toFixed(1)} pts • Bye:{" "}
              {confirmingPlayer.bye}
            </p>
            <div style={{ marginTop: "1rem" }}>
              <button
                onClick={confirmDraft}
                style={{
                  backgroundColor: "#4CAF50",
                  color: "white",
                  padding: "0.5rem 1rem",
                  marginRight: "1rem",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
              >
                Confirm
              </button>
              <button
                onClick={() => {
                  setConfirmingPlayer(null);
                  setConfirmingIndex(null);
                }}
                style={{
                  backgroundColor: "#ccc",
                  padding: "0.5rem 1rem",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default PlayerBox;