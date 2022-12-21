
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer34() 
	ballAt() != 3 && ballAt() != 4  

rule neverReachPlayer4AsRule(method f){
    env e; calldataarg args;

    uint256 _position = ballAt();
    require _position == 1;
    f(e, args);
    uint256 position_ = ballAt();

    assert position_ != 4, "The ball is at the hands of player 4";
}