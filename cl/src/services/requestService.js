import axios from 'axios';

const url = 'http://127.0.0.1:5000/'

export function getOptimalTeam(costCap, ignoreDrivers, ignoreConstructors, includeDrivers, includeConstructors) {
    const params = {
        costCap
    }
    
    if(ignoreDrivers.length !== 0)
        params['ignoreDrivers'] = JSON.stringify(ignoreDrivers)
    
    if(ignoreConstructors.length !== 0)
        params['ignoreConstructors'] = JSON.stringify(ignoreConstructors)

    if(includeDrivers.length !== 0) 
        params['includeDrivers'] = JSON.stringify(includeDrivers)

    if(includeConstructors.length !== 0) 
        params['includeConstructors'] = JSON.stringify(includeConstructors)

    return axios.get(url, {params: params})
}