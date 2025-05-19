import React from "react";
import { useDraft } from "./DraftContext";
import TeamCard from "./TeamCard";

const TeamBar: React.FC = () => {
  const { numTeams, draftPosition, currentTeamIndex } = useDraft();

  return (
    <div
      style={{
        backgroundColor: "#15192D",
        width: "100vw",
        height: "15vh",
        overflowX: "auto",
        display: "flex",
        alignItems: "center",
        padding: "1rem",
      }}
    >
      {Array.from({ length: numTeams }, (_, i) => (
        <TeamCard
          key={i}
          teamNumber={i + 1}
          isUserTeam={i === draftPosition}
          isCurrentTurn={i === currentTeamIndex}
        />
      ))}
    </div>
  );
};

export default TeamBar;
