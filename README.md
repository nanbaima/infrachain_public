# Infrachain Public

Proof-of-concept blockchain and IoT project for public-sector energy optimization.

The repository combines smart contracts, a small Web3 backend, and an input web application that works with energy data. It was created for an Infrachain/public-sector blockchain challenge and demonstrates how off-chain energy data and IoT-style inputs can be anchored or exchanged through blockchain interactions.

## Repository Layout

- `SmartContract/smart_contract/` - Hardhat project with Solidity contracts, deployment script, and tests.
- `SmartContract/smart_contract/contracts/CRUD.sol` - generic string-to-string-array CRUD contract.
- `SmartContract/smart_contract/contracts/iot.sol` - contract for device schedules, renewable-energy share, and total energy-saved values.
- `SmartContract/backend_web3/` - Express/Web3 backend that exposes HTTP endpoints for contract interaction.
- `SmartContract/backend_web3/src/index.js` - backend server entry point.
- `input_web/` - web/input prototype and local data/model artifacts.
- `input_web/data/` - CSV energy datasets used by the prototype.

## Backend Setup

```bash
cd SmartContract/backend_web3
npm ci
npm run prod
```

The backend listens on port `8888` when run through the existing compose file or `npm run prod`.

## Smart Contract Setup

```bash
cd SmartContract/smart_contract
npm ci
npm test
```

Useful scripts are defined in the smart-contract `package.json` and include compile, test, deploy, and verify workflows.

## Backend API Shape

The backend includes routes for:

- pushing and reading device schedules
- pushing and reading renewable-energy share values
- pushing and reading total energy-saved values

Check `SmartContract/backend_web3/src/index.js` for the exact route names and request payloads.

## Configuration and Secrets

Do not commit private keys, Infura/API keys, wallet mnemonics, or deployment secrets. Use `.env` or another ignored local configuration mechanism for sensitive values.

## Notes

- `package-lock.json` files are tracked and should be used with `npm ci`.
- Generated dependencies such as `node_modules/` are ignored.
- The backend Dockerfile is pinned to Node 20 and uses `npm ci`; Docker details are intentionally secondary to the local project overview here.
