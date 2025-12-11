import os
import grpc
import story_pb2
import story_pb2_grpc
from dotenv import load_dotenv

def run():
    load_dotenv()

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = story_pb2_grpc.StoryServiceStub(channel)

        metadata = (
            ('x-wallet-private-key', os.getenv('WALLET_PRIVATE_KEY')),
            ('x-rpc-provider-url', os.getenv('RPC_PROVIDER_URL')),
            ('x-pinata-jwt', os.getenv('PINATA_JWT'))
        )

        try:
            # 1. Creating a collection should only be done once. It returns an SPG address.
            #    Thereafter the SPG address must be used for minting and registering.
            response = stub.CreateCollection(
                story_pb2.CreateCollectionRequest(
                    name="Mystira Test Collection",
                    symbol="MYST",
                    mint_fee_recipient="0xecac9e29657dad1dd21cdf385a2628240f02d2a0"
                ),
                metadata=metadata
            )
            print(f"Success. Transaction Hash: {response.transaction_hash}. Collection Address: {response.collection_address}")


            # 2. Mint & Register IP Asset
            response = stub.RegisterAsset(
                story_pb2.RegisterAssetRequest(
                    name="Mystira Test Asset",
                    image_url="https://...",
                    description="My Asset Description",
                    text_content="My Asset Content",
                    collection_address=response.collection_address
                )
            )
            print(f"Success. Transaction Hash: {response.transaction_hash}. Asset ID: {response.asset_id}")

        except grpc.RpcError as e:
            # Cast to grpc.Call to hint the IDE
            if isinstance(e, grpc.Call):
                print(f"RPC failed: {e.code()} - {e.details()}")
            else:
                print(f"RPC failed: {e}")


if __name__ == '__main__':
    run()