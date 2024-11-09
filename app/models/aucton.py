from pydantic import BaseModel, Field
from typing import List, Optional

class Supplier(BaseModel):
    name: Optional[str]
    id: Optional[int]

class Customer(BaseModel):
    name: str
    id: int


class State(BaseModel):
    name: str
    id: int


class AuctionItem(BaseModel):
    currentValue: float
    costPerUnit: float
    okeiName: str
    createdOfferId: Optional[int]
    skuId: Optional[int]
    imageId: Optional[int]
    defaultImageId: Optional[int]
    okpdName: Optional[str]
    productionDirectoryName: Optional[str]
    oksm: Optional[str]
    name: Optional[str]
    id: int


class Bet(BaseModel):
    num: int
    cost: float
    serverTime: str
    isAutoBet: bool
    auctionId: int
    supplierId: int
    createUserId: int
    lastManualServerTime: Optional[str]
    supplier: Supplier
    id: int


class AuctionRegion(BaseModel):
    treePathId: str
    socr: str
    id: int
    oktmo: Optional[str]
    code: str
    name: str


class Item(BaseModel):
    currentValue: float
    costPerUnit: float
    okeiName: str
    createdOfferId: Optional[int]
    skuId: Optional[int]
    imageId: Optional[int]
    defaultImageId: Optional[int]
    okpdName: Optional[str]
    productionDirectoryName: Optional[str]
    oksm: Optional[str]
    name: str
    id: int


class DeliveryItem(BaseModel):
    sum: float
    costPerUnit: float
    quantity: float
    name: str
    buyerId: Optional[int]
    isBuyerInvitationSent: bool
    isApprovedByBuyer: Optional[bool]


class Delivery(BaseModel):
    periodDaysFrom: Optional[int]
    periodDaysTo: Optional[int]
    periodDateFrom: Optional[str]
    periodDateTo: Optional[str]
    deliveryPlace: str
    quantity: float
    items: List[DeliveryItem]
    id: int

class SupplierAutobetSetting(BaseModel):
    auctionId: int
    finalMinPrice: float
    autobetIsOn: bool
    supplierId: int
    orderNumber: int
    spUserId: int
    systemUserId: Optional[int] = None
    notShowWarningOnExceedFinalMinPrice: bool
    id: int

class File(BaseModel):
    companyId: Optional[int]
    name: str
    id: int


class Auction(BaseModel):
    customer: Customer
    createdByCustomer: Customer
    state: State
    startDate: str
    initialDuration: float
    endDate: str
    startCost: Optional[float]
    nextCost: Optional[float]
    lastBetSupplier: Optional[Supplier]
    lastBetCost: Optional[float]
    lastBetId: Optional[int]
    lastBet: Optional[Bet]
    step: float
    auctionItem: List[AuctionItem]
    bets: List[Bet]
    offerSignTime: Optional[str]
    uniqueSupplierCount: int
    auctionRegion: List[AuctionRegion]
    repeatId: Optional[int]
    unpublishName: Optional[str]
    unpublishDate: Optional[str]
    federalLawName: str
    conclusionReasonName: Optional[str]
    items: List[Item]
    deliveries: List[Delivery]
    files: List[File]
    licenseFiles: List[File]
    offersSigned: bool
    showPurchaseRequestMessageIfFailed: bool
    purchaseTypeId: int
    contractCost: Optional[float]
    contracts: List[str]
    unpublishComment: Optional[str]
    externalId: Optional[str]
    isElectronicContractExecutionRequired: bool
    isContractGuaranteeRequired: bool
    contractGuaranteeAmount: Optional[float]
    rowVersion: str
    organizingTypeId: int
    sharedPurchaseBuyers: Optional[List[Customer]]
    suppliersAutobetSettings: Optional[List[SupplierAutobetSetting]]
    isLicenseProduction: bool
    uploadLicenseDocumentsComment: Optional[str]
    isExternalIntegration: bool
    name: str
    id: int
