// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract paynow {

    address public payer;
    address public payee;
    uint public amount;

    // Mapping to track total amount sent by each user
    mapping(address => uint) public sentAmounts;

    // Event to log payments
    event Payment(address indexed payer, address indexed payee, uint amount);

    // Main payment function
    function weixin(address payer_add, address payable payee_add) public payable {

        // Validation checks
        require(payer_add == msg.sender, "Payer must be sender");
        require(msg.value > 0, "Send ETH");
        require(payee_add != address(0), "Invalid payee");
        require(payee_add != msg.sender, "Cannot send to self");

        // Effects (update state)
        payer = msg.sender;
        payee = payee_add;
        amount = msg.value;

        sentAmounts[msg.sender] += msg.value;

        // Interaction (transfer ETH)
        payee_add.transfer(msg.value);

        // Emit event
        emit Payment(msg.sender, payee_add, msg.value);
    }

    // View latest transaction (public)
    function check_transaction() public view returns (address, address, uint) {
        return (payer, payee, amount);
    }
}