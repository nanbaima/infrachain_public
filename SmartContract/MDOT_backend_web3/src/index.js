require('dotenv').config();
const {ethers} = require('ethers');
const {abi} = require('../iot.json')
const provider = new ethers.providers.InfuraProvider("goerli", process.env.INFURA_API_KEY);
const wallet = new ethers.Wallet(process.env.ETHEREUM_PRIVATE_KEY, provider);
const signer = wallet.connect(provider);
const contract = new ethers.Contract(process.env.CONTRACT_ADDRESS, abi, signer);
console.log(contract)

const express = require('express')
const app = express()

/*app.get('/pushHash', async (req, res) => {
    const {key, value} = req.query
    console.log("key", key)
    console.log("value", value)
    try {
        const result = await contract.pushHash(key, value)
        console.log("result", result)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/getHashArray', async (req, res) => {
    const {key} = req.query
    console.log("key", key)
    try {
        const array = await contract.getHashArray(key)
        console.log("array", array)
        res.status(200).send(array)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

*/

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
    console.log("key", key)
    const values_array = values.split(",");
    console.log("values", values_array)
    try {
        const result = await contract.push_on_off(key, values_array)
        console.log("result", result)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/schedule', async (req, res) => {
    const {key} = req.query
    console.log("key", key)
    try {
        const array = await contract.get_array(key)
        console.log("array", array)
        res.status(200).send(array)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/push_renewable_share', async (req, res) => {
    const {key, data} = req.query
    const values_array = data.split(",");
    console.log("values", values_array)
    var uint8 = [];
    //const uint8 = new Uint8Array(values_array.length);
    for (let index = 0; index < values_array.length; index++) {
        uint8[index] = parseInt(values_array[index]);
    }
    console.log("uint8", uint8)
    try {
        const result = await contract.push_renewable_share(key, uint8)
        console.log("result", result)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/get_renewable_share', async (req, res) => {
    const {key} = req.query
    console.log("key", key)
    try {
        const array = await contract.get_renewable_share(key)
        console.log("array", array)
        res.status(200).send(array)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/push_total_energy_saved', async (req, res) => {
    const {key, value} = req.query
    console.log("key", key)
    console.log("value", value)
    try {
        const result = await contract.push_total_energy_saved(key, value)
        console.log("result", result)
        res.status(200).send(result)
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.get('/get_total_energy_saved', async (req, res) => {
    const {key} = req.query
    console.log("key", key)
    try {
        const array = await contract.get_total_energy_saved(key)
        console.log("array", array)
        res.status(200).send(array.toString())
    } catch (e) {
        console.error(e)
        res.status(400).send(e)
    }
})

app.listen(8888)