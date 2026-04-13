import requests

SOLANA_RPC = "https://api.mainnet-beta.solana.com"


def get_current_slot():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot"
    }

    response = requests.post(SOLANA_RPC, json=payload)
    data = response.json()

    print(data['result'])

    return data["result"]


def get_block(slot):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlock",
        "params": [
            slot,
            {
                "encoding": "json",
                "transactionDetails": "none",
                "rewards": False
            }
        ]
    }

    response = requests.post(SOLANA_RPC, json=payload)
    data = response.json()

    return data.get("result")


def get_performance_samples():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getRecentPerformanceSamples",
        "params": [5] 
    }

    response = requests.post(SOLANA_RPC, json=payload)
    data = response.json()

    return data["result"]