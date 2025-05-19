import { SignedIn, SignedOut, SignIn, SignInButton } from "@clerk/clerk-react";
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import DraftBoard from "./DraftBoard";


function App() {
  return (
  <>
  <SignedIn>
    <DraftBoard />
  </SignedIn>
  <SignedOut>
    <SignInButton />
  </SignedOut>
  </>
  );
}

export default App;
