import React from "react";
import { UserButton } from "@clerk/clerk-react";

const Navbar: React.FC = () => {
  return (
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
  );
};

export default Navbar;
