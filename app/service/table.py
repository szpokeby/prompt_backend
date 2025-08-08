#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Table Service业务逻辑
"""

import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.table import Table
from ..schemas.table import TableCreate, TableResponse, TableUpdate, TableListResponse
from ..tool import generate_id
from .exceptions import BusinessException


logger = logging.getLogger(__name__)


class TableService:
    """Table服务类"""
    
    def __init__(self, db: Session = None):
        """初始化Table服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    async def create_table(self, table_data: TableCreate) -> TableResponse:
        """
        创建表格
        
        Args:
            table_data: 表格创建数据
            
        Returns:
            TableResponse: 创建的表格响应
            
        Raises:
            BusinessException: 创建表格失败
        """
        try:
            # 数据创建：ID生成
            table_id = generate_id()
            
            # 对象创建：Table对象创建
            new_table = Table(
                id=table_id,
                name=table_data.name
                # create_time会自动设置为当前时间
            )
            
            # 数据操作：数据库插入
            self.db.add(new_table)
            self.db.commit()
            
            # 日志记录：记录表格创建时间
            logger.info(f"成功创建表格: ID={table_id}, name='{table_data.name}', create_time={new_table.create_time}")
            
            # 结果返回：返回创建的Table对象
            return TableResponse.model_validate(new_table)
            
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"创建表格数据库错误: {str(e)}")
            raise BusinessException("创建表格失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"创建表格业务错误: {str(e)}")
            raise BusinessException("创建表格失败", str(e))
    
    async def get_table_page(self) -> TableListResponse:
        """
        查询表格列表
        
        Returns:
            TableListResponse: 表格列表响应
            
        Raises:
            BusinessException: 查询表格失败
        """
        try:
            # 数据获取：查询所有Table记录，按创建时间降序排列
            tables = self.db.query(Table).order_by(Table.create_time.desc()).all()
            
            logger.info(f"查询到 {len(tables)} 个表格")
            
            # 结果返回：转换为响应对象
            table_responses = [TableResponse.model_validate(table) for table in tables]
            
            return TableListResponse(
                tables=table_responses,
                total=len(table_responses)
            )
            
        except SQLAlchemyError as e:
            logger.error(f"查询表格数据库错误: {str(e)}")
            raise BusinessException("查询表格失败", str(e))
        except Exception as e:
            logger.error(f"查询表格业务错误: {str(e)}")
            raise BusinessException("查询表格失败", str(e))
    
    async def update_table(self, table_update: TableUpdate) -> Dict[str, str]:
        """
        更新表格
        
        Args:
            table_update: 表格更新数据
            
        Returns:
            Dict: 包含message的字典
            
        Raises:
            BusinessException: 表格不存在或更新失败
        """
        try:
            # 数据获取：通过ID查询Table记录
            existing_table = self.db.query(Table).filter(
                Table.id == table_update.id
            ).first()
            
            # 存在性验证：检查Table是否存在
            if not existing_table:
                raise BusinessException(f"ID为 {table_update.id} 的表格不存在")
            
            # 数据操作：更新字段
            existing_table.name = table_update.name
            
            # 事务提交
            self.db.commit()
            
            logger.info(f"成功更新表格: ID={table_update.id}, new_name='{table_update.name}'")
            
            return {"message": "更新成功"}
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"更新表格数据库错误: {str(e)}")
            raise BusinessException("更新表格失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"更新表格业务错误: {str(e)}")
            raise BusinessException("更新表格失败", str(e))
    
    async def delete_table(self, table_id: int) -> Dict[str, str]:
        """
        删除表格（级联删除坐标数据）
        
        Args:
            table_id: 表格ID
            
        Returns:
            Dict: 包含message的字典
            
        Raises:
            BusinessException: 表格不存在或删除失败
        """
        try:
            # 数据获取：通过ID查询Table记录
            existing_table = self.db.query(Table).filter(
                Table.id == table_id
            ).first()
            
            # 存在性验证：检查Table是否存在
            if not existing_table:
                raise BusinessException(f"ID为 {table_id} 的表格不存在")
            
            # 数据操作：删除操作（级联删除会自动删除关联的Coordinate记录）
            self.db.delete(existing_table)
            self.db.commit()
            
            logger.info(f"成功删除表格: ID={table_id}, name='{existing_table.name}'")
            
            return {"message": "删除成功"}
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"删除表格数据库错误: {str(e)}")
            raise BusinessException("删除表格失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"删除表格业务错误: {str(e)}")
            raise BusinessException("删除表格失败", str(e))