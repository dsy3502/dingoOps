# 资产的api接口
import os
import time
from io import BytesIO
from typing import List

import pandas
from fastapi import APIRouter, UploadFile, File, Query, Path, HTTPException
from fastapi.responses import FileResponse
from mako.testing.helpers import result_lines

from api.model.assets import AssetCreateApiModel, AssetManufacturerApiModel, AssetUpdateStatusApiModel, \
    AssetPartApiModel
from api.response import ResponseModel, success_response
from services.assets import AssetsService
from utils.constant import EXCEL_TEMP_DIR, ASSET_TEMPLATE_ASSET_SHEET, ASSET_TEMPLATE_PART_SHEET
from utils.datetime import format_unix_timestamp, format_d8q_timestamp

router = APIRouter()
assert_service = AssetsService()


@router.get("/assets/download", summary="下载资产信息", description="根据条件下载对应的资产文件")
async def download_assets_xlsx():
    # 把数据库中的资产数据导出资产信息数据
    result_file_name = "asset_" + format_d8q_timestamp() + ".xlsx"
    print(result_file_name)
    # 导出文件路径
    result_file_path = EXCEL_TEMP_DIR + result_file_name
    # 生成文件
    # 读取excel文件内容
    try:
        # 存入一行
        assert_service.create_asset_excel(result_file_path)
    except Exception as e:
        import traceback
        traceback.print_exc()
    # 文件存在则下载
    if os.path.exists(result_file_path):
        return FileResponse(
            path=result_file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=result_file_name  # 下载时显示的文件名
        )
    return {"error": "File not found"}


# @router.get("/assets", response_model=ResponseModel[dict])
@router.get("/assets", summary="查询资产列表", description="根据各种条件分页查询资产列表数据")
async def list_assets(
        asset_id:str = Query(None, description="资产id"),
        asset_name:str = Query(None, description="资产名称"),
        asset_status:str = Query(None, description="资产状态"),
        frame_position:str = Query(None, description="机架"),
        cabinet_position:str = Query(None, description="机柜"),
        u_position:str = Query(None, description="u位"),
        equipment_number:str = Query(None, description="设备型号"),
        asset_number:str = Query(None, description="资产编号"),
        sn_number:str = Query(None, description="序列号"),
        department_name:str = Query(None, description="部门"),
        user_name:str = Query(None, description="负责人"),
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="页数量大小"),
        sort_keys:str = Query(None, description="排序字段"),
        sort_dirs:str = Query(None, description="排序方式"),):
    # 接收查询参数
    # 返回数据接口
    try:
        # 查询成功
        result = assert_service.list_assets(asset_id, asset_name, asset_status, frame_position, cabinet_position, u_position, equipment_number, asset_number, sn_number, department_name, user_name, page, page_size, sort_keys, sort_dirs)
        return result
        # return success_response(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset not found")

@router.get("/assets/{asset_id}", summary="查询资产详情", description="根据id查询资产详情数据")
async def get_asset_by_id(asset_id:str,):
    # 返回数据接口
    try:
        # 查询成功
        result = assert_service.get_asset_by_id(asset_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset not found")

@router.delete("/assets/{asset_id}", summary="删除资产", description="根据资产id删除资产信息")
async def delete_asset_by_id(asset_id:str):
    # 创建资产设备
    try:
        # 创建成功
        result = assert_service.delete_asset(asset_id)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="asset delete error")


@router.put("/assets/{asset_id}", summary="更新资产信息", description="根据资产id更新资产信息")
async def update_asset_by_id(asset_id:str, asset:AssetCreateApiModel):
    # 创建资产设备
    try:
        # 创建成功
        result = assert_service.update_asset(asset_id, asset)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


@router.post("/assets", summary="创建资产", description="创建资产信息")
async def create_asset(asset:AssetCreateApiModel):
    # 创建资产设备
    try:
        # 创建成功
        result = assert_service.create_asset(asset)
        return result
        # return success_response(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="asset create error")


@router.post("/assets/update_status", summary="批量更新状态", description="批量更新状态")
async def update_assets_status(asset:List[AssetUpdateStatusApiModel]):
    # 更新资产设备的状态
    try:
        # 更新成功
        result = assert_service.update_assets_status(asset)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset update status error")


@router.get("/assets/templates/{template_id}", summary="下载模板", description="根据模板的id下载对应的模板文件")
async def download_asset_template_xlsx(template_id:str):
    # 当前目录
    print(os.getcwd())
    # 模板文件目录绝对路径
    file_dir_path = os.getcwd() + "/api/template/"
    # 模板文件路径
    file_path = file_dir_path + template_id + ".xlsx"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=template_id + ".xlsx"  # 下载时显示的文件名
        )
    return {"error": "File not found"}


@router.post("/assets/upload", summary="上传资产文件", description="上传资产文件创建对应数据")
async def upload_asset_xlsx(file: UploadFile = File(...)):
    # 按照资产模板导入数据
    # 文件是否是excel
    if not file.filename.endswith('.xlsx'):
        return "文件格式错误"
    # 文件大小
    if file.size > 1024 * 1024 * 5:
        return "文件大小不能超过5MB！"
    # 读取excel文件内容
    try:
        # 读取资产的数据
        contents = await file.read()
        buffer = BytesIO(contents)
        # 1、资产设备sheet
        df = pandas.read_excel(buffer, sheet_name=ASSET_TEMPLATE_ASSET_SHEET)
        # 遍历
        for _, row in df.iterrows():
            # 存入一行
            assert_service.import_asset(row)
        # 2、资产设备sheet
        df = pandas.read_excel(buffer, sheet_name=ASSET_TEMPLATE_PART_SHEET)
        # 遍历
        for _, row in df.iterrows():
            # 存入一行
            assert_service.import_asset_part(row)
    except Exception as e:
        import traceback
        traceback.print_exc()




# 以下是厂商的相关接口信息
@router.post("/manufactures", summary="创建厂商", description="创建厂商数据信息")
async def create_manufacture(manufacture:AssetManufacturerApiModel):
    # 创建资产设备
    try:
        # 创建成功
        result = assert_service.create_manufacture(manufacture)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None

@router.get("/manufactures", summary="查询厂商", description="根据条件查询厂商分页列表信息")
async def list_manufactures(
        manufacture_name:str = None,
        page: int = 1,
        page_size: int = 10,
        sort_keys:str = None,
        sort_dirs:str = None,):
    # 返回数据接口
    try:
        # 查询成功
        result = assert_service.list_manufactures(manufacture_name, page, page_size, sort_keys, sort_dirs)
        return result
    except Exception as e:
        return None

@router.delete("/manufactures/{manufacture_id}", summary="删除厂商", description="根据厂商id删除厂商数据信息")
async def delete_manufacture_by_id(manufacture_id:str):
    # 删除厂商
    try:
        # 删除成功
        result = assert_service.delete_manufacture(manufacture_id)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


@router.put("/manufactures/{manufacture_id}", summary="修改厂商", description="修改厂商的数据信息")
async def update_manufacture_by_id(manufacture_id:str, manufacture:AssetManufacturerApiModel):
    # 修改指定id的厂商信息
    try:
        # 修改成功
        result = assert_service.update_manufacture(manufacture_id, manufacture)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


# 以下是资产的类型相关的接口 start
@router.get("/asset_types", summary="查询资产类型列表", description="根据各种条件查询资产列表数据")
async def list_assets_types(
        asset_type_name:str = Query(None, description="资产类型名称")):
    # 接收查询参数
    # 返回数据接口
    try:
        # 查询成功
        result = assert_service.list_assets_types(asset_type_name)
        return result
    except Exception as e:
        return None

# 以下是资产的类型相关的接口 end

# 以下时资产配件的相关接口 start
@router.get("/parts", summary="查询资产配件列表", description="根据各种条件分页查询资产配件列表数据")
async def list_assets_parts(
        part_catalog: str = Query(None, description="配件分类：库存配件(inventory)、已用配件(used)"),
        asset_id: str = Query(None, description="资产id"),
        name: str = Query(None, description="配件名称"),
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="页数量大小"),
        sort_keys: str = Query(None, description="排序字段"),
        sort_dirs: str = Query(None, description="排序方式"),):
    # 返回数据接口
    try:
        # 查询成功
        result = assert_service.list_assets_parts_pages(part_catalog, asset_id, name, page, page_size, sort_keys, sort_dirs)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset part not found")


@router.post("/parts", summary="创建配件", description="根据输入信息创建配件数据")
async def create_assets_parts(asset_part:AssetPartApiModel):
    # 创建配件
    try:
        # 调用创建接口
        result = assert_service.create_asset_part(asset_part)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset part not found")


@router.put("/parts/{id}", summary="修改配件", description="根据id信息修改配件数据")
async def update_asset_part_by_id(id:str, asset_part:AssetPartApiModel):
    # 修改配件
    try:
        # 调用修改接口
        result = assert_service.update_asset_part_by_id(id, asset_part)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset part update error")


@router.delete("/parts/{id}", summary="删除配件", description="根据输入配件的id删除配件数据")
async def delete_asset_part_by_id(id:str):
    # 删除配件
    try:
        # 调用删除接口
        result = assert_service.delete_asset_part_by_id(id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset part delete error")

@router.put("/parts/{id}/bind/{asset_id}", summary="配件绑定资产", description="根据id信息修改配件绑定关系")
async def bind_asset_part_by_id(id:str, asset_id:str):
    # 修改配件
    try:
        # 调用修改接口
        result = assert_service.bind_asset_part_by_id(id, asset_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset part update error")

@router.put("/parts/{id}/unbind/{asset_id}", summary="配件解绑绑定资产", description="根据id信息修改配件绑定关系")
async def unbind_asset_part_by_id(id:str, asset_id:str):
    # 修改配件
    try:
        # 调用修改接口
        result = assert_service.unbind_asset_part_by_id(id, asset_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="asset part update error")