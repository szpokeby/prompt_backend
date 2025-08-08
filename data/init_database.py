#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite数据库初始化脚本
"""

import sqlite3
import time
import threading
from typing import Optional


class SnowflakeIDGenerator:
    """雪花算法ID生成器"""
    
    def __init__(self, datacenter_id: int = 1, worker_id: int = 1):
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
        
        # 64位ID的组成部分
        self.DATACENTER_ID_BITS = 5
        self.WORKER_ID_BITS = 5
        self.SEQUENCE_BITS = 12
        
        # 最大值
        self.MAX_DATACENTER_ID = -1 ^ (-1 << self.DATACENTER_ID_BITS)
        self.MAX_WORKER_ID = -1 ^ (-1 << self.WORKER_ID_BITS)
        self.MAX_SEQUENCE = -1 ^ (-1 << self.SEQUENCE_BITS)
        
        # 偏移量
        self.WORKER_ID_SHIFT = self.SEQUENCE_BITS
        self.DATACENTER_ID_SHIFT = self.SEQUENCE_BITS + self.WORKER_ID_BITS
        self.TIMESTAMP_LEFT_SHIFT = self.SEQUENCE_BITS + self.WORKER_ID_BITS + self.DATACENTER_ID_BITS
        
        # 起始时间戳 (2023-01-01 00:00:00 UTC)
        self.TWEPOCH = 1672531200000
        
        if self.worker_id > self.MAX_WORKER_ID or self.worker_id < 0:
            raise ValueError(f'worker_id超出范围: {self.worker_id}')
        if self.datacenter_id > self.MAX_DATACENTER_ID or self.datacenter_id < 0:
            raise ValueError(f'datacenter_id超出范围: {self.datacenter_id}')
    
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
            
            return ((timestamp - self.TWEPOCH) << self.TIMESTAMP_LEFT_SHIFT) | \
                   (self.datacenter_id << self.DATACENTER_ID_SHIFT) | \
                   (self.worker_id << self.WORKER_ID_SHIFT) | \
                   self.sequence


class DatabaseInitializer:
    """数据库初始化器"""
    
    def __init__(self, db_path: str = "./cube.db"):
        self.db_path = db_path
        self.id_generator = SnowflakeIDGenerator()
    
    def create_database(self):
        """创建SQLite数据库和表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 创建Table表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS "Table" (
                    id BIGINT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建TextInfo表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TextInfo (
                    id BIGINT PRIMARY KEY,
                    color INTEGER NOT NULL UNIQUE CHECK (color >= 0 AND color <= 8),
                    text TEXT DEFAULT ''
                )
            ''')
            
            # 创建Phrase表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Phrase (
                    id BIGINT PRIMARY KEY,
                    text_id BIGINT NOT NULL,
                    word VARCHAR(255) NOT NULL,
                    type INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (text_id) REFERENCES TextInfo(id)
                )
            ''')
            
            # 创建Coordinate表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Coordinate (
                    id BIGINT PRIMARY KEY,
                    tableId BIGINT NOT NULL,
                    color INTEGER NOT NULL CHECK (color >= 0 AND color <= 8),
                    position VARCHAR(255) NOT NULL,
                    voc VARCHAR(255),
                    repeated INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (tableId) REFERENCES "Table"(id)
                )
            ''')
            
            conn.commit()
            print("数据库表结构创建成功")
            
        except Exception as e:
            print(f"创建数据库表结构失败: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def insert_text_info_data(self):
        """插入TextInfo基础数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 检查是否已有数据
            cursor.execute("SELECT COUNT(*) FROM TextInfo")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print("TextInfo表已有数据，跳过插入")
                return
            
            # 插入9条记录，color分别为0-8
            for color in range(9):
                text_id = self.id_generator.generate_id()
                cursor.execute(
                    "INSERT INTO TextInfo (id, color, text) VALUES (?, ?, ?)",
                    (text_id, color, "")
                )
            
            conn.commit()
            print("TextInfo基础数据插入成功")
            
        except Exception as e:
            print(f"插入TextInfo数据失败: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def verify_database(self):
        """验证数据库结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 检查表是否存在
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('Table', 'TextInfo', 'Phrase', 'Coordinate')
            """)
            tables = [row[0] for row in cursor.fetchall()]
            print(f"已创建的表: {tables}")
            
            # 检查TextInfo数据
            cursor.execute("SELECT COUNT(*) FROM TextInfo")
            text_info_count = cursor.fetchone()[0]
            print(f"TextInfo表记录数: {text_info_count}")
            
            # 显示TextInfo数据
            cursor.execute("SELECT id, color, text FROM TextInfo ORDER BY color")
            text_info_data = cursor.fetchall()
            print("TextInfo数据:")
            for row in text_info_data:
                print(f"  ID: {row[0]}, Color: {row[1]}, Text: '{row[2]}'")
                
        except Exception as e:
            print(f"验证数据库失败: {e}")
            raise
        finally:
            conn.close()
    
    def initialize_database(self):
        """执行完整的数据库初始化"""
        print("开始初始化SQLite数据库...")
        print(f"数据库路径: {self.db_path}")
        
        try:
            # 创建数据库和表结构
            self.create_database()
            
            # 插入基础数据
            self.insert_text_info_data()
            
            # 验证数据库
            self.verify_database()
            
            print("数据库初始化完成！")
            
        except Exception as e:
            print(f"数据库初始化失败: {e}")
            raise


def main():
    """主函数"""
    initializer = DatabaseInitializer()
    initializer.initialize_database()


if __name__ == "__main__":
    main() 