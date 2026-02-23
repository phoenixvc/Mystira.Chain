*This repository has been merged into Mystira.workspace. All future development happens there. This repo is archived for reference only.*

# Mystira.Chain

A lightweight **Python gRPC service** that wraps Story Protocol operations behind a simple RPC interface.

It provides two high-level capabilities:

- **Create an SPG NFT Collection** (via Story Protocol SDK)
- **Mint an NFT and register it as an IP Asset** (including generating metadata, hashing it, and optionally pinning it to IPFS)

This lets you keep Story Protocol credentials and signing logic on the server while clients call a clean, typed gRPC API.

---

## What this project does

### 1) CreateCollection
Creates an SPG NFT collection on the configured Story Protocol network and returns:

- `collection_address` (contract address)
- `transaction_hash`
- `success`

### 2) RegisterAsset
Mints an NFT into a given collection and registers it as an IP Asset, returning:

- `asset_id`
- `transaction_hash`
- `success`

During registration, the server:
- builds **NFT metadata** (name/description/image/attributes)
- builds **IP metadata** (title/description/created_at/creators/media_type/content_text)
- computes **keccak256 hashes** of those metadata payloads
- optionally uploads JSON metadata to IPFS (via Pinata) to produce URIs
- submits the mint/register transaction through the Story Protocol SDK

---

## Required gRPC metadata (credentials)

Clients must send credentials as **gRPC metadata headers** with each request.

### Required keys

| Metadata key | Required | Description |
|---|---:|---|
| `x-wallet-private-key` | Yes | The EVM private key used to sign transactions. |
| `x-rpc-provider-url` | Yes | HTTP RPC endpoint used to connect to the chain/network. |

### Optional keys

| Metadata key | Required | Description |
|---|---:|---|
| `x-pinata-jwt` | No | Pinata JWT used to upload JSON metadata to IPFS. If omitted, the server will not be able to authenticate to Pinata (and may fall back to a mock URI depending on configuration). |

**Important:** If `x-wallet-private-key` or `x-rpc-provider-url` are missing, the server will reject the request as **UNAUTHENTICATED**.

---

## Proto Files

This repository contains proto definitions for the gRPC service:

### Directory Structure

```
protos/
└── mystira/
    └── chain/
        └── v1/
            ├── chain_service.proto  # Main service definition
            └── types.proto          # Shared types and enums
story.proto                          # Legacy proto (Python server)
```

### For .NET Clients

The `protos/mystira/chain/v1/` directory contains the canonical proto definitions:

- **chain_service.proto** - `ChainService` with full CRUD operations
- **types.proto** - Shared types (`ContributorType`, `IpMetadata`, etc.)

Reference these in your `.csproj`:

```xml
<Protobuf Include="path/to/protos/mystira/chain/v1/*.proto"
          GrpcServices="Client"
          ProtoRoot="path/to/protos" />
```

### For Python Server

The root `story.proto` is used by the Python server implementation. It provides a simpler interface suitable for the current Python gRPC server.

---

## API overview (RPC surface)

The service is defined in `story.proto` (Python) and `protos/mystira/chain/v1/chain_service.proto` (.NET) and exposes:

- `CreateCollection(CreateCollectionRequest) -> CollectionResponse`
- `RegisterAsset(RegisterAssetRequest) -> AssetResponse`

### CreateCollectionRequest fields
- `name`
- `symbol`
- `mint_fee_recipient`

### RegisterAssetRequest fields
- `name`
- `description`
- `image_url`
- `text_content`
- `collection_address`

---

## gRPC “Swagger-like” tooling (Reflection + Web UI)

This project supports **gRPC Server Reflection**, which allows tools to discover services/methods at runtime (similar to how Swagger/OpenAPI tooling can explore REST APIs).

### Enable reflection on the server
Reflection requires the `grpcio-reflection` package:

- Install:
  - `pip install grpcio-reflection`

Restart the server after installing/enabling reflection.

### Web UI option: `grpcui` (closest to Swagger UI)
`grpcui` provides a browser-based UI to browse services and invoke RPCs.

1) Install `grpcui` (requires Go):
- `go install github.com/fullstorydev/grpcui/cmd/grpcui@latest`

2) Start the UI (plaintext / insecure for local dev):
- `grpcui -plaintext localhost:50051`

3) In the UI, set request metadata headers (required for authenticated calls):
- `x-wallet-private-key: <YOUR_PRIVATE_KEY>`
- `x-rpc-provider-url: <YOUR_RPC_URL>`
- `x-pinata-jwt: <YOUR_PINATA_JWT>` (optional)

### CLI option: `grpcurl` (like curl for gRPC)
Good for quick inspection and scripted calls.

1) Install `grpcurl`:
- macOS: `brew install grpcurl`
- otherwise: download a release from the grpcurl GitHub repo

2) Discover services:
- `grpcurl -plaintext localhost:50051 list`

3) Describe the service:
- `grpcurl -plaintext localhost:50051 describe story.StoryService`

4) Call an RPC with metadata headers:
- `grpcurl -plaintext \
  -H 'x-wallet-private-key: YOUR_PRIVATE_KEY' \
  -H 'x-rpc-provider-url: YOUR_RPC_URL' \
  -H 'x-pinata-jwt: YOUR_PINATA_JWT' \
  -d '{"name":"My Collection","symbol":"MYC","mint_fee_recipient":"0x..."}' \
  localhost:50051 story.StoryService/CreateCollection`

### GUI clients (no reflection required, but helpful)
These tools can import `.proto` files and call gRPC methods. Reflection can improve discovery, but you can also work purely from protos.

- **Postman (gRPC)**
- **Insomnia (gRPC)**

Typical workflow:
- Import `story.proto`
- Set server address (e.g. `localhost:50051`)
- Add metadata headers:
  - `x-wallet-private-key`
  - `x-rpc-provider-url`
  - `x-pinata-jwt` (optional)

---

## Running the project (high level)

1. **Start the gRPC server**
2. Run any gRPC client that:
   - connects to the server
   - calls the RPCs above
   - provides the required metadata keys (`x-wallet-private-key`, `x-rpc-provider-url`)
   - optionally provides `x-pinata-jwt` for real IPFS uploads

---

## Notes / operational considerations

- This project performs **transaction signing server-side** using the supplied private key.
- Metadata hashing is performed using **Keccak-256**.
- If you don’t provide `x-pinata-jwt`, IPFS uploads may not be persisted (depending on server behavior), which is fine for local testing but not for production.
- Ensure your RPC URL points to the intended network and that the funded account matches the private key.

---

## Troubleshooting

### “Missing required credentials”
You did not include one or both required metadata keys:
- `x-wallet-private-key`
- `x-rpc-provider-url`

### IPFS upload warnings / mock URIs
You likely omitted `x-pinata-jwt`, so the server can’t authenticate to Pinata.
