import React from "react";

interface TeamCardProps {
  teamNumber: number;
  isUserTeam: boolean;
}

const TeamCard: React.FC<TeamCardProps> = ({ teamNumber, isUserTeam }) => {
  return (
    <div
      style={{
        backgroundColor: isUserTeam ? "#5EF4C7" : "#F7A24F",
        padding: "1rem",
        borderRadius: "0.5rem",
        minWidth: "150px",
        marginRight: "1rem",
        textAlign: "center",
        fontFamily: "sans-serif",
      }}
    >
      <div style={{ fontWeight: "bold" }}>
        {`Team ${teamNumber}`}
        {isUserTeam && <div style={{ fontSize: "0.85rem" }}>You (drafting)</div>}
      </div>
      <button
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
        {isUserTeam ? "Hide Roster" : "View Roster"}
      </button>
    </div>
  );
};

export default TeamCard;
