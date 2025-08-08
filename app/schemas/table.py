#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table Schema数据模型
"""

from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List
from datetime import datetime


class TableBase(BaseModel):
    """Table基础模型"""
    name: str = Field(..., min_length=1, max_length=255, description="表格名称，长度1-255")


class TableCreate(TableBase):
    """Table创建模型"""
    pass


class TableResponse(TableBase):
    """Table响应模型"""
    id: int = Field(..., description="ID")
    create_time: datetime = Field(..., description="创建时间")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    @field_serializer('id')
    def serialize_id(self, value: int) -> str:
        """ID字段转字符串"""
        return str(value)


class TableUpdate(BaseModel):
    """Table更新模型"""
    id: int = Field(..., description="ID")
    name: str = Field(..., min_length=1, max_length=255, description="表格名称，长度1-255")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TableListResponse(BaseModel):
    """Table列表响应模型"""
    tables: List[TableResponse] = Field(..., description="表格列表")
    total: int = Field(..., description="总数")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)