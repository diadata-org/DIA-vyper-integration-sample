from platform import java_ver
import pytest
from brownie.test import given, strategy

"""
@title Tests for IntegrationSample 
"""

@pytest.fixture(scope="session")
def sample_contract(IntegrationSample, accounts):
    # deploy the contract with the initial value as a constructor argument
    yield IntegrationSample.deploy({'from': accounts[0]})


@pytest.fixture(scope="session")
def diaoracle(interface):
    yield interface.IDIAOracleV2('0xa93546947f3015c986695750b8bbEa8e26D65856')

def test_initial_state(sample_contract, diaoracle, accounts):
    """
     @dev Test that the storage varibles in the sample contract are
         equal to values returned from DIAOracle 
    """

    sample_contract.getPriceInfo("ETH/USD")

    latestPrice = sample_contract.latestPrice()
    timestampOfLatestPrice = sample_contract.timestampOfLatestPrice()

    latestPriceFromOracle, timestampOfLatestPriceFromOracle = diaoracle.getValue.call("ETH/USD", {'from': accounts[1]}) 

    assert latestPrice == latestPriceFromOracle
    assert timestampOfLatestPrice == timestampOfLatestPriceFromOracle

@given(maxTimePassed=strategy('uint256', max_value=100000))
def test_price_check(sample_contract, diaoracle, accounts, chain, maxTimePassed):
    """
    @dev Fuzzy test that checks if the bool returned from checkPriceAge in
        the sample contract is correct. 
    """

    sample_contract.getPriceInfo("ETH/USD")

    inTime = sample_contract.checkPriceAge.call(maxTimePassed) 

    latestPriceFromOracle, timestampOfLatestPriceFromOracle = diaoracle.getValue.call("ETH/USD", {'from': accounts[1]}) 

    if (chain[chain.height].timestamp - timestampOfLatestPriceFromOracle) < maxTimePassed:
        inTimeOracle = True;
    else: 
        inTimeOracle = False;

    assert inTimeOracle == inTime 