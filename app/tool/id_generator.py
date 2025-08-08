#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID生成工具
"""

import time
import threading
from typing import Optional


class SnowflakeIdGenerator:
    """雪花算法ID生成器"""
    
    def __init__(self, machine_id: int = 1):
        """
        初始化雪花算法ID生成器
        
        Args:
            machine_id: 机器ID
        """
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
        
        # 各部分位数
        self.MACHINE_ID_BITS = 10
        self.SEQUENCE_BITS = 12
        
        # 最大值
        self.MAX_MACHINE_ID = (1 << self.MACHINE_ID_BITS) - 1
        self.MAX_SEQUENCE = (1 << self.SEQUENCE_BITS) - 1
        
        # 位移
        self.MACHINE_ID_SHIFT = self.SEQUENCE_BITS
        self.TIMESTAMP_SHIFT = self.SEQUENCE_BITS + self.MACHINE_ID_BITS
        
        # 起始时间戳 (2023-01-01 00:00:00 UTC)
        self.EPOCH = 1672531200000
        
        if machine_id > self.MAX_MACHINE_ID or machine_id < 0:
            raise ValueError(f"机器ID必须在0到{self.MAX_MACHINE_ID}之间")
    
    def _get_timestamp(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)
    
    def _wait_for_next_millis(self, last_timestamp: int) -> int:
        """等待到下一个毫秒"""
        timestamp = self._get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_timestamp()
        return timestamp
    
    def generate_id(self) -> int:
        """生成唯一ID"""
        with self.lock:
            timestamp = self._get_timestamp()
            
            if timestamp < self.last_timestamp:
                raise RuntimeError('时钟回拨，拒绝生成ID')
            
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                if self.sequence == 0:
                    timestamp = self._wait_for_next_millis(self.last_timestamp)
            else:
                self.sequence = 0
            
            self.last_timestamp = timestamp
            
            # 组装ID
            return ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
                   (self.machine_id << self.MACHINE_ID_SHIFT) | \
                   self.sequence


# 全局ID生成器实例
_id_generator: Optional[SnowflakeIdGenerator] = None


def get_id_generator() -> SnowflakeIdGenerator:
    """获取全局ID生成器实例"""
    global _id_generator
    if _id_generator is None:
        _id_generator = SnowflakeIdGenerator()
    return _id_generator


def generate_id() -> int:
    """生成唯一ID"""
    return get_id_generator().generate_id()