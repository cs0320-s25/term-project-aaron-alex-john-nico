import React, { useState } from "react";
import { useDraft } from "./DraftContext";
import { Player } from "./PlayerCard";
import PlayerInfoModal from "./PlayerInfoModal";

interface RosterSlotProps {
  position: string;
  labelColor: string;
  player?: Player;
  onClick?: () => void;
}

const RosterSlot: React.FC<RosterSlotProps> = ({ position, labelColor, player, onClick }) => {
  return (
    <div
      onClick={player ? onClick : undefined}
      style={{
        display: "flex",
        alignItems: "center",
        padding: "0.8rem 1rem",
        borderBottom: "1px solid #888",
        backgroundColor: "#1D2036",
        color: "#ccc",
        cursor: player ? "pointer" : "default",
      }}
    >
      <div
        style={{
          backgroundColor: labelColor,
          color: "#fff",
          fontWeight: "bold",
          fontSize: "0.75rem",
          padding: "0.3rem 0.6rem",
          borderRadius: "6px",
          marginRight: "1rem",
          minWidth: "50px",
          textAlign: "center",
          flexShrink: 0,
        }}
      >
        {position}
      </div>
      <div
        style={{
          flex: 1,
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {player
          ? `${player.name} (Proj Pts: ${player.proj_points.toFixed(1)}})`
          : "Empty"}
      </div>
    </div>
  );
};

const RosterBox: React.FC = () => {
  const { draftPosition, teamRosters, viewingRosterIndex } = useDraft();
  const index = viewingRosterIndex ?? draftPosition;
  const roster = teamRosters[index] || [];
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);

  const slotCounts: Record<string, number> = {
    QB: 1,
    RB: 2,
    WR: 2,
    TE: 1,
    FLEX: 1,
    DEF: 1,
    K: 1,
    BENCH: 5,
  };

  const filled: Record<string, Player[]> = {
    QB: [],
    RB: [],
    WR: [],
    TE: [],
    FLEX: [],
    DEF: [],
    K: [],
    BENCH: [],
  };

  for (const player of roster) {
    const pos = player.position;
    if (filled[pos] && filled[pos].length < slotCounts[pos]) {
      filled[pos].push(player);
    } else if (
      (pos === "RB" || pos === "WR" || pos === "TE") &&
      filled["FLEX"].length < slotCounts["FLEX"]
    ) {
      filled["FLEX"].push(player);
    } else if (filled["BENCH"].length < slotCounts["BENCH"]) {
      filled["BENCH"].push(player);
    }
  }

  const rosterSlots = [
    { pos: "QB", color: "#FF3C7E" },
    { pos: "RB", color: "#2EDFC2" },
    { pos: "RB", color: "#2EDFC2" },
    { pos: "WR", color: "#3B82F6" },
    { pos: "WR", color: "#3B82F6" },
    { pos: "TE", color: "#FBBF24" },
    { pos: "FLEX", color: "#60A5FA" },
    { pos: "DEF", color: "#6366F1" },
    { pos: "K", color: "#A855F7" },
    ...Array(5).fill({ pos: "BENCH", color: "#4B5563" }),
  ];

  const slotFillCounts: Record<string, number> = {};

  return (
    <>
      <div
        style={{
          backgroundColor: "#ACACAC",
          width: "40vw",
          height: "70vh",
          flexShrink: 0,
          overflowY: "scroll",
          overflowX: "hidden",
        }}
      >
        {rosterSlots.map((slot, index) => {
          const count = slotFillCounts[slot.pos] || 0;
          const player = filled[slot.pos][count];
          slotFillCounts[slot.pos] = count + 1;
          return (
            <RosterSlot
              key={index}
              position={slot.pos}
              labelColor={slot.color}
              player={player}
              onClick={() => player && setSelectedPlayer(player)}
            />
          );
        })}
      </div>
      {selectedPlayer && (
        <PlayerInfoModal
          player={selectedPlayer}
          onClose={() => setSelectedPlayer(null)}
        />
      )}
    </>
  );
};

export default RosterBox;
