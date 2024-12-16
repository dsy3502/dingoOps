# 数据表对应的model对象

from __future__ import annotations

from sqlalchemy import JSON, Column, MetaData, String, Table, Text, DateTime, Integer, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 资产对象
class Asset(Base):
    __tablename__ = "ops_assets"

    uuid = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_name = Column(String(length=128), nullable=True)
    asset_description = Column(String(length=255), nullable=True)


# 资产类型信息对象
class AssetType(Base):
    __tablename__ = "ops_assets_types"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    parent_id = Column(String(length=128), nullable=True)
    asset_type_name = Column(String(length=128), nullable=True)
    asset_type_name_zh = Column(String(length=128), nullable=True)
    queue = Column(Integer, default=0, nullable= False)
    description = Column(String(length=255), nullable=True)


# 资产基础信息对象
class AssetBasicInfo(Base):
    __tablename__ = "ops_assets_basic_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_type_id = Column(String(length=128), nullable=True)
    name = Column(String(length=128), nullable=True)
    description = Column(String(length=255), nullable=True)
    equipment_number = Column(String(length=128), nullable=True)
    sn_number = Column(String(length=128), nullable=True)
    asset_number = Column(String(length=128), nullable=True)
    asset_status = Column(String(length=40), nullable=True)
    extra = Column(Text)


# 资产设备的配件信息对象
class AssetPartsInfo(Base):
    __tablename__ = "ops_assets_parts_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_id = Column(String(length=128), nullable=True)
    part_type = Column(String(length=128), nullable=True)
    part_brand = Column(String(length=128), nullable=True)
    part_config = Column(String(length=128), nullable=True)
    part_number = Column(String(length=128), nullable=True)
    personal_used_flag = Column(Boolean, nullable=True, default=False)
    surplus = Column(String(length=128), nullable=True)
    name = Column(String(length=128), nullable=True)
    description = Column(String(length=255), nullable=True)
    extra = Column(Text)


# 资产设备的厂商信息对象
class AssetManufacturesInfo(Base):
    __tablename__ = "ops_assets_manufactures_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_id = Column(String(length=128), nullable=True)
    name = Column(String(length=128), nullable=True)
    description = Column(String(length=255), nullable=True)
    extra = Column(Text)


# 资产设备的位置信息对象
class AssetPositionsInfo(Base):
    __tablename__ = "ops_assets_positions_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_id = Column(String(length=128), nullable=True)
    frame_position = Column(String(length=128), nullable=True)
    cabinet_position = Column(String(length=128), nullable=True)
    u_position = Column(String(length=128), nullable=True)
    description = Column(String(length=255), nullable=True)


# 资产设备的合同信息对象
class AssetContractsInfo(Base):
    __tablename__ = "ops_assets_contracts_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_id = Column(String(length=128), nullable=True)
    contract_number = Column(String(length=128), nullable=True)
    purchase_date = Column(DateTime)
    batch_number = Column(String(length=10), nullable=True)
    description = Column(String(length=255), nullable=True)


# 资产设备的归属用户信息对象
class AssetBelongsInfo(Base):
    __tablename__ = "ops_assets_belongs_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_id = Column(String(length=128), nullable=True)
    department_id = Column(String(length=128), nullable=True)
    department_name = Column(String(length=128), nullable=True)
    user_id = Column(String(length=128), nullable=True)
    user_name = Column(String(length=128), nullable=True)
    tel_number = Column(String(length=128), nullable=True)
    description = Column(String(length=255), nullable=True)


# 资产设备的租户信息对象
class AssetCustomersInfo(Base):
    __tablename__ = "ops_assets_customers_info"

    id = Column(String(length=128), primary_key= True, nullable=False, index=True, unique=False)
    asset_id = Column(String(length=128), nullable=True)
    customer_id = Column(String(length=128), nullable=True)
    customer_name = Column(String(length=128), nullable=True)
    rental_duration = Column(Integer, default=0)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    vlan_id = Column(String(length=128), nullable=True)
    float_ip = Column(String(length=128), nullable=True)
    band_width = Column(String(length=128), nullable=True)
    description = Column(String(length=255), nullable=True)


# 资产对象
# class Asset(Base) = Table(
# "ops_assets",
# Column("uuid", String(length=128), nullable=False, index=True, unique=False),
# Column("asset_name", String(length=128), nullable=True),
# Column("asset_description", String(length=255), nullable=True),
# )
