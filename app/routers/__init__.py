#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路由模块
"""

from .text_info import router as text_info_router
from .phrase import router as phrase_router
from .table import router as table_router
from .coordinate import router as coordinate_router

__all__ = [
    "text_info_router",
    "phrase_router", 
    "table_router",
    "coordinate_router",
]