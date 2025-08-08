#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本处理工具类
"""

import re
from typing import List, Dict, Set


class TextProcessor:
    """文本处理工具类"""
    
    @staticmethod
    def split_text_by_comma(text: str) -> List[str]:
        """
        按逗号分割文本
        
        Args:
            text: 待分割的文本
            
        Returns:
            List[str]: 分割后的文本块列表
        """
        if not text:
            return []
        
        # 按逗号分割并去除空白
        blocks = [block.strip() for block in text.split(',')]
        
        # 过滤空字符串
        return [block for block in blocks if block]
    
    @staticmethod
    def find_different_blocks(old_blocks: List[str], new_blocks: List[str]) -> List[str]:
        """
        找出新增的文本块（存在于new_blocks但不存在于old_blocks）
        
        Args:
            old_blocks: 旧文本块列表
            new_blocks: 新文本块列表
            
        Returns:
            List[str]: 新增的文本块列表
        """
        old_set = set(old_blocks) if old_blocks else set()
        new_set = set(new_blocks) if new_blocks else set()
        
        # 找出新增的块
        different_blocks = new_set - old_set
        
        # 保持原始顺序
        return [block for block in new_blocks if block in different_blocks]
    
    @staticmethod
    def find_deleted_blocks(old_blocks: List[str], new_blocks: List[str]) -> List[str]:
        """
        找出删除的文本块（存在于old_blocks但不存在于new_blocks）
        
        Args:
            old_blocks: 旧文本块列表
            new_blocks: 新文本块列表
            
        Returns:
            List[str]: 删除的文本块列表
        """
        old_set = set(old_blocks) if old_blocks else set()
        new_set = set(new_blocks) if new_blocks else set()
        
        # 找出删除的块
        deleted_blocks = old_set - new_set
        
        # 保持原始顺序
        return [block for block in old_blocks if block in deleted_blocks]
    
    @staticmethod
    def get_block_index_map(blocks: List[str]) -> Dict[str, int]:
        """
        获取文本块索引映射
        
        Args:
            blocks: 文本块列表
            
        Returns:
            Dict[str, int]: 文本块到索引的映射
        """
        return {block: index for index, block in enumerate(blocks)}
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        清理文本，去除多余空白字符
        
        Args:
            text: 待清理的文本
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""
        
        # 去除首尾空白
        text = text.strip()
        
        # 将多个连续空白字符替换为单个空格
        text = re.sub(r'\s+', ' ', text)
        
        return text