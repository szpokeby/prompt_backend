#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接配置
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from .settings import settings

# SQLAlchemy引擎配置
DATABASE_URL = settings.database_url

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 会话管理
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 基础模型类
Base = declarative_base()


def get_db() -> Generator:
    """依赖注入生成器"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 