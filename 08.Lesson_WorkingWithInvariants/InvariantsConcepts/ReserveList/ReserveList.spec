methods {
    getTokenAtIndex(uint256) returns (address) envfree
    getIdOfToken(address) returns (uint256) envfree
    getReserveCount() returns (uint256) envfree
    addReserve(address, address, address, uint256) envfree
    removeReserve(address) envfree
}

// check valid state around a registered index
function isValidIndexState(uint256 index) returns bool {
  return getTokenAtIndex(index) != 0 &&
  index < getReserveCount() && 
  getIdOfToken(getTokenAtIndex(index)) == index ;
}

// check valid state around a registered token
function isValidTokenState(address token) returns bool {
  return token != 0 && 
  getIdOfToken(token) < getReserveCount() &&
  getTokenAtIndex(getIdOfToken(token)) == token; 
}

// check last token, if exists, has valid state
invariant lastTokenHasValidState()
    getReserveCount() > 0 => isValidIndexState( to_uint256(getReserveCount()-1) ) 
    {
        preserved removeReserve(address tok) {
            require isValidTokenState(tok);
            // requireInvariant lastTokenHasValidState();
        }
    }

// check zero address returns id 0
invariant indexOfZeroAddressIsZero()
    getIdOfToken(0) == 0
    {
        preserved removeReserve(address tok) {
            requireInvariant lastTokenHasValidState();
        }
    }

// invariant indexNotNullPointToTokenNotNull(uint256 index)
//     0 < index && index < getReserveCount() => getTokenAtIndex(index) != 0

// // token index is less than token count (in reserves)
invariant indexLessThanCount(address token)
    getIdOfToken(token) == 0 || getIdOfToken(token) < getReserveCount()
    {
        preserved removeReserve(address tok) {
            require isValidTokenState(tok);
            require isValidTokenState(token);
            requireInvariant lastTokenHasValidState();
        }
    }

// // reserve token.id is underlying index  (token may be at address 0 and id 0)
// invariant reserveTokenIdIsUnderlyingIndex(address token)
//     getIdOfToken(token) != 0 || getTokenAtIndex(0) == token 
//      <=> 
//     getTokenAtIndex(getIdOfToken(token)) == token 
//     {
//         preserved
//         {
//             requireInvariant indexOfZeroAddressIsZero();
//             requireInvariant indexNotNullPointToTokenNotNull(getIdOfToken(token));
//             requireInvariant indexLessThanCount(token);
//         }
//     }

// invariant idOfTokenIsUnderlyingIndex(address token)
//     getIdOfToken(token) != 0 => getTokenAtIndex(getIdOfToken(token)) == token

// invariant mappingCorrelation(uint256 index, address token)
//     getTokenAtIndex(index) == token <=> getIdOfToken(token) == index