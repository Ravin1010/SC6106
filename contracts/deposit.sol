// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract deposit {

    address public customer;
    uint public amount;
    address public owner;

    mapping(address => uint) public balances;

    event DepositMade(address indexed user, uint amount);
    event Withdraw(address indexed owner, uint amount);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function deposit_money(address customer_add) public payable {

        require(customer_add == msg.sender, "Customer must be sender");
        require(msg.value > 0, "Send ETH");

        customer = msg.sender;
        amount = msg.value;

        balances[msg.sender] += msg.value;

        emit DepositMade(msg.sender, msg.value);
    }

    function deposit_view() public view returns (address, uint) {
        return (customer, amount);
    }

    function withdraw() public onlyOwner {
        uint contractBalance = address(this).balance;
        require(contractBalance > 0, "No funds");

        payable(owner).transfer(contractBalance);

        emit Withdraw(owner, contractBalance);
    }
}