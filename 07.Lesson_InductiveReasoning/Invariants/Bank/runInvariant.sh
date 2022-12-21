certoraRun BankFixed.sol:Bank --verify Bank:invariant.spec \
--send_only \
--msg "$1" --rule can_withdraw