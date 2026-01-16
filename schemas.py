from typing import Any

from pydantic import BaseModel


class SPGCollectionCreate(BaseModel):
    name: str
    symbol: str
    mint_fee_recipient: str


class SPGCollectionResponse(BaseModel):
    tx_hash: str | None = None
    nft_contract: str | None = None


class IPAssetCreate(BaseModel):
    text_content: str
    asset_name: str
    asset_description: str
    spg_nft_contract_address: str
    nft_image_uri: str = "https://via.placeholder.com/150"
    nft_attributes: list[dict[str, Any]] | None = None


class IPAssetResponse(BaseModel):
    tx_hash: str | None = None
    ip_id: str | None = None
    explorer_url: str | None = None
