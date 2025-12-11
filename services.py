import json
import requests
from web3 import Web3
from story_protocol_python_sdk import StoryClient
from datetime import datetime


class IPFSService:
    """
    Service responsible for interacting with IPFS (via Pinata).
    """

    def __init__(self, jwt_token: str):
        self.jwt_token = jwt_token
        self.pinata_api_url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    def generate_keccak256_hash(self, data_dict: dict) -> str:
        """Generates a Keccak-256 hash of a dictionary."""
        json_str = json.dumps(data_dict, sort_keys=True, separators=(',', ':'))
        return Web3.keccak(text=json_str).hex()

    def upload_json(self, data_dict: dict) -> str:
        """Uploads JSON to IPFS and returns the URI."""
        if not self.jwt_token:
            print("Warning: No Pinata JWT provided for upload.")
            return "https://ipfs.io/ipfs/Qm_MOCK_CID"

        headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "pinataOptions": {"cidVersion": 1},
            "pinataContent": data_dict
        }

        try:
            response = requests.post(self.pinata_api_url, json=payload, headers=headers)
            response.raise_for_status()
            cid = response.json()['IpfsHash']
            return f"https://ipfs.io/ipfs/{cid}"
        except Exception as e:
            print(f"IPFS Upload failed: {e}")
            raise Exception(f"Failed to upload to IPFS: {str(e)}")


class StoryService:
    """
    Service responsible for interacting with the Story Protocol.
    """

    def __init__(self, private_key: str, rpc_url: str, pinata_jwt: str):
        if not private_key or not rpc_url:
            raise ValueError("Missing 'private_key' or 'rpc_url' configuration.")

        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = self.w3.eth.account.from_key(private_key)

        # Initialize SDK Client (Chain ID 1315 for Odyssey Testnet)
        self.client = StoryClient(
            account=self.account,
            web3=self.w3,
            chain_id=1315
        )

        self.ipfs_service = IPFSService(pinata_jwt)

    def create_collection(self, name: str, symbol: str, recipient: str) -> dict:
        print(f"Creating Collection: {name} ({symbol})")
        try:
            response = self.client.NFTClient.create_nft_collection(
                name=name,
                symbol=symbol,
                is_public_minting=True,
                mint_open=True,
                contract_uri="ipfs://QmYourContractMetadataURI",
                mint_fee_recipient=recipient
            )

            return {
                "tx_hash": response.get('tx_hash'),
                "nft_contract": response.get('nft_contract')
            }
        except Exception as e:
            print(f"Error creating collection: {e}")
            raise e

    def register_asset(self, asset_data) -> dict:
        """
        Mint NFT and Register IP Asset.
        """
        # 1. Prepare Metadata
        nft_metadata = {
            "name": asset_data.asset_name,
            "description": asset_data.asset_description,
            "image": asset_data.nft_image_uri,
            "attributes": asset_data.nft_attributes or []
        }

        ip_metadata = {
            "title": asset_data.asset_name,
            "description": asset_data.asset_description,
            "created_at": datetime.now().isoformat(),
            "creators": [self.account.address],
            "media_type": "text/plain",
            "content_text": asset_data.text_content
        }

        # 2. Upload to IPFS & Hash
        nft_hash = self.ipfs_service.generate_keccak256_hash(nft_metadata)
        nft_uri = self.ipfs_service.upload_json(nft_metadata)

        ip_hash = self.ipfs_service.generate_keccak256_hash(ip_metadata)
        ip_uri = self.ipfs_service.upload_json(ip_metadata)

        # 3. Mint & Register
        if not asset_data.spg_nft_contract_address.startswith("0x"):
            raise ValueError("Invalid SPG Contract Address")

        print(f"Minting IP Asset for {asset_data.asset_name}...")
        response = self.client.IPAsset.mint_and_register_ip(
            recipient=self.account.address,
            spg_nft_contract=asset_data.spg_nft_contract_address,
            ip_metadata={
                "ipMetadataURI": ip_uri,
                "ipMetadataHash": ip_hash,
                "nftMetadataURI": nft_uri,
                "nftMetadataHash": nft_hash
            }
        )

        return {
            "tx_hash": response.get('tx_hash'),
            "ip_id": response.get('ip_id'),
            "explorer_url": f"https://aeneid.storyscan.xyz/address/{response.get('ip_id')}" if response.get(
                'ip_id') else None
        }