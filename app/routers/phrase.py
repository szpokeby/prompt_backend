#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phrase路由模块
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, Optional
from ..schemas import TextInfoColorUpdate, PhraseListResponse
from ..service import PhraseService
from ..service.dependencies import get_phrase_service

router = APIRouter(prefix="/phrase", tags=["phrases"])


@router.post("/add", response_model=Dict[str, Any])
async def add_phrase(
    text_info_data: TextInfoColorUpdate,
    phrase_service: PhraseService = Depends(get_phrase_service)
):
    """
    添加词汇（智能词汇处理+自动编号）
    
    Args:
        text_info_data: 文本信息和颜色数据
        
    Returns:
        Dict: 包含message和text_info的字典
    """
    try:
        return await phrase_service.add_phrase(text_info_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加词汇失败: {str(e)}"
        )


@router.delete("/delete", response_model=Dict[str, Any])
async def delete_phrase(
    text_info_data: TextInfoColorUpdate,
    phrase_service: PhraseService = Depends(get_phrase_service)
):
    """
    删除词汇（差异化删除逻辑）
    
    Args:
        text_info_data: 文本信息和颜色数据
        
    Returns:
        Dict: 包含message或message+updated_text_infos的字典
    """
    try:
        return await phrase_service.delete_phrase(text_info_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除词汇失败: {str(e)}"
        )


@router.get("/list", response_model=PhraseListResponse)
async def list_phrases(
    color: Optional[int] = Query(None, ge=0, le=8, description="颜色筛选，范围0-8"),
    phrase_service: PhraseService = Depends(get_phrase_service)
):
    """
    查询词汇列表
    
    Args:
        color: 颜色筛选参数
        
    Returns:
        PhraseListResponse: 词汇列表响应
    """
    try:
        return await phrase_service.list_phrases(color)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询词汇列表失败: {str(e)}"
        )