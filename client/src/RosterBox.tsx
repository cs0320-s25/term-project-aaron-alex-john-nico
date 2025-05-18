import React from "react";

interface RosterSlotProps {
  position: string;
  labelColor: string;
}

const RosterSlot: React.FC<RosterSlotProps> = ({ position, labelColor }) => {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        padding: "0.8rem 1rem",
        borderBottom: "1px solid #888",
        backgroundColor: "#1D2036",
        color: "#ccc",
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
          minWidth: "40px",
          textAlign: "center",
        }}
      >
        {position}
      </div>
      <div>Empty</div>
    </div>
  );
};

const RosterBox: React.FC = () => {
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

  return (
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
      {rosterSlots.map((slot, index) => (
        <RosterSlot key={index} position={slot.pos} labelColor={slot.color} />
      ))}
    </div>
  );
};

export default RosterBox;
