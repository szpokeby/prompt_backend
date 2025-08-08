#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextInfo模型定义
"""

from sqlalchemy import Column, BigInteger, Integer, String, Index, CheckConstraint
from sqlalchemy.orm import relationship
from ..config.database import Base


class TextInfo(Base):
    """TextInfo模型"""
    
    __tablename__ = "text_info"
    
    # 主键索引
    id = Column(BigInteger, primary_key=True, index=True)
    
    # 字段定义
    color = Column(Integer, nullable=False, unique=True)
    text = Column(String, nullable=True, default="")
    
    # 约束：color字段范围检查
    __table_args__ = (
        CheckConstraint('color >= 0 AND color <= 8', name='check_color_range'),
    )
    
    # 关系：一对多关联Phrase模型，级联删除
    phrases = relationship("Phrase", back_populates="text_info", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        """字符串表示方法"""
        return f"<TextInfo(id={self.id}, color={self.color}, text='{self.text}')>" 