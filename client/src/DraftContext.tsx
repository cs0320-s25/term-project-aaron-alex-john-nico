import React, { createContext, useContext, useState } from "react";

interface DraftContextType {
  numTeams: number;
  setNumTeams: (n: number) => void;
  draftPosition: number;
  setDraftPosition: (n: number) => void;
}

const DraftContext = createContext<DraftContextType | undefined>(undefined);

export const DraftProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [numTeams, setNumTeams] = useState(8);
  const [draftPosition, setDraftPosition] = useState(1);

  return (
    <DraftContext.Provider value={{ numTeams, setNumTeams, draftPosition, setDraftPosition }}>
      {children}
    </DraftContext.Provider>
  );
};

export const useDraft = () => {
  const context = useContext(DraftContext);
  if (!context) throw new Error("useDraft must be used within a DraftProvider");
  return context;
};

export interface TeamRoster {
    qb: string;
    rb1: string;
    rb2: string;
    wr1: string;
    wr2: string;
    te: string;
    flex: string;
    def: string;
    k: string;
    bench: string[]; // 5 bench players
};  
