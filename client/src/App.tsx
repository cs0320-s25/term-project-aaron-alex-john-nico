import { SignedIn, SignedOut, SignIn, SignInButton } from "@clerk/clerk-react";
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import DraftBoard from "./DraftBoard";
import Homepage from "./Homepage";


function App() {
  return (
  <>
  <SignedIn>
    <DraftBoard />
  </SignedIn>
  <SignedOut>
    <Homepage />
  </SignedOut>
  </>
  );
}

export default App;
