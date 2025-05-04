import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import Navbar from "./Navbar";
import TeamBar from "./TeamBar";

const DraftBoard: React.FC = () => {
    return(
        <div style={{ width: "100vw", height: "100vh", backgroundColor: "#000000" }}>
            <Navbar />
            <TeamBar />
            <p>Hello, world!</p>
        </div>
    );
}

export default DraftBoard;