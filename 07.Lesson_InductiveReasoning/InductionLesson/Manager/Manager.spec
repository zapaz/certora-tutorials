methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}

function validFund(uint256 fundId) returns bool {
	address manager = getCurrentManager(fundId);
	return manager != 0 && isActiveManager(manager);
}

rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	require validFund(fundId1) && validFund(fundId2);
	require fundId1 != fundId2;
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);
	
	env e;
	calldataarg args;
	f(e,args);
	
	// verify that the managers are still different 
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
}
