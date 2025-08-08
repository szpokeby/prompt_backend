请按照以下代码结构编写CoordinateService.delete_coordinates_by_table业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM批量删除 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚 + 日志记录

公共规范：
- 导入规范：sqlalchemy.orm.Session + Coordinate模型 + BusinessException + logging
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM批量删除 + 事务提交回滚

业务逻辑模板：
```
delete_coordinates_by_table(table_id: int) -> None:
    数据操作(批量删除, 计数统计)
    结果记录(日志记录, 事务提交)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据操作参数：
- 批量删除：query(Coordinate).filter(table_id).delete()
- 计数统计：记录删除的记录数量

结果记录参数：
- 日志记录：记录删除数量和table_id
- 事务提交：commit()提交删除操作

异常处理参数：
- 业务异常：删除坐标数据失败
- 数据库回滚：rollback回滚 + BusinessException包装

数据库操作流程：
1. 删除操作：query(Coordinate).filter(table_id).delete() → 批量删除
2. 计数获取：获取删除的记录数量
3. 日志记录：记录删除数量和table_id信息
4. 提交操作：commit() → 保存到数据库
5. 异常处理：rollback() + BusinessException抛出

返回数据结构：
- 成功情况：None - 无返回值