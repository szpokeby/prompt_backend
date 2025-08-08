#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phrase模型定义
"""

from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..config.database import Base


class Phrase(Base):
    """Phrase模型"""
    
    __tablename__ = "phrase"
    
    # 主键索引
    id = Column(BigInteger, primary_key=True, index=True)
    
    # 外键关系
    text_id = Column(BigInteger, ForeignKey("text_info.id"), nullable=False, index=True)
    
    # 字段定义
    word = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False, default=0)
    
    # 关系：多对一关联TextInfo模型
    text_info = relationship("TextInfo", back_populates="phrases")
    
    def __repr__(self) -> str:
        """字符串表示方法"""
        return f"<Phrase(id={self.id}, text_id={self.text_id}, word='{self.word}', type={self.type})>" 