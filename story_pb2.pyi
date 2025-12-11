from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateCollectionRequest(_message.Message):
    __slots__ = ("name", "symbol", "mint_fee_recipient")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    MINT_FEE_RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    mint_fee_recipient: str
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., mint_fee_recipient: _Optional[str] = ...) -> None: ...

class CollectionResponse(_message.Message):
    __slots__ = ("collection_address", "transaction_hash", "success")
    COLLECTION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_HASH_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    collection_address: str
    transaction_hash: str
    success: bool
    def __init__(self, collection_address: _Optional[str] = ..., transaction_hash: _Optional[str] = ..., success: bool = ...) -> None: ...

class RegisterAssetRequest(_message.Message):
    __slots__ = ("name", "description", "image_url", "text_content", "collection_address")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    TEXT_CONTENT_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    image_url: str
    text_content: str
    collection_address: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., image_url: _Optional[str] = ..., text_content: _Optional[str] = ..., collection_address: _Optional[str] = ...) -> None: ...

class AssetResponse(_message.Message):
    __slots__ = ("asset_id", "transaction_hash", "success")
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_HASH_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    asset_id: str
    transaction_hash: str
    success: bool
    def __init__(self, asset_id: _Optional[str] = ..., transaction_hash: _Optional[str] = ..., success: bool = ...) -> None: ...
