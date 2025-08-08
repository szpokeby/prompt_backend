#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用设置配置
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用设置类"""
    
    # 数据库连接配置
    database_url: str = "sqlite:///./cube.db"
    
    # 环境变量管理
    debug: bool = True
    
    # 环境变量文件配置
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局配置实例
settings = Settings() 