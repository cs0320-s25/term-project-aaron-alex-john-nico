import React, { createContext, useContext, useEffect, useState } from "react";
import { Player } from "./PlayerCard";
import { mockPlayers } from "./data/mockplayers";

interface DraftContextType {
  draftPosition: number;
  availablePlayers: Player[];
  teamRosters: Player[][];
  numTeams: number;
  isDraftComplete: boolean;
  makePick: (player: Player, index: number) => void;
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

  const totalPicks = numTeams * 14; // assume 14 roster slots per team
  const isDraftComplete = pickNumber >= totalPicks;

  const makePick = (player: Player, index: number) => {
    if (isDraftComplete) return;

    // Remove from pool
    const newAvailable = [...availablePlayers];
    newAvailable.splice(index, 1);
    setAvailablePlayers(newAvailable);

    // Add to current team
    const newRosters = [...teamRosters];
    newRosters[draftPosition] = [...newRosters[draftPosition], player];
    setTeamRosters(newRosters);

    // Advance pick
    const nextPick = pickNumber + 1;
    setPickNumber(nextPick);

    // Snake logic: even round = left to right, odd round = right to left
    const round = Math.floor(nextPick / numTeams);
    const posInRound = nextPick % numTeams;
    const forward = round % 2 === 0;
    const nextDraftPos = forward ? posInRound : numTeams - 1 - posInRound;
    setDraftPosition(nextDraftPos);
  };

  useEffect(() => {
    setTeamRosters(Array.from({ length: numTeams }, () => []));
    setPickNumber(0);
    setDraftPosition(0);
  }, [numTeams]);

  return (
    <DraftContext.Provider
      value={{
        draftPosition,
        availablePlayers,
        teamRosters,
        numTeams,
        isDraftComplete,
        makePick,
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
