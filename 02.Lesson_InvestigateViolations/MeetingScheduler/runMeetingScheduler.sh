CERTORA_COMMAND="certoraRun MeetingScheduler$1.sol:MeetingScheduler \
--verify MeetingScheduler:meetings.spec --send_only \
--msg certoraRun_MeetingScheduler$1  $([ $# -ge 2 ] && shift && echo --rule $@)"

echo $CERTORA_COMMAND

$CERTORA_COMMAND