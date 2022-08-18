# @version ^0.3.6

"""
 @title A sample contract showing how DIA oracles can be used in contracts.
"""

interface IDIAOracleV2:
    def getValue(key: String[7]) -> (uint128, uint128): nonpayable

ORACLE: constant(address) = 0xa93546947f3015c986695750b8bbEa8e26D65856
latestPrice: public(uint128)
timestampOfLatestPrice: public(uint128)


@external
def getPriceInfo(key: String[7]):
    """
    @dev A function that retreives the price and the corresponding timestamp
        from the DIA oracle and saves them in storage variables.
    @param key - A string specifying the asset.
    """

    self.latestPrice, self.timestampOfLatestPrice = IDIAOracleV2(ORACLE).getValue(key)

@view
@external
def checkPriceAge(maxTimePassed: uint128) -> bool:
    """
    @dev A function that checks if the timestamp of the saved price
        is older than maxTimePassed.
    @param maxTimePassed - The max acceptable amount of time passed since the
        oracle price was last updated.
    @return inTime - A bool hat will be true if the price was updated
        at most maxTimePassed seconds ago, otherwise false.
    """

    inTime: bool = False
    if (convert(block.timestamp, uint128) - self.timestampOfLatestPrice) < maxTimePassed:
        inTime = True
    else:
        inTime = False 

    return inTime
        

