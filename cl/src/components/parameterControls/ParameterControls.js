import Slider from '@mui/material/Slider';
import { useState } from 'react';
import MuiInput from '@mui/material/Input';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import './parameterControls.css';
import { Grid, InputAdornment } from '@mui/material';


const Input = styled(MuiInput)`width: 42px;`;

export default function ParameterControls({costCap, setCostCap}) {
    const [internalCostCap, setInternalCostCap] = useState(costCap)

    const handleChange = (e) => {
        setInternalCostCap(Number(e.target.value))
    }

    const handleBlur = e => {
        setCostCap(Number(e.target.value))
    }

    const toLabel = (val) => `${val} $ (mil)`
    return (
        <Card className='control-card'>
            <Typography variant="h5" component="div">
                Team Constraints
            </Typography>
            <Grid container>
                <Grid item xs={10}>
                    <Slider value={internalCostCap} onChange={handleChange} onBlur={handleBlur} min={0} max={200} step={0.1} valueLabelDisplay="auto" valueLabelFormat={toLabel}/> 
                </Grid>
                <Grid item xs={2}>
                    <Input value={internalCostCap} min={0} max={200} type='number' onChange={handleChange} endAdornment={<InputAdornment position='end'>$ (mil)</InputAdornment>} fullWidth className='test'/>
                </Grid>
            </Grid>
        </Card>
        
    )
}