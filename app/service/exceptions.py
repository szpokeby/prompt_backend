#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
业务异常模块
"""


class BusinessException(Exception):
    """业务异常类"""
    
    def __init__(self, message: str, detail: str = None):
        """
        初始化业务异常
        
        Args:
            message: 异常消息
            detail: 异常详细信息
        """
        self.message = message
        self.detail = detail
        super().__init__(self.message)