require('dotenv').config();
const {ethers} = require('ethers');
const {abi} = require('../iot.json')
const provider = new ethers.providers.InfuraProvider("goerli", process.env.INFURA_API_KEY);
const wallet = new ethers.Wallet(process.env.ETHEREUM_PRIVATE_KEY, provider);
const signer = wallet.connect(provider);
const contract = new ethers.Contract(process.env.CONTRACT_ADDRESS, abi, signer);

const express = require('express')
const app = express()

app.get('/', async (req, res) => {
    try {
        res.status(200).send("Hello world\n")
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/push_schedule', async (req, res) => {
    const {key, values} = req.query
    const values_array = values.split(",");
    try {
        const result = await contract.push_on_off(key, values_array)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/schedule', async (req, res) => {
    const {key} = req.query
    try {
        const array = await contract.get_array(key)
        res.status(200).send(array)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/push_renewable_share', async (req, res) => {
    const {key, data} = req.query
    const values_array = data.split(",");
    var uint8 = [];
    for (let index = 0; index < values_array.length; index++) {
        uint8[index] = parseInt(values_array[index]);
    }
    try {
        const result = await contract.push_renewable_share(key, uint8)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/get_renewable_share', async (req, res) => {
    const {key} = req.query
    try {
        const array = await contract.get_renewable_share(key)
        res.status(200).send(array)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/push_total_energy_saved', async (req, res) => {
    const {key, value} = req.query
    try {
        const result = await contract.push_total_energy_saved(key, value)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/get_total_energy_saved', async (req, res) => {
    const {key} = req.query
    try {
        const array = await contract.get_total_energy_saved(key)
        res.status(200).send(array.toString())
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.listen(8888);
