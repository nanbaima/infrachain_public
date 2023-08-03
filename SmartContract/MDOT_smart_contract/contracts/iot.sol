pragma solidity 0.8.9;

import '@openzeppelin/contracts/access/Ownable.sol';

contract iot is Ownable {
    mapping(string => string []) private userToHashArray; // Hash_map key:[v1, v2, ..., vn]
    mapping(string => uint8[]) private renewable_share; // Hash_map key:[int1, int2, ..., intn]
    mapping(string => uint16) private total_energy_saved;

    function push_on_off(string calldata key, string[] calldata values) onlyOwner external {
        // device_id: [on, on, off, ...] per 24 values // device schedule for 24h
        for (uint i = 0; i < values.length; i++) {
            userToHashArray[key].push(values[i]);
        }
    }

    function get_array(string calldata key) external view returns (string[] memory) {
        return userToHashArray[key];
    }

    function push_renewable_share(string calldata rs_key, uint8[] calldata shares) onlyOwner external {
        for (uint i = 0; i < shares.length; i++) {
            renewable_share[rs_key].push(shares[i]);
        }
    }

    function get_renewable_share(string calldata rs_key) external view returns (uint8[] memory) {
        return renewable_share[rs_key];
    }

    function push_total_energy_saved(string calldata key, uint16 value) onlyOwner external {
        total_energy_saved[key] = value;
    }

    function get_total_energy_saved(string calldata rs_key) external view returns (uint16) {
        return total_energy_saved[rs_key];
    }
}
