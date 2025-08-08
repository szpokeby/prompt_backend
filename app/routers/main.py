#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主路由整合模块
"""

from fastapi import APIRouter
from . import text_info_router, phrase_router, table_router, coordinate_router

# 创建主路由器
api_router = APIRouter(prefix="/api")

# 注册各模块路由
api_router.include_router(text_info_router)
api_router.include_router(phrase_router)
api_router.include_router(table_router)
api_router.include_router(coordinate_router)