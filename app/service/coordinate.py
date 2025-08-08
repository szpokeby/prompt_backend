#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinate Service业务逻辑
"""

import logging
import re
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.coordinate import Coordinate
from ..models.text_info import TextInfo
from ..models.phrase import Phrase
from ..models.table import Table
from ..schemas.coordinate import CoordinateUpdate
from ..tool import generate_id
from .exceptions import BusinessException


logger = logging.getLogger(__name__)


class CoordinateService:
    """Coordinate服务类"""
    
    def __init__(self, db: Session = None):
        """初始化Coordinate服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    async def batch_import(self, table_id: int) -> Dict[str, Any]:
        """
        批量导入坐标（从cor.txt导入）
        
        Args:
            table_id: 表格ID
            
        Returns:
            Dict: 包含coordinates和total的字典
            
        Raises:
            BusinessException: 表格不存在或导入失败
        """
        try:
            # 数据验证：验证table_id存在性
            table = self.db.query(Table).filter(Table.id == table_id).first()
            if not table:
                raise BusinessException(f"ID为 {table_id} 的表格不存在")
            
            # 文件处理：读取cor.txt文件
            cor_file_path = "data/cor.txt"  # 假设文件在data目录下
            if not os.path.exists(cor_file_path):
                raise BusinessException("cor.txt文件不存在")
            
            with open(cor_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # 数据解析：解析坐标数据
            coordinates_data = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                
                # 正则匹配"（x， y） color"格式
                match = re.match(r'[（(](\d+)[，,]\s*(\d+)[）)]\s*(\d+)', line)
                if not match:
                    logger.warning(f"第{line_num}行格式不正确: {line}")
                    continue
                
                x, y, color = match.groups()
                position = f"({x}, {y})"
                color_int = int(color)
                
                # 验证数据有效性
                if not (0 <= color_int <= 8):
                    logger.warning(f"第{line_num}行颜色值超出范围: {color_int}")
                    continue
                
                coordinates_data.append({
                    'id': generate_id(),
                    'table_id': table_id,
                    'position': position,
                    'color': color_int,
                    'voc': '',  # 默认空
                    'repeated': 0  # 默认0
                })
            
            if not coordinates_data:
                return {"coordinates": [], "total": 0}
            
            # 批量操作：分批插入
            batch_size = 1000
            total_inserted = 0
            
            for i in range(0, len(coordinates_data), batch_size):
                batch = coordinates_data[i:i + batch_size]
                
                # bulk_insert_mappings批量插入
                self.db.bulk_insert_mappings(Coordinate, batch)
                self.db.commit()
                
                batch_count = len(batch)
                total_inserted += batch_count
                logger.info(f"成功插入第{i//batch_size + 1}批坐标数据，数量: {batch_count}")
            
            # 结果查询：查询插入的坐标记录
            inserted_coordinates = self.db.query(Coordinate).filter(
                Coordinate.table_id == table_id
            ).all()
            
            # 数据转换：转换为Dict格式
            coordinate_dicts = []
            for coord in inserted_coordinates:
                coordinate_dicts.append({
                    'id': coord.id,
                    'table_id': coord.table_id,
                    'color': coord.color,
                    'position': coord.position,
                    'voc': coord.voc,
                    'repeated': coord.repeated
                })
            
            logger.info(f"批量导入完成，表格ID: {table_id}，总数量: {total_inserted}")
            
            return {
                "coordinates": coordinate_dicts,
                "total": len(coordinate_dicts)
            }
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"批量导入坐标错误: {str(e)}")
            raise BusinessException("批量导入坐标失败", str(e))
    
    async def delete_coordinates_by_table(self, table_id: int) -> Dict[str, str]:
        """
        删除表格所有坐标
        
        Args:
            table_id: 表格ID
            
        Returns:
            Dict: 包含message的字典
            
        Raises:
            BusinessException: 删除失败
        """
        try:
            # 数据操作：批量删除
            deleted_count = self.db.query(Coordinate).filter(
                Coordinate.table_id == table_id
            ).delete()
            
            # 事务提交
            self.db.commit()
            
            # 日志记录：记录删除数量和table_id
            logger.info(f"成功删除表格ID {table_id} 的 {deleted_count} 个坐标")
            
            return {"message": f"删除成功，共删除 {deleted_count} 个坐标"}
            
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"删除坐标数据库错误: {str(e)}")
            raise BusinessException("删除坐标数据失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"删除坐标业务错误: {str(e)}")
            raise BusinessException("删除坐标数据失败", str(e))
    
    async def find_coordinates_by_table(self, table_id: int) -> Dict[str, Any]:
        """
        获取表格坐标
        
        Args:
            table_id: 表格ID
            
        Returns:
            Dict: 包含coordinates和total的字典
            
        Raises:
            BusinessException: 查询失败
        """
        try:
            # 数据获取：条件查询
            coordinates = self.db.query(Coordinate).filter(
                Coordinate.table_id == table_id
            ).all()
            
            # 数据转换：转换为Dict格式
            coordinate_dicts = []
            for coord in coordinates:
                coordinate_dicts.append({
                    'id': coord.id,
                    'table_id': coord.table_id,
                    'color': coord.color,
                    'position': coord.position,
                    'voc': coord.voc,
                    'repeated': coord.repeated
                })
            
            logger.info(f"查询到表格ID {table_id} 的 {len(coordinate_dicts)} 个坐标")
            
            return {
                "coordinates": coordinate_dicts,
                "total": len(coordinate_dicts)
            }
            
        except SQLAlchemyError as e:
            logger.error(f"查询坐标数据库错误: {str(e)}")
            raise BusinessException("查询坐标数据失败", str(e))
        except Exception as e:
            logger.error(f"查询坐标业务错误: {str(e)}")
            raise BusinessException("查询坐标数据失败", str(e))
    
    async def list_coordinate_phrases(
        self, 
        color: Optional[int] = None, 
        table_id: Optional[int] = None, 
        coordinate_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        坐标关联词汇查询
        
        Args:
            color: 颜色筛选
            table_id: 表格ID
            coordinate_id: 坐标ID
            
        Returns:
            Dict: 包含phrases和total的字典
            
        Raises:
            BusinessException: 查询失败
        """
        try:
            if color is not None:
                # 通过color获取TextInfo
                text_info = self.db.query(TextInfo).filter(
                    TextInfo.color == color
                ).first()
                
                if not text_info:
                    # TextInfo不存在时返回空结果
                    logger.info(f"颜色 {color} 的TextInfo不存在，返回空结果")
                    return {"phrases": [], "total": 0}
                
                # 关联查询：获取该TextInfo的所有Phrase
                phrases = self.db.query(Phrase).filter(
                    Phrase.text_id == text_info.id
                ).all()
            else:
                # 查询所有词汇
                phrases = self.db.query(Phrase).all()
            
            # 数据转换：转换为Dict格式
            phrase_dicts = []
            for phrase in phrases:
                phrase_dicts.append({
                    'id': phrase.id,
                    'text_id': phrase.text_id,
                    'word': phrase.word,
                    'type': phrase.type
                })
            
            logger.info(f"坐标关联词汇查询成功，参数: color={color}, table_id={table_id}, coordinate_id={coordinate_id}，结果数量: {len(phrase_dicts)}")
            
            return {
                "phrases": phrase_dicts,
                "total": len(phrase_dicts)
            }
            
        except SQLAlchemyError as e:
            logger.error(f"查询词汇列表数据库错误: {str(e)}")
            raise BusinessException("查询词汇列表失败", str(e))
        except Exception as e:
            logger.error(f"查询词汇列表业务错误: {str(e)}")
            raise BusinessException("查询词汇列表失败", str(e))
    
    async def update_coordinate(self, coordinate_update: CoordinateUpdate) -> Dict[str, Any]:
        """
        更新坐标
        
        Args:
            coordinate_update: 坐标更新数据
            
        Returns:
            Dict: 包含coordinates的字典
            
        Raises:
            BusinessException: 坐标不存在或更新失败
        """
        try:
            # 数据获取：通过ID查询Coordinate记录
            existing_coordinate = self.db.query(Coordinate).filter(
                Coordinate.id == coordinate_update.id
            ).first()
            
            # 存在性验证：检查Coordinate是否存在
            if not existing_coordinate:
                raise BusinessException(f"ID为 {coordinate_update.id} 的坐标不存在")
            
            # 数据操作：更新字段
            existing_coordinate.table_id = coordinate_update.table_id
            existing_coordinate.color = coordinate_update.color
            existing_coordinate.position = coordinate_update.position
            existing_coordinate.voc = coordinate_update.voc
            existing_coordinate.repeated = coordinate_update.repeated
            
            # 事务提交
            self.db.commit()
            
            # 结果转换：转换为Dict格式
            updated_coordinate = {
                'id': existing_coordinate.id,
                'table_id': existing_coordinate.table_id,
                'color': existing_coordinate.color,
                'position': existing_coordinate.position,
                'voc': existing_coordinate.voc,
                'repeated': existing_coordinate.repeated
            }
            
            logger.info(f"成功更新坐标: ID={coordinate_update.id}")
            
            return {"coordinates": [updated_coordinate]}
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"更新坐标数据库错误: {str(e)}")
            raise BusinessException("更新坐标失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"更新坐标业务错误: {str(e)}")
            raise BusinessException("更新坐标失败", str(e))