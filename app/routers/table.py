#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table路由模块
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any
from ..schemas import TableCreate, TableResponse, TableUpdate, TableListResponse
from ..service import TableService
from ..service.dependencies import get_table_service

router = APIRouter(prefix="/table", tags=["tables"])


@router.post("/add", response_model=TableResponse)
async def create_table(
    table_data: TableCreate,
    table_service: TableService = Depends(get_table_service)
):
    """
    创建表格
    
    Args:
        table_data: 表格创建数据
        
    Returns:
        TableResponse: 创建的表格信息
    """
    try:
        return await table_service.create_table(table_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建表格失败: {str(e)}"
        )


@router.get("/page", response_model=TableListResponse)
async def get_table_page(
    table_service: TableService = Depends(get_table_service)
):
    """
    查询表格列表
    
    Returns:
        TableListResponse: 表格列表响应
    """
    try:
        return await table_service.get_table_page()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询表格列表失败: {str(e)}"
        )


@router.put("/update", response_model=Dict[str, str])
async def update_table(
    table_update: TableUpdate,
    table_service: TableService = Depends(get_table_service)
):
    """
    更新表格
    
    Args:
        table_update: 表格更新数据
        
    Returns:
        Dict: 包含message的字典
    """
    try:
        return await table_service.update_table(table_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新表格失败: {str(e)}"
        )


@router.delete("/delete", response_model=Dict[str, str])
async def delete_table(
    id: int = Query(..., description="表格ID"),
    table_service: TableService = Depends(get_table_service)
):
    """
    删除表格（级联删除坐标数据）
    
    Args:
        id: 表格ID
        
    Returns:
        Dict: 包含message的字典
    """
    try:
        return await table_service.delete_table(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除表格失败: {str(e)}"
        )