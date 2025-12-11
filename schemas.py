from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SPGCollectionCreate(BaseModel):
    name: str
    symbol: str
    mint_fee_recipient: str

class SPGCollectionResponse(BaseModel):
    tx_hash: Optional[str] = None
    nft_contract: Optional[str] = None

class IPAssetCreate(BaseModel):
    text_content: str
    asset_name: str
    asset_description: str
    spg_nft_contract_address: str
    nft_image_uri: str = "https://via.placeholder.com/150"
    nft_attributes: Optional[List[Dict[str, Any]]] = None

class IPAssetResponse(BaseModel):
    tx_hash: Optional[str] = None
    ip_id: Optional[str] = None
    explorer_url: Optional[str] = None