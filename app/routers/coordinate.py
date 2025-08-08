#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinate路由模块
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, Optional
from ..schemas import CoordinateUpdate
from ..service import CoordinateService
from ..service.dependencies import get_coordinate_service

router = APIRouter(prefix="/coordinate", tags=["coordinates"])


@router.get("/batch", response_model=Dict[str, Any])
async def batch_import_coordinates(
    id: int = Query(..., description="表格ID"),
    coordinate_service: CoordinateService = Depends(get_coordinate_service)
):
    """
    批量导入坐标（从cor.txt导入）
    
    Args:
        id: 表格ID
        
    Returns:
        Dict: 包含coordinates和total的字典
    """
    try:
        return await coordinate_service.batch_import(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量导入坐标失败: {str(e)}"
        )


@router.delete("/delete", response_model=Dict[str, str])
async def delete_coordinates(
    id: int = Query(..., description="表格ID"),
    coordinate_service: CoordinateService = Depends(get_coordinate_service)
):
    """
    删除表格所有坐标
    
    Args:
        id: 表格ID
        
    Returns:
        Dict: 包含message的字典
    """
    try:
        return await coordinate_service.delete_coordinates_by_table(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除坐标失败: {str(e)}"
        )


@router.get("/find", response_model=Dict[str, Any])
async def find_coordinates(
    id: int = Query(..., description="表格ID"),
    coordinate_service: CoordinateService = Depends(get_coordinate_service)
):
    """
    获取表格坐标
    
    Args:
        id: 表格ID
        
    Returns:
        Dict: 包含coordinates和total的字典
    """
    try:
        return await coordinate_service.find_coordinates_by_table(id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询坐标失败: {str(e)}"
        )


@router.get("/list", response_model=Dict[str, Any])
async def list_coordinate_phrases(
    color: Optional[int] = Query(None, ge=0, le=8, description="颜色筛选"),
    table_id: Optional[int] = Query(None, description="表格ID"),
    coordinate_id: Optional[int] = Query(None, description="坐标ID"),
    coordinate_service: CoordinateService = Depends(get_coordinate_service)
):
    """
    坐标关联词汇查询
    
    Args:
        color: 颜色筛选
        table_id: 表格ID
        coordinate_id: 坐标ID
        
    Returns:
        Dict: 包含phrases和total的字典
    """
    try:
        return await coordinate_service.list_coordinate_phrases(color, table_id, coordinate_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询坐标关联词汇失败: {str(e)}"
        )


@router.put("/update", response_model=Dict[str, Any])
async def update_coordinate(
    coordinate_update: CoordinateUpdate,
    coordinate_service: CoordinateService = Depends(get_coordinate_service)
):
    """
    更新坐标
    
    Args:
        coordinate_update: 坐标更新数据
        
    Returns:
        Dict: 包含coordinates的字典
    """
    try:
        return await coordinate_service.update_coordinate(coordinate_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新坐标失败: {str(e)}"
        )