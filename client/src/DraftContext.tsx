import React, { createContext, useContext, useEffect, useState } from "react";
import { Player } from "./PlayerCard";

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
  recommendedPlayer: Player | null;
  setRecommendedPlayer: (p: Player | null) => void;
}

const DraftContext = createContext<DraftContextType | undefined>(undefined);

export const DraftProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [draftPosition, setDraftPosition] = useState(0);
  const [availablePlayers, setAvailablePlayers] = useState<Player[]>([]);
  const [numTeams, setNumTeams] = useState<number>(4);
  const [teamRosters, setTeamRosters] = useState<Player[][]>(
    Array.from({ length: 4 }, () => [])
  );
  const [pickNumber, setPickNumber] = useState(0);
  const [recommendedPlayer, setRecommendedPlayer] = useState<Player | null>(null);

  const totalPicks = numTeams * 14;
  const isDraftComplete = pickNumber >= totalPicks;

  const currentTeamIndex = (() => {
    const round = Math.floor(pickNumber / numTeams);
    const indexInRound = pickNumber % numTeams;
    return round % 2 === 0
      ? indexInRound
      : numTeams - 1 - indexInRound;
  })();

  useEffect(() => {
    const fetchRecommendation = async () => {
      try {
        const res = await fetch("http://127.0.0.1:3232/best-player", {
          credentials: "include",
        });
        const data = await res.json();
        console.log("Fetched initial recommendation:", data);
        setRecommendedPlayer(data);
      } catch (err) {
        console.error("Failed to fetch initial recommendation:", err);
      }
    };

    fetchRecommendation();
  }, []);

  const makePick = async (player: Player, index: number) => {
    if (isDraftComplete) return;

    const isUserTeam = currentTeamIndex === draftPosition;

    try {
      const res = await fetch(
        `http://127.0.0.1:3232/add-player?name=${encodeURIComponent(player.name)}&user=${isUserTeam}`,
        {
          method: "GET",
          credentials: "include",
        }
      );

      const result = await res.json();

      if (!res.ok) {
        console.error("Backend rejected player:", result.message);
        return;
      }

      console.log("Player added on backend:", player.name);

      // Update local roster
      const newRosters = [...teamRosters];
      newRosters[currentTeamIndex] = [...newRosters[currentTeamIndex], player];
      setTeamRosters(newRosters);

      // Remove player from available pool
      const newAvailable = [...availablePlayers];
      newAvailable.splice(index, 1);
      setAvailablePlayers(newAvailable);

      setPickNumber((prev) => prev + 1);

      // Fetch new recommendation
      try {
        const recRes = await fetch("http://127.0.0.1:3232/best-player", {
          credentials: "include",
        });
        const recommendation = await recRes.json();
        console.log("Recommended player from backend:", recommendation);
        setRecommendedPlayer(recommendation);
      } catch (err) {
        console.error("Failed to fetch recommendation:", err);
        setRecommendedPlayer(null);
      }

    } catch (err) {
      console.error("Request failed:", err);
    }
  };

  useEffect(() => {
    setTeamRosters(Array.from({ length: numTeams }, () => []));
    setPickNumber(0);
  }, [numTeams]);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const res = await fetch("http://127.0.0.1:3232/fetch-all-players", {
          credentials: "include",
        });
        const data = await res.json();
        setAvailablePlayers(data);
      } catch (err) {
        console.error("Failed to fetch players:", err);
      }
    };

    fetchPlayers();
  }, []);

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
        recommendedPlayer,
        setRecommendedPlayer,
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
