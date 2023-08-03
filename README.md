# Infrachain Public

This repository contains the source code for the Infrachain project, an innovative solution developed during a 30-hour hackathon challenge. The project combines blockchain and IoT (Internet of Things) technologies to optimize energy consumption in the public sector.

## Challenge Description

The challenge was to conceive and develop a novel solution based on blockchain combined with IoT to further optimize the energy consumption of the government. This could be addressed by optimizing energy usage in public buildings, public infrastructure, or any other public asset.

The Infrachain project is a proof of concept (PoC) DApp running on the public sector blockchain (PSB) that demonstrates a novel way of how energy savings can be achieved in the public sector by involving IoT devices and retrieving specific information from external data sources. The DApp can include interaction with external stakeholders and favor energy-saving behaviors.

The DApp interacts with the Open Data Portal (https://data.public.lu/) to retrieve and publish data. It does not store any personal information on the chain but acts as a trust anchor between the DApp parties, with any personal information stored off-chain with the necessary data protection mechanisms in place.

## Structure

The repository is divided into two main directories:

1. `SmartContract`: This directory contains the source code for the smart contracts and the backend services.
2. `input_web`: This directory contains the data used by the backend services.

## Smart Contracts

The `SmartContract` directory contains two subdirectories:

1. `MDOT_backend_web3`: This directory contains the backend services for the project. The main file is `index.js`, which sets up an Express.js server and provides endpoints for interacting with the smart contracts.

2. `MDOT_smart_contract`: This directory contains the smart contracts for the project. There are two main contracts:

   - `CRUD.sol`: This contract provides basic CRUD operations for a mapping of strings to arrays of strings.
   - `iot.sol`: This contract provides operations for managing IoT devices and energy data. It includes methods for pushing and getting device schedules, renewable energy shares, and total energy saved.

## Data

The `input_web` directory contains the `data` subdirectory, which includes CSV files with energy data.

## Setup

To set up the project, you need to install the necessary dependencies and provide the necessary environment variables. The backend services require the Infura API key and the Ethereum private key.

## Usage

The backend services provide several endpoints for interacting with the smart contracts:

- `/push_schedule`: Pushes a device schedule to the `iot` contract.
- `/schedule`: Gets a device schedule from the `iot` contract.
- `/push_renewable_share`: Pushes a renewable energy share to the `iot` contract.
- `/get_renewable_share`: Gets a renewable energy share from the `iot` contract.
- `/push_total_energy_saved`: Pushes the total energy saved to the `iot` contract.
- `/get_total_energy_saved`: Gets the total energy saved from the `iot` contract.
