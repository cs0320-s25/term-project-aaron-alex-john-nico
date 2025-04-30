import { useState } from "react";

const Draft: React.FC = () => {
  const [showRoster, setShowRoster] = useState(true);

  const playerCardStyle: React.CSSProperties = {
    border: "4px solid #00ff99",
    padding: "10px",
    textAlign: "center",
    background: "#222",
    borderRadius: "8px",
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0d0d1a", color: "white" }}>
      <header
        style={{
          background: "#0f1624",
          padding: "10px",
          display: "flex",
          justifyContent: "space-between",
          borderBottom: "2px solid #00f",
        }}
      >
        <h1 style={{ fontSize: "2rem", fontWeight: "bold" }}>Fantasy Draft</h1>
        <div
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "50%",
            backgroundColor: "#00ffff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "20px",
            color: "#000",
          }}
        >
          👤
        </div>
      </header>

      <div
        style={{
          display: "flex",
          gap: "10px",
          padding: "10px",
          flexWrap: "wrap",
        }}
      >
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            style={{
              background: "#f4a261",
              padding: "10px",
              borderRadius: "6px",
              width: "120px",
              color: "black",
            }}
          >
            <div>
              <strong>Team {i + 1}</strong>
            </div>
            <button style={{ width: "100%" }}>View Roster</button>
          </div>
        ))}

        <div
          style={{
            background: "#90ee90",
            padding: "10px",
            borderRadius: "6px",
            width: "120px",
            color: "black",
          }}
        >
          <div>
            <strong>Team 6</strong>
            <br />
            <small>You (drafting)</small>
          </div>
          <button
            style={{ width: "100%" }}
            onClick={() => setShowRoster(!showRoster)}
          >
            {showRoster ? "Hide Roster" : "View Roster"}
          </button>
        </div>

        <div
          style={{
            background: "#00ffff",
            borderRadius: "50%",
            width: "40px",
            height: "40px",
            fontSize: "24px",
            color: "#000",
            fontWeight: "bold",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          +
        </div>
      </div>

      <div style={{ display: "flex" }}>
        {showRoster && (
          <div
            style={{
              width: "25%",
              background: "#3498db",
              padding: "10px",
              minWidth: "150px",
            }}
          >
            <h2>Roster</h2>
            {["QB", "RB", "RB", "WR", "WR", "TE"].map((pos, idx) => (
              <div
                key={idx}
                style={{
                  background: "#eee",
                  color: "#000",
                  padding: "5px",
                  margin: "6px 0",
                  borderRadius: "4px",
                }}
              >
                {pos}
              </div>
            ))}
          </div>
        )}

        <div
          style={{
            flex: 1,
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "10px",
            padding: "10px",
          }}
        >
          <div style={playerCardStyle}>
            <img
              src="https://via.placeholder.com/40"
              alt="RB"
              style={{ borderRadius: "50%" }}
            />
            <div style={{ marginTop: "8px" }}>
              <strong>RB | 49ers</strong>
            </div>
            <button style={{ marginTop: "8px", width: "100%" }}>
              More Info
            </button>
          </div>

          {[...Array(11)].map((_, i) => (
            <div
              key={i}
              style={{
                background: "#ccc",
                height: "100px",
                borderRadius: "6px",
              }}
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Draft;