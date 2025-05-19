import React from "react";
import { useDraft } from "./DraftContext";

interface TeamCardProps {
  teamNumber: number;
  isUserTeam: boolean;
  isCurrentTurn: boolean;
}

const TeamCard: React.FC<TeamCardProps> = ({ teamNumber, isUserTeam, isCurrentTurn }) => {
  const { setViewingRosterIndex, viewingRosterIndex } = useDraft(); // ⬅️ Add this
  const index = teamNumber - 1; // teams are 0-indexed internally
  const isViewingThisRoster = viewingRosterIndex === index;
  const bgColor = isCurrentTurn ? "#5EF4C7" : "#F7A24F";
  const scaleStyle = isCurrentTurn ? "scale(1.1)" : "scale(1)";

  return (
    <div
      style={{
        backgroundColor: bgColor,
        padding: "1rem",
        borderRadius: "0.5rem",
        minWidth: "150px",
        marginRight: "1rem",
        textAlign: "center",
        fontFamily: "sans-serif",
        transform: scaleStyle,
        transition: "transform 0.2s ease-in-out",
      }}
    >
      <div style={{ fontWeight: "bold" }}>
        {isUserTeam ? "You" : `Team ${teamNumber}`}
      </div>
      <button
        onClick={() =>
          setViewingRosterIndex(isViewingThisRoster ? null : index)
        }
        style={{
          marginTop: "0.5rem",
          padding: "0.4rem 0.8rem",
          border: "none",
          borderRadius: "4px",
          backgroundColor: isUserTeam ? "#2C4F47" : "#333",
          color: "white",
          cursor: "pointer",
        }}
      >
        {isViewingThisRoster ? "Hide Roster" : "View Roster"} 
      </button>
    </div>
  ); //changed IsViewingThisRoster ftom isUserTeam
};

export default TeamCard;
