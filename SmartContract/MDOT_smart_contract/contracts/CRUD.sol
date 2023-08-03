pragma solidity 0.8.9;

import '@openzeppelin/contracts/access/Ownable.sol';

contract CRUD is Ownable {
    mapping(string => string []) private userToHashArray; // Hash_map key:[v1, v2, ..., vn]

    function pushHash(string calldata key, string calldata value) onlyOwner external {
        userToHashArray[key].push(value);
    }

    function getHashArray(string calldata key) external view returns (string[] memory) {
        return userToHashArray[key];
    }
}