请按照以下代码结构编写TableService.create_table业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM创建 + ID生成 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚 + 日志记录

公共规范：
- 导入规范：sqlalchemy.orm.Session + Table模型 + generate_id工具 + BusinessException + logging
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM创建 + add插入 + 事务提交回滚

业务逻辑模板：
```
create_table(name: str) -> Table:
    数据创建(ID生成, 对象创建)
    数据操作(数据库插入, 事务提交)
    结果返回(创建对象)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据创建参数：
- ID生成：generate_id()生成唯一ID
- 对象创建：Table对象创建 + name字段赋值 + create_time自动设置

数据操作参数：
- 数据库插入：add()添加到会话
- 事务提交：commit()提交事务

结果返回参数：
- 创建对象：返回创建的Table对象
- 日志记录：记录表格创建时间

异常处理参数：
- 业务异常：创建表格失败
- 数据库回滚：rollback回滚 + BusinessException包装

数据库操作流程：
1. 创建操作：Table对象实例化 + 字段赋值
2. 插入操作：add(table) → 添加到会话
3. 提交操作：commit() → 保存到数据库
4. 日志记录：记录创建时间信息
5. 异常处理：rollback() + BusinessException抛出

返回数据结构：
- 成功情况：Table - 创建的Table对象