import axios from 'axios';

const url = 'http://127.0.0.1:5000/'

export function getOptimalTeam(costCap) {
    return axios.get(url, {params: {
        costCap: costCap
    }})
}