import Slider from '@mui/material/Slider';
import { useState } from 'react';
import MuiInput from '@mui/material/Input';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import './parameterControls.css';
import { FormControl, Grid, InputAdornment, InputLabel, MenuItem, Select } from '@mui/material';
import AvatarChip from '../AvatarChip';
import { constructorIds, driverIds, nameDirectory } from '../../services/idNameService';


const Input = styled(MuiInput)`width: 42px;`;

export default function ParameterControls({costCap, setCostCap, excludedDrivers, setExcludedDrivers, 
        excludedConstructors, setExcludedConstructors, includedDrivers, setIncludedDrivers, includedConstructors, setIncludedConstructors}) {
    const [internalCostCap, setInternalCostCap] = useState(costCap)

    // TODO: Perform sanity check or remove contradictoryy options here
    const handleExcludedDriversChange = (event) => {
        const value = event.target.value
        setExcludedDrivers(typeof value === 'string' ? value.split(',') : value,
        );
      };

    const handleExcludedConstructorsChange = (event) => {
        const value = event.target.value
        setExcludedConstructors(typeof value === 'string' ? value.split(',') : value,
        );
      };
    
    const handleIncludedConstructorsChange = (event) => {
        const value = event.target.value
        setIncludedConstructors(typeof value === 'string' ? value.split(',') : value,
        );
      };
    
    const handleIncludedDriversChange = (event) => {
        const value = event.target.value
        setIncludedDrivers(typeof value === 'string' ? value.split(',') : value,
        );
      };

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
                <Grid item xs={12} md={8}>
                    <Slider value={internalCostCap} onChange={handleChange} onBlur={handleBlur} min={0} max={200} step={0.1} valueLabelDisplay="auto" valueLabelFormat={toLabel}/> 
                </Grid>
                <Grid item xs={12} md={4}>
                    <Input className='input-field' fullWidth value={internalCostCap} min={0} max={200} type='number' onChange={handleChange} endAdornment={<InputAdornment position='end'>$ (mil)</InputAdornment>}/>
                </Grid>
                <Grid item xs={12} md={12}>
                    <FormControl className='multi-select'>
                        <InputLabel id="excludeDriversLabel">Exclude Drivers</InputLabel>
                        <Select label="Exclude Drivers" labelId='excludeDriversLabel' multiple value={excludedDrivers} onChange={handleExcludedDriversChange} 
                            renderValue={(value) => ( 
                                <div className='multi-select-display'>
                                    {
                                        value.map(id => <div key={id} className='multi-select-display-chip'> <AvatarChip id={id} /> </div>)
                                    }
                                </div>
                            )}>
                        {driverIds.map((id) => (
                            <MenuItem
                                key={id}
                                value={id}
                            >
                                {nameDirectory.get(id)}
                            </MenuItem>
                        ))}
                        </Select>
                    </FormControl>                    
                </Grid>

                <Grid item xs={12} md={12}>
                    <FormControl className='multi-select'>
                        <InputLabel id="excludeConstructorsLabel">Exclude Constructors</InputLabel>
                        <Select label="Exclude Constructors" labelId='excludeConstructorsLabel' multiple value={excludedConstructors} onChange={handleExcludedConstructorsChange} 
                            renderValue={(value) => ( 
                                <div className='multi-select-display'>
                                    {
                                        value.map(id => <div key={id} className='multi-select-display-chip'> <AvatarChip id={id} /> </div>)
                                    }
                                </div>
                            )}>
                        {constructorIds.map((id) => (
                            <MenuItem
                                key={id}
                                value={id}
                            >
                                {nameDirectory.get(id)}
                            </MenuItem>
                        ))}
                        </Select>
                    </FormControl>
                </Grid>

                <Grid item xs={12} md={12}>
                    <FormControl className='multi-select'>
                        <InputLabel id="includeDriversLabel">Include Drivers</InputLabel>
                        <Select label="Include Drivers" labelId='includeDriversLabel' multiple value={includedDrivers} onChange={handleIncludedDriversChange} 
                            renderValue={(value) => ( 
                                <div className='multi-select-display'>
                                    {
                                        value.map(id => <div key={id} className='multi-select-display-chip'> <AvatarChip id={id} /> </div>)
                                    }
                                </div>
                            )}>
                        {driverIds.map((id) => (
                            <MenuItem
                                key={id}
                                value={id}
                            >
                                {nameDirectory.get(id)}
                            </MenuItem>
                        ))}
                        </Select>
                    </FormControl>                    
                </Grid>

                <Grid item xs={12} md={12}>
                    <FormControl className='multi-select'>
                        <InputLabel id="includeConstructorsLabel">Include Constructors</InputLabel>
                        <Select label="Include Constructors" labelId='includeConstructorsLabel' multiple value={includedConstructors} onChange={handleIncludedConstructorsChange} 
                            renderValue={(value) => ( 
                                <div className='multi-select-display'>
                                    {
                                        value.map(id => <div key={id} className='multi-select-display-chip'> <AvatarChip id={id} /> </div>)
                                    }
                                </div>
                            )}>
                        {constructorIds.map((id) => (
                            <MenuItem
                                key={id}
                                value={id}
                            >
                                {nameDirectory.get(id)}
                            </MenuItem>
                        ))}
                        </Select>
                    </FormControl>
                </Grid>
            </Grid>
        </Card>
        
    )
}