import React, { createContext, useContext, useEffect, useState } from "react";
import { Player } from "./PlayerCard";
import { mockPlayers } from "./data/mockplayers";

interface DraftContextType {
  draftPosition: number;
  setDraftPosition: (n: number) => void;
  availablePlayers: Player[];
  setAvailablePlayers: (players: Player[]) => void;
  teamRosters: Player[][];
  setTeamRosters: (rosters: Player[][]) => void;
  numTeams: number;
  setNumTeams: (n: number) => void;
}

const DraftContext = createContext<DraftContextType | undefined>(undefined);

export const DraftProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [draftPosition, setDraftPosition] = useState(0);
  const [availablePlayers, setAvailablePlayers] = useState<Player[]>(mockPlayers);
  const [numTeams, setNumTeams] = useState<number>(4);
  const [teamRosters, setTeamRosters] = useState<Player[][]>(Array.from({ length: 4 }, () => []));

  useEffect(() => {
    setTeamRosters(Array.from({ length: numTeams }, () => []));
  }, [numTeams]);

  return (
    <DraftContext.Provider
      value={{
        draftPosition,
        setDraftPosition,
        availablePlayers,
        setAvailablePlayers,
        teamRosters,
        setTeamRosters,
        numTeams,
        setNumTeams,
      }}
    >
      {children}
    </DraftContext.Provider>
  );
};

export const useDraft = () => {
  const context = useContext(DraftContext);
  if (!context) {
    throw new Error("useDraft must be used within a DraftProvider");
  }
  return context;
};
