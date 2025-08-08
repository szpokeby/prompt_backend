#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service依赖注入模块
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from ..config.database import get_db
from .text_info import TextInfoService
from .phrase import PhraseService
from .table import TableService
from .coordinate import CoordinateService


def get_text_info_service(db: Session = Depends(get_db)) -> TextInfoService:
    """获取TextInfo服务实例"""
    return TextInfoService(db=db)


def get_phrase_service(db: Session = Depends(get_db)) -> PhraseService:
    """获取Phrase服务实例"""
    return PhraseService(db=db)


def get_table_service(db: Session = Depends(get_db)) -> TableService:
    """获取Table服务实例"""
    return TableService(db=db)


def get_coordinate_service(db: Session = Depends(get_db)) -> CoordinateService:
    """获取Coordinate服务实例"""
    return CoordinateService(db=db)