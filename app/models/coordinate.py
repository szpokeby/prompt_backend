#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinate模型定义
"""

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship
from ..config.database import Base


class Coordinate(Base):
    """Coordinate模型"""
    
    __tablename__ = "coordinate"
    
    # 主键索引
    id = Column(BigInteger, primary_key=True, index=True)
    
    # 外键关系
    table_id = Column(BigInteger, ForeignKey("table_info.id"), nullable=False, index=True)
    
    # 字段定义
    color = Column(Integer, nullable=False)
    position = Column(String(255), nullable=False)
    voc = Column(String(255), nullable=True)
    repeated = Column(Integer, nullable=False, default=0)
    
    # 约束：color字段范围检查
    __table_args__ = (
        CheckConstraint('color >= 0 AND color <= 8', name='check_coordinate_color_range'),
    )
    
    # 关系：多对一关联Table模型
    table = relationship("Table", back_populates="coordinates")
    
    def __repr__(self) -> str:
        """字符串表示方法"""
        return f"<Coordinate(id={self.id}, table_id={self.table_id}, color={self.color}, position='{self.position}', voc='{self.voc}', repeated={self.repeated})>" 