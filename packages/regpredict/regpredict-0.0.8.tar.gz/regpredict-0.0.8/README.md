# Evx predictor mlbot

This is a simple package used to generate buy and sell signals for crypto and conventional stock markets based on the excess volume index(EVX)  
You can read more about EVX in the whitepaper [here](https://www.researchgate.net/publication/345313655_DeFiPaper)

# Usage

In your python script simply import the module and use as follows  
from regpredict import regbot

print(regbot.signal(20,65,120))

The above methods take an assets opening, closing, and volume of the asset based on the time interval you have chosen. A zero classification output would instruct the user not to buy or sell the asset if it is registerd in the database, while one output means buy the asset.
