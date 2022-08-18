# DIAOracle Sample Contract

To use a DIA oracle in your own contract you must call one of our deployed oracle. DIA oracles are 
deployed on many EVM-chains, a complete list of deployed contracts can be found 
[here](https://docs.diadata.org/documentation/oracle-documentation/deployed-contracts).

This sample contract is written in the Vyper, a sample contract for Solidity can be found [here](https://github.com/diadata-org/DIA-integration-sample).


## Sample Contract

```
# @version ^0.3.6

ORACLE: constant(address) = 0xa93546947f3015c986695750b8bbEa8e26D65856
latestPrice: public(uint128)
timestampOfLatestPrice: public(uint128)

interface IDIAOracleV2:
    def getValue(key: String[7]) -> (uint128, uint128): nonpayable

@external
def getPriceInfo(key: String[7]):
    self.latestPrice, self.timestampOfLatestPrice = IDIAOracleV2(ORACLE).getValue(key)

@view
@external
def checkPriceAge(maxTimePassed: uint128) -> bool:
    inTime: bool = False
    if (convert(block.timestamp, uint128) - self.timestampOfLatestPrice) < maxTimePassed:
        inTime = True
    else:
        inTime = False 

    return inTime
```

The IntegrationSample contract is provided to show you how to integrate DIA oracles in your own contracts. The first step is to define
the interface of the DIAOracleV2 contract so that it can be called externally.

```
interface IDIAOracleV2:
    def getValue(key: String[7]) -> (uint128, uint128): nonpayable
``` 

In this sample contract we are using a DIA oracle deployed on the ethereum mainnet, we define
an immutable variable where the address of the oracle is saved. 

```
ORACLE: constant(address) = 0xa93546947f3015c986695750b8bbEa8e26D65856
```

We also define two storage variables to save the price and timestamp retrieved from the oracle.

```
latestPrice: public(uint128)
timestampOfLatestPrice: public(uint128)
```

To retrieve the price and timestamp from the oracle we create a function that calls the
oracle using the IDIAOracleV2 interface and the oracle address.

```
def getPriceInfo(key: String[7]):
    self.latestPrice, self.timestampOfLatestPrice = IDIAOracleV2(ORACLE).getValue(key)
```

When using an oracle it is important to know if the price has been updated recently. In the sample
contract we create a function that answers that questions. The function ```checkPriceAge``` takes an input ```maxTimePassed``` 
representing our limit on how old the price can be and returns a boolian that will be true
if the time since the price was last updates is ```< maxTimePassed``` and false otherwise.

```
@view
@external
def checkPriceAge(maxTimePassed: uint128) -> bool:
    inTime: bool = False
    if (convert(block.timestamp, uint128) - self.timestampOfLatestPrice) < maxTimePassed:
        inTime = True
    else:
        inTime = False 

    return inTime
```

# Running Tests

In addition to the sample contract unit tests are also included [here](https://github.com/tajobin/DIA-vyper-integration-sample/blob/main/tests/test_sample.py). To run them [brownie](https://github.com/eth-brownie/brownie) and [ganache](https://github.com/trufflesuite/ganache) has to be installed. 

With everything install you can run the tests with:
```
brownie test --network mainnet-fork
```

To fork mainnet you must provide a RCP_URL from a provider such as Infura. 






