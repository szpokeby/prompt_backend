#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phrase Service业务逻辑
"""

import logging
import re
from typing import List, Dict, Any, Optional
from collections import Counter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.text_info import TextInfo
from ..models.phrase import Phrase
from ..schemas.phrase import PhraseResponse
from ..schemas.text_info import TextInfoColorUpdate
from ..tool import TextProcessor, generate_id
from .exceptions import BusinessException


logger = logging.getLogger(__name__)


class PhraseService:
    """Phrase服务类"""
    
    def __init__(self, db: Session = None):
        """初始化Phrase服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    async def add_phrase(self, text_info_data: TextInfoColorUpdate) -> Dict[str, Any]:
        """
        添加词汇（智能词汇处理+自动编号）
        
        Args:
            text_info_data: 包含color和text的数据
            
        Returns:
            Dict: 包含message和text_info的字典
            
        Raises:
            BusinessException: 文本信息不存在或添加失败
        """
        try:
            # 数据获取：通过color获取TextInfo记录
            text_info = self.db.query(TextInfo).filter(
                TextInfo.color == text_info_data.color
            ).first()
            
            # 数据验证：TextInfo存在性检查
            if not text_info:
                raise BusinessException(f"颜色 {text_info_data.color} 的文本信息不存在")
            
            old_text = text_info.text or ""
            new_text = text_info_data.text or ""
            text_info_id = text_info.id
            
            # 算法处理：工具类调用
            old_blocks = TextProcessor.split_text_by_comma(old_text)
            new_blocks = TextProcessor.split_text_by_comma(new_text)
            diff_blocks = TextProcessor.find_different_blocks(old_blocks, new_blocks)
            
            # 逻辑判断：差异列表为空时返回无新增
            if not diff_blocks:
                return {
                    "message": "没有新增词汇",
                    "text_info": {
                        "id": text_info.id,
                        "color": text_info.color,
                        "text": text_info.text
                    }
                }
            
            # 数据操作：查询所有现有词汇进行计数
            all_phrases = self.db.query(Phrase).all()
            phrase_count = Counter(phrase.word for phrase in all_phrases)
            
            # 批量处理：创建新词汇
            new_phrases = []
            for block in diff_blocks:
                cleaned_block = TextProcessor.clean_text(block)
                if not cleaned_block:
                    continue
                
                # 自动编号算法：如果词汇已存在，添加数字后缀
                word = cleaned_block
                count = phrase_count.get(word, 0)
                if count > 0:
                    word = f"{cleaned_block}{count + 1}"
                
                # 创建新词汇
                phrase_id = generate_id()
                new_phrase = Phrase(
                    id=phrase_id,
                    text_id=text_info_id,
                    word=word,
                    type=0  # 默认类型
                )
                new_phrases.append(new_phrase)
                phrase_count[cleaned_block] += 1
            
            # 数据库操作：批量插入新词汇
            if new_phrases:
                self.db.add_all(new_phrases)
            
            # 关联更新：更新TextInfo.text字段
            text_info.text = new_text
            self.db.commit()
            
            logger.info(f"成功添加 {len(new_phrases)} 个词汇到TextInfo ID: {text_info_id}")
            
            # 结果返回：数据组装
            return {
                "message": "添加成功",
                "text_info": {
                    "id": text_info.id,
                    "color": text_info.color,
                    "text": text_info.text
                }
            }
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"添加词汇数据库错误: {str(e)}")
            raise BusinessException("添加词汇失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"添加词汇业务错误: {str(e)}")
            raise BusinessException("添加词汇失败", str(e))
    
    async def delete_phrase(self, text_info_data: TextInfoColorUpdate) -> Dict[str, Any]:
        """
        删除词汇（差异化删除逻辑）
        
        Args:
            text_info_data: 包含color和text的数据
            
        Returns:
            Dict: 包含message或message+updated_text_infos的字典
            
        Raises:
            BusinessException: 文本信息不存在或删除失败
        """
        try:
            # 数据获取：通过color获取TextInfo记录
            text_info = self.db.query(TextInfo).filter(
                TextInfo.color == text_info_data.color
            ).first()
            
            # 数据验证：TextInfo存在性检查
            if not text_info:
                raise BusinessException(f"颜色 {text_info_data.color} 的文本信息不存在")
            
            old_text = text_info.text or ""
            new_text = text_info_data.text or ""
            text_info_id = text_info.id
            
            # 算法处理：差异分析
            old_blocks = TextProcessor.split_text_by_comma(old_text)
            new_blocks = TextProcessor.split_text_by_comma(new_text)
            deleted_blocks = TextProcessor.find_deleted_blocks(old_blocks, new_blocks)
            
            if not deleted_blocks:
                # 更新文本但没有删除词汇
                text_info.text = new_text
                self.db.commit()
                return {"message": "文本已更新，但没有删除词汇"}
            
            updated_text_infos = []
            
            # 遍历每个被删除的词汇块
            for deleted_block in deleted_blocks:
                cleaned_block = TextProcessor.clean_text(deleted_block)
                if not cleaned_block:
                    continue
                
                # 删除策略判断：检查数字后缀
                has_suffix = bool(re.search(r'\d+$', cleaned_block))
                
                if not has_suffix:
                    # 简单删除：直接删除Phrase
                    deleted_phrases = self.db.query(Phrase).filter(
                        Phrase.text_id == text_info_id,
                        Phrase.word == cleaned_block
                    ).all()
                    
                    for phrase in deleted_phrases:
                        self.db.delete(phrase)
                else:
                    # 复杂删除：需要重新编号
                    # 提取基础词汇（去除数字后缀）
                    base_word = re.sub(r'\d+$', '', cleaned_block)
                    suffix_match = re.search(r'(\d+)$', cleaned_block)
                    deleted_number = int(suffix_match.group(1)) if suffix_match else 0
                    
                    # 删除目标词汇
                    deleted_phrases = self.db.query(Phrase).filter(
                        Phrase.text_id == text_info_id,
                        Phrase.word == cleaned_block
                    ).all()
                    
                    for phrase in deleted_phrases:
                        self.db.delete(phrase)
                    
                    # 查询需要重新编号的相关词汇
                    related_phrases = self.db.query(Phrase).filter(
                        Phrase.word.like(f"{base_word}%")
                    ).all()
                    
                    # 重编号算法：更新type和相关文本
                    for phrase in related_phrases:
                        # 检查是否有更大的数字后缀
                        suffix_match = re.search(r'(\d+)$', phrase.word)
                        if suffix_match:
                            current_number = int(suffix_match.group(1))
                            if current_number > deleted_number:
                                # 递减编号
                                new_number = current_number - 1
                                old_word = phrase.word
                                new_word = f"{base_word}{new_number}" if new_number > 1 else base_word
                                phrase.word = new_word
                                
                                # 更新对应的TextInfo文本
                                phrase_text_info = self.db.query(TextInfo).filter(
                                    TextInfo.id == phrase.text_id
                                ).first()
                                
                                if phrase_text_info and phrase_text_info.text:
                                    phrase_text_info.text = phrase_text_info.text.replace(old_word, new_word)
                                    updated_text_infos.append({
                                        "id": phrase_text_info.id,
                                        "color": phrase_text_info.color,
                                        "text": phrase_text_info.text
                                    })
            
            # 更新当前TextInfo.text
            text_info.text = new_text
            self.db.commit()
            
            logger.info(f"成功删除词汇，TextInfo ID: {text_info_id}")
            
            # 差异化返回
            if updated_text_infos:
                return {
                    "message": "删除成功",
                    "updated_text_infos": updated_text_infos
                }
            else:
                return {"message": "删除成功"}
            
        except BusinessException:
            # 业务异常直接抛出
            self.db.rollback()
            raise
        except SQLAlchemyError as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"删除词汇数据库错误: {str(e)}")
            raise BusinessException("删除词汇失败", str(e))
        except Exception as e:
            # 数据库回滚
            self.db.rollback()
            logger.error(f"删除词汇业务错误: {str(e)}")
            raise BusinessException("删除词汇失败", str(e))
    
    async def list_phrases(self, color: Optional[int] = None) -> Dict[str, Any]:
        """
        查询词汇列表
        
        Args:
            color: 颜色筛选参数（可选）
            
        Returns:
            Dict: 包含phrases和total的字典
            
        Raises:
            BusinessException: 查询失败
        """
        try:
            if color is not None:
                # 按颜色筛选
                text_info = self.db.query(TextInfo).filter(
                    TextInfo.color == color
                ).first()
                
                if not text_info:
                    # TextInfo不存在时返回空列表
                    return {"phrases": [], "total": 0}
                
                # 关联查询：获取该TextInfo的所有Phrase
                phrases = self.db.query(Phrase).filter(
                    Phrase.text_id == text_info.id
                ).all()
            else:
                # 查询所有词汇
                phrases = self.db.query(Phrase).all()
            
            # 数据转换：转换为响应对象
            phrase_responses = [
                PhraseResponse.model_validate(phrase) for phrase in phrases
            ]
            
            logger.info(f"查询到 {len(phrase_responses)} 个词汇")
            
            # 结果返回
            return {
                "phrases": phrase_responses,
                "total": len(phrase_responses)
            }
            
        except SQLAlchemyError as e:
            logger.error(f"查询词汇数据库错误: {str(e)}")
            raise BusinessException("查询词汇失败", str(e))
        except Exception as e:
            logger.error(f"查询词汇业务错误: {str(e)}")
            raise BusinessException("查询词汇失败", str(e))