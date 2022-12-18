pragma solidity ^0.8.4;

/**
 * This example is based on a bug in Popsicle Finance which was exploited by an attacker in August 2021. https://twitter.com/PopsicleFinance/status/1422748604524019713?s=20.  The attacker managed to drain approximately $20.7 million in tokens from the project’s Sorbetto Fragola pool.
 * 
 *
 */

import {ERC20} from "./ERC20.sol";
import {Receiver} from "./Receiver.sol";
/* 
    The popsicle finance platform is used by pools liquidity providers to maximize their fees gain from providing liquidity to pools. */

contract Popsicle is ERC20 {
    event Deposit(address user_address, uint256 deposit_amount);
    event Withdraw(address user_address, uint256 withdraw_amount);
    event CollectFees(address collector, uint256 totalCollected);

    address owner;
    uint256 public currentUpdate = 1; // total fees earned per share

    mapping(address => UserInfo) public accounts;

    constructor() {
        owner = msg.sender;
    }

    struct UserInfo {
        uint256 latestUpdate;
        uint256 rewards; // general "debt" of popsicle to the user
    }

    function deposit() public payable {
        uint256 amount = msg.value;
        uint256 reward = balances[msg.sender] * (currentUpdate - accounts[msg.sender].latestUpdate);
        accounts[msg.sender].latestUpdate = currentUpdate;
        accounts[msg.sender].rewards += reward;
        mint(msg.sender, amount);
        emit Deposit(msg.sender, amount);
    }

    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        uint256 reward = amount * (currentUpdate - accounts[msg.sender].latestUpdate);
        burn(msg.sender, amount);
        accounts[msg.sender].latestUpdate = currentUpdate;
        accounts[msg.sender].rewards += reward;
        Receiver(payable(msg.sender)).acceptEth{value: amount}();
        emit Withdraw(msg.sender, amount);
    }

    function collectFees() public {
        require(currentUpdate >= accounts[msg.sender].latestUpdate);
        uint256 fee_per_share = currentUpdate - accounts[msg.sender].latestUpdate;
        uint256 to_pay = fee_per_share * balances[msg.sender] + accounts[msg.sender].rewards;
        accounts[msg.sender].latestUpdate = currentUpdate;
        accounts[msg.sender].rewards = 0;
        Receiver(payable(msg.sender)).acceptEth{value: to_pay}();
        emit CollectFees(msg.sender, to_pay);
    }

    function OwnerDoItsJobAndEarnsFeesToItsClients() public payable {
        currentUpdate += 1;
    }

    // added for spec
    function currentBalance(address user) public view returns (uint256) {
        return accounts[user].rewards + balances[user] * (currentUpdate - accounts[user].latestUpdate);
    }

    function ethBalance(address user) public view returns (uint256) {
        return user.balance;
    }
}
