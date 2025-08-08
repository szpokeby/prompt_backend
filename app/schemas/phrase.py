#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phrase Schema数据模型
"""

from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List


class PhraseBase(BaseModel):
    """Phrase基础模型"""
    word: str = Field(..., min_length=1, max_length=255, description="词汇，长度1-255")
    phrase_type: int = Field(..., ge=0, alias="type", description="词汇类型，非负整数")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PhraseResponse(PhraseBase):
    """Phrase响应模型"""
    id: int = Field(..., description="ID")
    text_id: int = Field(..., description="文本ID")
    
    @field_serializer('id', 'text_id')
    def serialize_ids(self, value: int) -> str:
        """多ID字段转字符串"""
        return str(value)


class PhraseListResponse(BaseModel):
    """Phrase列表响应模型"""
    phrases: List[PhraseResponse] = Field(..., description="词汇列表")
    total: int = Field(..., description="总数")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)