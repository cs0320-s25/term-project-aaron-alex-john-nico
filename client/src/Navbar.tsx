import React, { useState } from "react";
import { UserButton } from "@clerk/clerk-react";
import ConfigModal from "./ConfigModal";

const Navbar: React.FC = () => {
  const [isModalOpen, setModalOpen] = useState(false);

  return (
    <>
      <div
        style={{
          backgroundColor: "#15192D",
          width: "100vw",
          height: "10vh",
          display: "flex",
          justifyContent: "flex-end",
          alignItems: "center",
        }}
      >
        <div
          onClick={() => setModalOpen(true)}
          style={{
            color: "white",
            marginRight: "1vw",
            cursor: "pointer",
            fontFamily: "sans-serif",
            fontSize: "1.1rem",
          }}
        >
          Configure Draft Settings
        </div>
        <div
          style={{
            paddingRight: "2vw",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div style={{ transform: "scale(1.6)", transformOrigin: "center" }}>
            <UserButton afterSignOutUrl="/" />
          </div>
        </div>
      </div>

      <ConfigModal isOpen={isModalOpen} onClose={() => setModalOpen(false)} title="Configure Draft Settings" />
    </>
  );
};

export default Navbar;
