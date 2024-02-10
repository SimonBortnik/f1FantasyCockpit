import { useState } from "react"
import { getOptimalTeam } from "../../services/requestService"
import { Button, Card, Typography } from "@mui/material"
import AvatarChip from "../AvatarChip"
import './TeamDisplay.css'

export default function TeamDisplay({costCap, excludedDrivers, excludedConstructors, includedDrivers, includedConstructors}) {
    const [constructors, setConstructors] = useState([])
    const [drivers, setDrivers] = useState([])
    const [cost, setCost] = useState(0)
    const [projectedPoints, setProjectedPoints] = useState(0)
    const [noSolutionFound, setNoSolutionFound] = useState(false)
    
    const handleCalculate = () => {
        getOptimalTeam(costCap, excludedDrivers, excludedConstructors, includedDrivers, includedConstructors).then((res) => {
            setConstructors(res.data.constructors)
            setDrivers(res.data.drivers)
            setCost(res.data.cost)
            setProjectedPoints(res.data.projectedPoints)
            setNoSolutionFound(false)
        })
            .catch(() => {
                setNoSolutionFound(true)
            })
    }

    const round = (num) => Math.round((num + Number.EPSILON) * 100) / 100

    const renderDrivers = () => drivers.map(id => <div key={id} className='chip'><AvatarChip id={id}/></div>)
    const renderConstructors = () => constructors.map(id => <div key={id} className='chip'><AvatarChip id={id}/></div>)

    return (
        <Card className='control-card'>
            <Typography variant="h5" component="div">
                Optimal Team
            </Typography>
            <Button onClick={handleCalculate} variant="outlined">Calculate</Button>
            {noSolutionFound && <p>No solution found, reajust paramters</p>}
            {(!noSolutionFound && cost !== 0) && <>
            <p>{round(cost)}</p>
            <div className="chip-holder">{renderDrivers()}</div>
            <div className="chip-holder">{renderConstructors()}</div>
            <p>{round(projectedPoints)}</p></>}
        </Card>
    )
}