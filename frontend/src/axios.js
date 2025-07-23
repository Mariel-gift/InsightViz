// src/axios.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',  // Port du backend Flask
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json'
  }
})
api.interceptors.request.use((config) => {
  console.log('Request:', config)
  return config
})


export default api
