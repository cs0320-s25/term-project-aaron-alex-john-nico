import React, { createContext, useContext, useEffect, useState } from "react";
import { Player } from "./PlayerCard";
import { mockPlayers } from "./data/mockplayers";

interface DraftContextType {
  draftPosition: number;
  setDraftPosition: (n: number) => void;
  availablePlayers: Player[];
  teamRosters: Player[][];
  numTeams: number;
  setNumTeams: (n: number) => void;
  isDraftComplete: boolean;
  makePick: (player: Player, index: number) => void;
  currentTeamIndex: number;
}

const DraftContext = createContext<DraftContextType | undefined>(undefined);

export const DraftProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [draftPosition, setDraftPosition] = useState(0);
  const [availablePlayers, setAvailablePlayers] = useState<Player[]>(mockPlayers);
  const [numTeams, setNumTeams] = useState<number>(4);
  const [teamRosters, setTeamRosters] = useState<Player[][]>(
    Array.from({ length: 4 }, () => [])
  );
  const [pickNumber, setPickNumber] = useState(0);

  const totalPicks = numTeams * 14;
  const isDraftComplete = pickNumber >= totalPicks;

  // Snake draft logic
  const currentTeamIndex = (() => {
    const round = Math.floor(pickNumber / numTeams);
    const indexInRound = pickNumber % numTeams;
    return round % 2 === 0
      ? indexInRound                 // left to right
      : numTeams - 1 - indexInRound; // right to left
  })();

  const makePick = (player: Player, index: number) => {
    if (isDraftComplete) return;

    const newAvailable = [...availablePlayers];
    newAvailable.splice(index, 1);
    setAvailablePlayers(newAvailable);

    const newRosters = [...teamRosters];
    newRosters[currentTeamIndex] = [...newRosters[currentTeamIndex], player];
    setTeamRosters(newRosters);

    setPickNumber(pickNumber + 1);
  };

  useEffect(() => {
    setTeamRosters(Array.from({ length: numTeams }, () => []));
    setPickNumber(0);
  }, [numTeams]);

  return (
    <DraftContext.Provider
      value={{
        draftPosition,
        setDraftPosition,
        availablePlayers,
        teamRosters,
        numTeams,
        setNumTeams,
        isDraftComplete,
        makePick,
        currentTeamIndex,
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
