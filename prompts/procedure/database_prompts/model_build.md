请按照以下代码结构编写数据库相关代码：

代码模式：
- 导入模式：标准SQLAlchemy和Pydantic导入
- 配置模式：Pydantic设置类 + 全局实例
- 连接模式：引擎配置 + 会话管理 + 依赖注入
- 模型模式：继承Base + 主键索引 + 外键关系 + __repr__方法

文件结构：
- 环境配置：.env环境变量文件
- 设置配置：app/config/settings.py应用设置
- 数据库配置：app/config/database.py数据库连接配置
- 模型层：app/models/各个实体模型文件
- 模型包：app/models/__init__.py统一导入

代码结构要求：

环境配置（.env）：
- 数据库连接配置：DATABASE_URL=sqlite:///./cube.db
- 调试模式设置： DEBUG=True


设置配置（app/config/settings.py）：
- Pydantic设置类：database_url: str = "sqlite:///./cube.db"
- 环境变量管理：debug: bool = True
- 全局配置实例：env_file = ".env"

数据库配置（app/config/database.py）：
- SQLAlchemy引擎配置：DATABASE_URL = "sqlite:///./cube.db"
- 会话管理：connect_args={"check_same_thread": False}
- 基础模型类：autocommit=False, autoflush=False
- 依赖注入生成器

模型层（app/models/）：
- ORM模型定义
- 主键索引配置
- 外键关系映射
- 字段类型约束
- 字符串表示方法

模型包（app/models/__init__.py）：
- 统一导入管理
- 模块导出

模型定义要求：

Table模型：
- 表名：table_info
- id: BigInteger主键，索引
- name: String(255)非空
- create_time: DateTime默认当前时间，非空
- 关系：一对多关联Coordinate模型，级联删除

TextInfo模型：
- 表名：text_info
- id: BigInteger主键，索引
- color: Integer(0-8)非空，唯一约束
- text: String可空，默认空字符串
- 关系：一对多关联Phrase模型，级联删除

Phrase模型：
- 表名：phrase
- id: BigInteger主键，索引
- text_id: BigInteger外键关联TextInfo.id，非空，索引，字段名"textId"
- word: String(255)非空
- type: Integer非空，默认0
- 关系：多对一关联TextInfo模型

Coordinate模型：
- 表名：coordinate
- id: BigInteger主键，索引
- table_id: BigInteger外键关联Table.id，非空，索引，字段名"tableId"
- color: Integer非空
- position: String(255)非空
- voc: String(255)可空
- repeated: Integer非空，默认0
- 关系：多对一关联Table模型
