#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table模型定义
"""

from sqlalchemy import Column, BigInteger, String, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base


class Table(Base):
    """Table模型"""
    
    __tablename__ = "table_info"
    
    # 主键索引
    id = Column(BigInteger, primary_key=True, index=True)
    
    # 字段定义
    name = Column(String(255), nullable=False)
    create_time = Column(DateTime, nullable=False, default=func.now())
    
    # 关系：一对多关联Coordinate模型，级联删除
    coordinates = relationship("Coordinate", back_populates="table", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """字符串表示方法"""
        return f"<Table(id={self.id}, name='{self.name}', create_time='{self.create_time}')>" 