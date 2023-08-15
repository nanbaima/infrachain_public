//Ensure you replace the REDACTED placeholders with the actual
// values when you're deploying or testing in a secure environment.

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require('@nomiclabs/hardhat-waffle');
require('dotenv').config()
require("@nomiclabs/hardhat-etherscan");

task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();
  for (const account of accounts) {
    console.log(account.address);
  }
});

module.exports = {
  solidity: "0.8.9",
  networks: {
    goerli: {
      url: `https://goerli.infura.io/v3/REDACTED_INFURA_API_KEY`,
      accounts: [`REDACTED_METAMASK_PRIVATE_KEY`]
    }
  },
  etherscan: {
    apiKey: `REDACTED_ETHERSCAN_API_KEY`,
  }
};
