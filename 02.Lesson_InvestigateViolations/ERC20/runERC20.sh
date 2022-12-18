CERTORA_COMMAND="certoraRun ERC20$1.sol:ERC20 --verify ERC20:ERC20.spec --solc solc --optimistic_loop --send_only \
--msg certoraRun_ERC20$1  $([ $# -ge 2 ] && shift && echo --rule $@)"

echo $CERTORA_COMMAND

$CERTORA_COMMAND