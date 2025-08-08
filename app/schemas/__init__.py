# -*- coding: utf-8 -*-
"""
数据模式模块
"""

from .text_info import TextInfoBase, TextInfoResponse, TextInfoUpdate, TextInfoColorUpdate
from .phrase import PhraseBase, PhraseResponse, PhraseListResponse
from .table import TableBase, TableCreate, TableResponse, TableUpdate, TableListResponse
from .coordinate import CoordinateUpdate, CoordinateResponse, CoordinateListResponse

__all__ = [
    # TextInfo schemas
    "TextInfoBase",
    "TextInfoResponse", 
    "TextInfoUpdate",
    "TextInfoColorUpdate",
    
    # Phrase schemas
    "PhraseBase",
    "PhraseResponse",
    "PhraseListResponse",
    
    # Table schemas
    "TableBase",
    "TableCreate",
    "TableResponse",
    "TableUpdate", 
    "TableListResponse",
    
    # Coordinate schemas
    "CoordinateUpdate",
    "CoordinateResponse",
    "CoordinateListResponse",
] 