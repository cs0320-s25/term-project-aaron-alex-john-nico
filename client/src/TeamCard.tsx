import React from "react";

interface TeamCardProps {
  teamNumber: number;
  isUserTeam: boolean;
  isCurrentTurn: boolean;
}

const TeamCard: React.FC<TeamCardProps> = ({ teamNumber, isUserTeam, isCurrentTurn }) => {
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
