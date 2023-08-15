const {expect} = require('chai')
const {ethers} = require("hardhat");

describe('CRUD contract', () => {
    let CRUD, crud, owner, addr1, addr2;
    beforeEach(async () => {
        CRUD = await ethers.getContractFactory('CRUD');
        crud = await CRUD.deploy();
        [owner, addr1, addr2, _] = await ethers.getSigners();
    })
    describe('Deployment', () => {
        it('Should set the right owner', async () => {
            expect(await crud.owner()).to.equal(owner.address);
        })
    })
    describe('insert()', () => {
        it('Should insert a new key/value pair', async () => {
            const key = '123432123asdas';
            const values = ['asdasgsdfd', 'ggdfgdfgd'];
            await Promise.all(values.map(async value => await crud.pushHash(key, value)));
            const hashArray = await crud.getHashArray(key);
            expect(hashArray).to.have.members(values);
        })
        it('Should NOT insert a new key/value pair (wrong owner)', async () => {
            const key = '444444';
            const value = 'fghfghfgh';
            await expect( crud.connect(addr1).pushHash(key, value)).to.be.reverted;
        })
    })
})
