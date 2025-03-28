# sniperBot
This bot subscribes to Pump.Fun mints and gets the mint address for the token, immediately buys it, unsubscribes from new token creations, and then subscribes to the trade logs of the mint. The program waits until someone else sells or a predetermined total of solana is entered into the bonding curve, and then the token is then sold.
After downloading the files, make sure to change the API key to your own key that you get from creating a lightning wallet from pumpportal.fun, then change the if statements on lines 86 and 89 to your new wallet address.
Also change the sol_buy to whatever solana you want to be in the bonding curve before it sells.
