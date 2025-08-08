#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextInfo Schema数据模型
"""

from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List


class TextInfoBase(BaseModel):
    """TextInfo基础模型"""
    color: int = Field(..., ge=0, le=8, description="颜色值，范围0-8")
    text: Optional[str] = Field(None, max_length=1000, description="文本内容，可选，最大1000字符")


class TextInfoResponse(TextInfoBase):
    """TextInfo响应模型"""
    id: int = Field(..., description="ID")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    @field_serializer('id')
    def serialize_id(self, value: int) -> str:
        """ID字段转字符串"""
        return str(value)


class TextInfoUpdate(BaseModel):
    """TextInfo更新模型"""
    id: int = Field(..., description="ID")
    color: int = Field(..., ge=0, le=8, description="颜色值，范围0-8")
    text: str = Field(..., max_length=1000, description="文本内容，最大1000字符")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TextInfoColorUpdate(BaseModel):
    """TextInfo颜色文本更新模型"""
    color: int = Field(..., ge=0, le=8, description="颜色值，范围0-8")
    text: str = Field(..., max_length=1000, description="文本内容，必需，最大1000字符")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)