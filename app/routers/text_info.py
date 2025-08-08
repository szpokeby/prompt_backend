#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextInfo路由模块
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas import TextInfoResponse, TextInfoUpdate
from ..service import TextInfoService
from ..service.dependencies import get_text_info_service

router = APIRouter(prefix="/text", tags=["text_info"])


@router.get("/find", response_model=List[TextInfoResponse])
async def find_text_info(
    text_info_service: TextInfoService = Depends(get_text_info_service)
):
    """
    查询所有TextInfo信息
    
    Returns:
        List[TextInfoResponse]: TextInfo列表
    """
    try:
        return await text_info_service.find_all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询TextInfo信息失败: {str(e)}"
        )


@router.put("/update", response_model=TextInfoResponse)
async def update_text_info(
    text_info_update: TextInfoUpdate,
    text_info_service: TextInfoService = Depends(get_text_info_service)
):
    """
    更新TextInfo信息
    
    Args:
        text_info_update: TextInfo更新数据
        
    Returns:
        TextInfoResponse: 更新后的TextInfo信息
    """
    try:
        return await text_info_service.update(text_info_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新TextInfo信息失败: {str(e)}"
        )