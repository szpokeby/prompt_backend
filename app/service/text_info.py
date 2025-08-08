#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextInfo Service业务逻辑
"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.text_info import TextInfo
from ..schemas.text_info import TextInfoResponse, TextInfoUpdate
from ..config.database import get_db
from .exceptions import BusinessException


logger = logging.getLogger(__name__)


class TextInfoService:
    """TextInfo服务类"""
    
    def __init__(self, db: Session = None):
        """初始化TextInfo服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    async def find_all(self) -> List[TextInfoResponse]:
        """
        查询所有TextInfo信息
        
        Returns:
            List[TextInfoResponse]: TextInfo响应列表
            
        Raises:
            BusinessException: 查询文本信息失败
        """
        try:
            # 数据获取：查询所有TextInfo记录，按color字段升序排列
            text_infos = self.db.query(TextInfo).order_by(TextInfo.color).all()
            
            # 日志记录：记录查询到的记录数量
            logger.info(f"查询到 {len(text_infos)} 条TextInfo记录")
            
            # 结果返回：转换为响应模型列表
            return [TextInfoResponse.model_validate(text_info) for text_info in text_infos]
            
        except SQLAlchemyError as e:
            logger.error(f"查询TextInfo数据库错误: {str(e)}")
            raise BusinessException("查询文本信息失败", str(e))
        except Exception as e:
            logger.error(f"查询TextInfo业务错误: {str(e)}")
            raise BusinessException("查询文本信息失败", str(e))
    
    async def update(self, text_info_update: TextInfoUpdate) -> TextInfoResponse:
        """
        更新TextInfo信息
        
        Args:
            text_info_update: TextInfo更新数据
            
        Returns:
            TextInfoResponse: 更新后的TextInfo响应
            
        Raises:
            BusinessException: 文本信息不存在或更新失败
        """
        try:
            # 数据获取：通过ID查询TextInfo记录
            existing_text_info = self.db.query(TextInfo).filter(
                TextInfo.id == text_info_update.id
            ).first()
            
            # 存在性验证：检查TextInfo是否存在
            if not existing_text_info:
                raise BusinessException(f"ID为 {text_info_update.id} 的文本信息不存在")
            
            # 数据操作：更新字段
            existing_text_info.color = text_info_update.color
            existing_text_info.text = text_info_update.text
            
            # 数据库保存：merge更新 + commit提交
            updated_text_info = self.db.merge(existing_text_info)
            self.db.commit()
            
            logger.info(f"成功更新TextInfo ID: {text_info_update.id}")
            
            # 结果返回：返回更新后的TextInfo对象
            return TextInfoResponse.model_validate(updated_text_info)
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"更新TextInfo数据库错误: {str(e)}")
            raise BusinessException("更新文本信息失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"更新TextInfo业务错误: {str(e)}")
            raise BusinessException("更新文本信息失败", str(e))