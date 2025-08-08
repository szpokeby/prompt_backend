请按照以下代码结构编写TableService.delete_table业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM查询 + 删除操作 + 级联删除 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚

公共规范：
- 导入规范：sqlalchemy.orm.Session + Table模型 + BusinessException
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + delete删除 + 级联删除 + 事务提交回滚

业务逻辑模板：
```
delete_table(table_id: int) -> None:
    数据获取(ID查询, 存在性验证)
    数据操作(删除操作, 级联删除, 事务提交)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据获取参数：
- ID查询：通过table_id查询Table记录
- 存在性验证：检查Table是否存在

数据操作参数：
- 删除操作：delete(table)删除Table记录
- 级联删除：数据库级联删除关联的Coordinate记录
- 事务提交：commit()提交删除

异常处理参数：
- 业务异常：表格不存在 + 删除表格失败
- 数据库回滚：rollback回滚 + BusinessException包装

数据库操作流程：
1. 查询操作：query(Table).filter(id) → 获取Table记录
2. 存在性检查：检查记录是否存在 → 不存在抛出异常
3. 删除操作：delete(table) → 删除Table记录
4. 级联删除：数据库自动删除关联的Coordinate记录
5. 提交操作：commit() → 保存到数据库
6. 异常处理：rollback() + BusinessException抛出

业务规范：
- 级联删除：Table删除时自动删除所有关联的Coordinate记录
- 数据一致性：确保删除操作的原子性

返回数据结构：
- 成功情况：None - 无返回值