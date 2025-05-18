import React, { useState } from "react";
import PlayerCard from "./PlayerCard";
import { useDraft } from "./DraftContext";
import { Player } from "./PlayerCard";

const PlayerBox: React.FC = () => {
  const {
    availablePlayers,
    setAvailablePlayers,
    teamRosters,
    setTeamRosters,
    draftPosition,
  } = useDraft();

  const [confirmingPlayer, setConfirmingPlayer] = useState<Player | null>(null);
  const [confirmingIndex, setConfirmingIndex] = useState<number | null>(null);

  const confirmDraft = () => {
    if (confirmingIndex === null || !confirmingPlayer) return;

    const newAvailable = [...availablePlayers];
    newAvailable.splice(confirmingIndex, 1);
    setAvailablePlayers(newAvailable);

    const updatedRosters = [...teamRosters];
    updatedRosters[draftPosition] = [...updatedRosters[draftPosition], confirmingPlayer];
    setTeamRosters(updatedRosters);

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
        {availablePlayers.map((player, index) => (
          <div
            key={index}
            onClick={() => {
              setConfirmingPlayer(player);
              setConfirmingIndex(index);
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
            <h3>Draft {confirmingPlayer.name} ({confirmingPlayer.team})?</h3>
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
