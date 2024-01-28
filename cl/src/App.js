//import logo from './logo.svg';
import { useState } from 'react';
import './App.css';
import TeamDisplay from './components/TeamDisplay';
import ParameterControls from './components/parameterControls/ParameterControls';

function App() {
  const [costCap, setCostCap] = useState(100)

  return (
    <div className="App">
      <ParameterControls costCap={costCap} setCostCap={setCostCap}/>
      <TeamDisplay costCap={costCap}/>
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;
