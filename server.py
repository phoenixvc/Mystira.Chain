import logging
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

import story_pb2
import story_pb2_grpc

from services import StoryService
from schemas import IPAssetCreate


class StoryServiceServicer(story_pb2_grpc.StoryServiceServicer):
    def _get_credentials(self, context):
        """Helper to extract credentials from gRPC metadata."""
        metadata = dict(context.invocation_metadata())

        private_key = metadata.get("x-wallet-private-key")
        rpc_url = metadata.get("x-rpc-provider-url")
        pinata_jwt = metadata.get("x-pinata-jwt")

        if not private_key or not rpc_url:
            context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                "Missing required credentials (private key or RPC URL)",
            )

        return private_key, rpc_url, pinata_jwt

    def _get_service_instance(self, context):
        """Initializes the StoryService with credentials from context."""
        private_key, rpc_url, pinata_jwt = self._get_credentials(context)
        try:
            return StoryService(
                private_key=private_key,
                rpc_url=rpc_url,
                pinata_jwt=pinata_jwt,
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Failed to initialize service: {str(e)}")

    def CreateCollection(self, request, context):
        logging.info("SERVER story_pb2 loaded from: %s", story_pb2.__file__)
        service = self._get_service_instance(context)

        try:
            logging.info("Creating collection: %s", request.name)
            result = service.create_collection(
                name=request.name,
                symbol=request.symbol,
                recipient=request.mint_fee_recipient,
            )

            nft_contract = result.get("nft_contract")
            tx_hash = result.get("tx_hash")

            return story_pb2.CollectionResponse(
                collection_address=nft_contract or "",
                transaction_hash=tx_hash or "",
                success=True,
            )
        except Exception as e:
            logging.error("Error creating collection: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    def RegisterAsset(self, request, context):
        service = self._get_service_instance(context)

        try:
            asset_data = IPAssetCreate(
                asset_name=request.name,
                asset_description=request.description,
                nft_image_uri=request.image_url,
                text_content=request.text_content,
                spg_nft_contract_address=request.collection_address,
            )

            logging.info("Registering asset: %s", request.name)
            result = service.register_asset(asset_data)

            asset_id = result.get("ip_id")
            tx_hash = result.get("tx_hash")

            return story_pb2.AssetResponse(
                asset_id=asset_id or "",
                transaction_hash=tx_hash or "",
                success=True,
            )
        except ValueError as ve:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(ve))
        except Exception as e:
            logging.error("Error registering asset: %s", e)
            context.abort(grpc.StatusCode.INTERNAL, str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    story_pb2_grpc.add_StoryServiceServicer_to_server(StoryServiceServicer(), server)

    # Enable gRPC Server Reflection (for grpcui/grpcurl/Postman discovery)
    service_names = (
        story_pb2.DESCRIPTOR.services_by_name["StoryService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    address = "[::]:50051"
    server.add_insecure_port(address)
    logging.info("Server started on %s", address)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()