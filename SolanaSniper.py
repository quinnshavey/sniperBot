# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!
# MAKE SURE TO GET A NEW PUMPPORTAL LIGHTNING WALLET AND REPLACE IT IN THE RESPONSES!!!!!!!!!!!

import sys
import os
import asyncio
import websockets
import json
import requests
import time

async def subscribe():
    count = 0
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        # Initial subscription to new tokens
        payload = {
            "method": "subscribeNewToken",
        }
        await websocket.send(json.dumps(payload)) 

        processed_token = None  # Keep track of the processed token
        buy = False
        sell = False
        step = False

        async for message in websocket:
            if count == 0:
                count += 1
                pass
            else: 
                data = json.loads(message)  # Parse the message
                specific_value = data.get("mint")  # Access the "mint" field
                '''Replace API key here'''
                response = requests.post(url="https://pumpportal.fun/api/trade?api-key=YOUR KEY", data={
                    "action": "buy",             # "buy" or "sell"
                    "mint": specific_value,      # contract address of the token you want to trade
                    "amount": 1.0,            # amount of SOL or tokens to trade
                    "denominatedInSol": "true", # "true" if amount is amount of SOL, "false" if amount is number of tokens
                    "slippage": 5,              # percent slippage allowed
                    "priorityFee": 0.0004,        # amount used to enhance transaction speed
                    "pool": "pump"               # exchange to trade on. "pump", "raydium" or "auto"
                })
                payload = {
                    "method": "subscribeTokenTrade",
                    "keys": [specific_value],  # Array of token CAs to watch
                }
                await websocket.send(json.dumps(payload))
                start = time.time()
                asyncio.create_task(sell_after_timeout(specific_value))  # New timeout task
                print("Tracking Token of ", specific_value)
                sol_buy = float(data.get("solAmount", 0))
                # Skip processing if this token was already handled
                if processed_token is not None and specific_value != processed_token:
                    print(f"Discarding duplicate token message for {specific_value}")
                    continue

                # Mark the token as processed
                processed_token = specific_value

                # Unsubscribe from new token logs after processing the first valid token
                payload = {
                    "method": "unsubscribeNewToken",
                }
                await websocket.send(json.dumps(payload))
                buy = True

                # Check if `buy` is True to handle token trade subscription
                
                if buy:
                    print(" ")
                    # Process trade subscription messages
                    async for trade_message in websocket:
                        trade_data = json.loads(trade_message)  # Parse the trade message
                        trade_type = trade_data.get("txType", "unknown")  # Access the "type" field
                        trader = trade_data.get("traderPublicKey", "unknown")
                        specific_type2 = float(trade_data.get("solAmount", 0))
                        sol_buy += specific_type2
                        if trade_type == "buy" and trader == "YOUR WALLET ADDRESS":
                            step = True
                        
                        if step and trade_type == "buy" and trader != "YOUR WALLET ADDRESS":
                            sell = True

                        if trade_type == "sell" or (time.time()-start >= 30):
                            '''Replace API key here'''
                            response = requests.post(url="https://pumpportal.fun/api/trade?api-key=YOUR KEY", data={
                                "action": "sell",             # "buy" or "sell"
                                "mint": processed_token,      # contract address of the token you want to trade
                                "amount": "100%",            # amount of SOL or tokens to trade
                                "denominatedInSol": "true", # "true" if amount is amount of SOL, "false" if amount is number of tokens
                                "slippage": 5,              # percent slippage allowed
                                "priorityFee": 0.0004,        # amount used to enhance transaction speed
                                "pool": "pump"               # exchange to trade on. "pump", "raydium" or "auto"
                            })
                            payload = {
                                "method": "unsubscribeTokenTrade",
                            }
                            await websocket.send(json.dumps(payload))
                            print("Unsubscribed from token trades.")
                            sys.exit(0)
                        elif sol_buy >= 3.0 and sell:
                            '''Replace API key here'''
                            response = requests.post(url="https://pumpportal.fun/api/trade?api-key=YOUR KEY", data={
                                "action": "sell",             # "buy" or "sell"
                                "mint": processed_token,      # contract address of the token you want to trade
                                "amount": "100%",            # amount of SOL or tokens to trade
                                "denominatedInSol": "true", # "true" if amount is amount of SOL, "false" if amount is number of tokens
                                "slippage": 7,              # percent slippage allowed
                                "priorityFee": 0.0004,        # amount used to enhance transaction speed
                                "pool": "pump"               # exchange to trade on. "pump", "raydium" or "auto"
                            })
                            payload = {
                                "method": "unsubscribeTokenTrade",
                            }
                            await websocket.send(json.dumps(payload))
                            print("Unsubscribed from token trades.")
                            sys.exit(0)
                        elif trade_type == "create":
                            continue

async def sell_after_timeout(specific_value):
    """Handles selling if 30 seconds pass without a sell trigger."""
    await asyncio.sleep(30)  # Wait for 30 seconds
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        '''Replace API key here'''
        response = requests.post(url="https://pumpportal.fun/api/trade?api-key=YOUR KEY", data={
            "action": "sell",             # "buy" or "sell"
         "mint": specific_value,      # contract address of the token you want to trade
            "amount": "100%",            # amount of SOL or tokens to trade
            "denominatedInSol": "true", # "true" if amount is amount of SOL, "false" if amount is number of tokens
            "slippage": 5,              # percent slippage allowed
            "priorityFee": 0.0001,        # amount used to enhance transaction speed
            "pool": "pump"               # exchange to trade on. "pump", "raydium" or "auto"
        })
        payload = {
            "method": "unsubscribeTokenTrade",
        }
        await websocket.send(json.dumps(payload))
        print("Unsubscribed from token trades.")
        os._exit(0)
    
                        

# Run the subscribe function
asyncio.run(subscribe())
