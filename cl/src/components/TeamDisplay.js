import { useEffect, useState } from "react"
import { getOptimalTeam } from "../services/requestService"
import { Button } from "@mui/material"

export default function TeamDisplay({costCap}) {
    const [constructors, setConstructors] = useState()
    const [drivers, setDrivers] = useState()
    const [cost, setCost] = useState()
    const [projectedPoints, setProjectedPoints] = useState()
    
    const handleCalculate= () => {
        getOptimalTeam(costCap).then((res) => {
            console.log(res)
            setConstructors(res.data.constructors)
            setDrivers(res.data.drivers)
            setCost(res.data.cost)
            setProjectedPoints(res.data.projectedPoints)

        })
    }

    return (
        <>
            <Button onClick={handleCalculate} variant="outlined">Calculate</Button>
            <p>{cost}</p>
            <p>{drivers}</p>
            <p>{constructors}</p>
            <p>{projectedPoints}</p>
        </>
    )
}