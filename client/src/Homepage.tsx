import React from "react";
import { SignInButton, SignUpButton } from "@clerk/clerk-react";

const Homepage: React.FC = () => {
  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#1A1B2F",
        color: "white",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "sans-serif",
        padding: "2rem",
      }}
    >
      <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>
        Welcome to Our Fantasy Football Draft Aid
      </h1>
      <p style={{ fontSize: "1.2rem", marginBottom: "2rem", textAlign: "center", maxWidth: "600px" }}>
        Sign in or register to start your fantasy football draft with powerful analytics.
      </p>
      <div style={{ display: "flex", gap: "1rem" }}>
        <SignInButton mode="modal">
          <button
            style={{
              backgroundColor: "#4CAF50",
              color: "white",
              padding: "0.75rem 1.5rem",
              border: "none",
              borderRadius: "8px",
              fontSize: "1rem",
              cursor: "pointer",
            }}
          >
            Sign In
          </button>
        </SignInButton>
        <SignUpButton mode="modal">
          <button
            style={{
              backgroundColor: "#007BFF",
              color: "white",
              padding: "0.75rem 1.5rem",
              border: "none",
              borderRadius: "8px",
              fontSize: "1rem",
              cursor: "pointer",
            }}
          >
            Register
          </button>
        </SignUpButton>
      </div>
    </div>
  );
};

export default Homepage;
