import React from "react";
import { useDraft } from "./DraftContext"; // Adjust path as needed

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
}

const ConfigModal: React.FC<ModalProps> = ({ isOpen, onClose, title }) => {
  const { numTeams, setNumTeams, draftPosition, setDraftPosition } = useDraft();

  const handleNumTeamsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value);
    if (!isNaN(val) && val >= 2 && val <= 22) {
      setNumTeams(val);
      if (draftPosition > val) setDraftPosition(val);
    }
  };

  const handleDraftPositionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value);
    if (!isNaN(val) && val >= 1 && val <= numTeams) {
      setDraftPosition(val);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: "white",
          padding: "2rem",
          borderRadius: "8px",
          minWidth: "300px",
          textAlign: "center",
          fontFamily: "sans-serif",
        }}
      >
        {title && <h2>{title}</h2>}

        <form
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "1.5rem",
            fontFamily: "sans-serif",
            marginTop: "1rem",
          }}
          onSubmit={(e) => {
            e.preventDefault();
            onClose();
          }}
        >
          <div>
            <label htmlFor="numTeams" style={{ fontWeight: "bold", display: "block", marginBottom: "0.5rem" }}>
              Number of Teams
            </label>
            <input
              id="numTeams"
              type="number"
              min={2}
              value={numTeams}
              onChange={handleNumTeamsChange}
              style={{
                padding: "0.5rem",
                borderRadius: "6px",
                border: "1px solid #ccc",
                width: "100%",
              }}
            />
          </div>

          <div>
            <label htmlFor="draftPosition" style={{ fontWeight: "bold", display: "block", marginBottom: "0.5rem" }}>
              Your Draft Position
            </label>
            <input
              id="draftPosition"
              type="number"
              min={1}
              max={numTeams}
              value={draftPosition}
              onChange={handleDraftPositionChange}
              style={{
                padding: "0.5rem",
                borderRadius: "6px",
                border: "1px solid #ccc",
                width: "100%",
              }}
            />
          </div>

          <button
            type="submit"
            style={{
              padding: "0.6rem 1rem",
              backgroundColor: "#15192D",
              color: "white",
              border: "none",
              borderRadius: "6px",
              fontWeight: "bold",
              cursor: "pointer",
              marginTop: "1rem",
            }}
          >
            Save Settings
          </button>
        </form>

        <button
          onClick={onClose}
          style={{
            marginTop: "1rem",
            padding: "0.5rem 1rem",
            backgroundColor: "#ccc",
            color: "#333",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

export default ConfigModal;
