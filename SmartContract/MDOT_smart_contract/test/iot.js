const {expect} = require('chai')
const {ethers} = require("hardhat");

describe('IoT contract', () => {
    let iot_contract, iot, owner, addr1, addr2;
    beforeEach(async () => {
        iot_contract = await ethers.getContractFactory('iot');
        iot = await iot_contract.deploy();
        [owner, addr1, addr2, _] = await ethers.getSigners();
    })
    describe('Deployment', () => {
        it('Should set the right owner', async () => {
            expect(await iot.owner()).to.equal(owner.address);
        })
    })
    describe('insert() / get()', () => {
        it('push_on_off() -> Should insert a new key/values array', async () => {
            const key = '123432123asdas';
            const values = ['asdasgsdfd', 'ggdfgdfgd', 'qwerty'];
            await iot.push_on_off(key, values); // push key:[v1,v2,...]
            const array = await iot.get_array(key);
            expect(array).to.have.members(values);
        })
        it('push_on_off() -> Should NOT insert a new key/value pair (wrong owner)', async () => {
            const key = '444444';
            const value = ['fghfghfgh'];
            await expect( iot.connect(addr1).push_on_off(key, value)).to.be.reverted;
        })
        it('push_renewable_share() -> It should insert the renewable share as a 24 int array', async () => {
            const key = '123432123asdas';
            const array = [...Array(24).keys()];
            await iot.push_renewable_share(key, array);
            const ret_array = await iot.get_renewable_share(key);
            expect(ret_array).to.have.members(array);
        })
        it('push_total_energy_saved() -> It should insert total amount saved as Int', async () => {
            const key = '123432123asdas';
            const value = 33;
            await iot.push_total_energy_saved(key, value);
            const ret = await iot.get_total_energy_saved(key);
            expect(ret).to.equal(value);
        })
    })
})
