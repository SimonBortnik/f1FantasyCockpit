//import logo from './logo.svg';
import { useState } from 'react';
import './App.css';
import TeamDisplay from './components/teamDisplay/TeamDisplay';
import ParameterControls from './components/parameterControls/ParameterControls';
import { Grid } from '@mui/material';

function App() {
  const [costCap, setCostCap] = useState(100)
  const [excludedDrivers, setExcludedDrivers] = useState([])
  const [excludedConstructors, setExcludedConstructors] = useState([])
  const [includedDrivers, setIncludedDrivers] = useState([])
  const [includedConstructors, setIncludedConstructors] = useState([])

  return (
    <div className="App">
      <Grid container spacing={4}>
        <Grid item xs={12} md={5}>
          <ParameterControls costCap={costCap} setCostCap={setCostCap} excludedDrivers={excludedDrivers} setExcludedDrivers={setExcludedDrivers} 
            excludedConstructors={excludedConstructors} setExcludedConstructors={setExcludedConstructors} 
            includedDrivers={includedDrivers} setIncludedDrivers={setIncludedDrivers}
            includedConstructors={includedConstructors} setIncludedConstructors={setIncludedConstructors}
          />
        </Grid>
        <Grid item xs={12} md={7}>
          <TeamDisplay costCap={costCap} excludedDrivers={excludedDrivers} excludedConstructors={excludedConstructors} includedDrivers={includedDrivers} includedConstructors={includedConstructors}/>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
