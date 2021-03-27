import json
import math
import os
from hashlib import sha256
import streamlit as st

import requests
from dotenv import load_dotenv
from eth_account import Account

from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware, geth_poa_middleware


load_dotenv()


def get_abi():
    with open("abi.json", "r") as abi_file:
        abi = json.load(abi_file)
        return abi


def login_and_mint(private_key, filename):
    account = Account.from_key(private_key)
    w3 = Web3(Web3.WebsocketProvider(os.getenv("INFURA_URL")))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    w3.eth.default_account = account.address
    contract = w3.eth.contract(
        address=os.getenv("ZORA_CONTRACT_ADDRESS"), abi=get_abi()
    )
    mint('pokemon-gpt-2-output' + '/' + filename, contract, w3)


def mint(filename, contract, w3):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
    }
    files = {"file": open(filename, "rb")}
    response = requests.post(url, files=files, headers=headers, verify=False)

    asset_ipfs_hash = json.loads(response.content)["IpfsHash"]

    token_meta = {
        "asset_ipfs_hash": asset_ipfs_hash,
        "convenience_asset_url": f"https://ipfs.io/ipfs/{asset_ipfs_hash}",
    }
    token_meta_bytes = json.dumps(token_meta, indent=2).encode("utf-8")
    files = {"file": token_meta_bytes}
    response = requests.post(url, files=files, headers=headers, verify=False)
    json_ipfs_hash = json.loads(response.content)["IpfsHash"]

    token_uri = f"https://ipfs.io/ipfs/{asset_ipfs_hash}"
    metadata_uri = f"https://ipfs.io/ipfs/{json_ipfs_hash}"

    BLOCK_SIZE = 65536

    content_sha = sha256()
    with open(filename, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            content_sha.update(fb)
            fb = f.read(BLOCK_SIZE)

    content_sha = content_sha.digest()
    metadata_sha = sha256(json.dumps(token_meta).encode("utf-8")).digest()

    st.text(content_sha)
    st.text("\n")
    st.text(metadata_sha)

    share = math.pow(10, 18)
    share = int(share * 100)
    zora_data = {
        "tokenURI": token_uri,
        "metadataURI": metadata_uri,
        "contentHash": content_sha,
        "metadataHash": metadata_sha,
    }
    zora_bidshares = {
        "prevOwner": {"value": 0},
        "creator": {"value": 0},
        "owner": {"value": share},
    }

    gas_estimate = contract.functions.mint(
        data=zora_data, bidShares=zora_bidshares
    ).estimateGas()
    tx_hash = contract.functions.mint(
        data=zora_data, bidShares=zora_bidshares
    ).transact()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    st.text(token_uri)
    st.text("\n")
    st.text(metadata_uri)

    st.text(zora_data)
    st.text("\n")
    st.text(zora_bidshares)

    st.text(gas_estimate)
    st.text("\n")
    st.text(tx_hash)
    st.text("\n")
    st.text(receipt)
