import React from "react";
import Navbar from "./Navbar";
import TeamBar from "./TeamBar";
import RosterBox from "./RosterBox";
import PlayerBox from "./PlayerBox";

const DraftBoard: React.FC = () => {
    return(
        <div style={{ width: "100vw", height: "100vh", backgroundColor: "#000000" }}>
            <Navbar />
            <TeamBar />
            <div style={{ display: "flex", width: "100%", height: "70vh" }}>
                <RosterBox />
                <PlayerBox />
            </div>
        </div>
    );
}

export default DraftBoard;