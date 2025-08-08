#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinate Schema数据模型
"""

from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List


class CoordinateUpdate(BaseModel):
    """Coordinate更新模型"""
    id: int = Field(..., description="ID")
    table_id: int = Field(..., description="表格ID")
    color: int = Field(..., ge=0, le=8, description="颜色值，范围0-8")
    position: str = Field(..., description="位置")
    voc: Optional[str] = Field("", description="词汇，可选，默认空")
    repeated: int = Field(0, ge=0, description="重复次数，默认0")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CoordinateResponse(BaseModel):
    """Coordinate响应模型"""
    id: int = Field(..., description="ID")
    table_id: int = Field(..., description="表格ID")
    color: int = Field(..., description="颜色值")
    position: str = Field(..., description="位置")
    voc: Optional[str] = Field(None, description="词汇")
    repeated: int = Field(..., description="重复次数")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    @field_serializer('id', 'table_id')
    def serialize_ids(self, value: int) -> str:
        """ID字段转字符串"""
        return str(value)


class CoordinateListResponse(BaseModel):
    """Coordinate列表响应模型"""
    coordinates: List[CoordinateResponse] = Field(..., description="坐标列表")
    total: int = Field(..., description="总数")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)