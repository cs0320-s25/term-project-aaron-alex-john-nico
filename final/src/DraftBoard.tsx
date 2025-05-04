import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import Navbar from "./Navbar";

const DraftBoard: React.FC = () => {
    return(
        <div style={{ width: "100vw", height: "100vh", backgroundColor: "#000000" }}>
            <Navbar />
            <p>Hello, world!</p>
        </div>
    );
}

export default DraftBoard;