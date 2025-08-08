请按照以下代码结构编写CoordinateService.update_coordinate业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM查询 + 更新操作 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚

公共规范：
- 导入规范：sqlalchemy.orm.Session + Coordinate模型 + BusinessException + typing.List/Dict
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + 字段更新 + 事务提交回滚

业务逻辑模板：
```
update_coordinate(coordinate_id: int, coordinate_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    数据获取(ID查询, 存在性验证)
    数据操作(字段更新, 事务提交)
    结果返回(更新对象, 格式转换)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据获取参数：
- ID查询：通过coordinate_id查询Coordinate记录
- 存在性验证：检查Coordinate是否存在

数据操作参数：
- 字段更新：更新table_id、color、position、voc、repeated字段
- 事务提交：commit()提交更新

结果返回参数：
- 更新对象：返回更新后的Coordinate对象
- 格式转换：{"coordinates": [Coordinate字典]}格式

异常处理参数：
- 业务异常：坐标不存在 + 更新坐标失败
- 数据库回滚：rollback回滚 + BusinessException包装

数据库操作流程：
1. 查询操作：query(Coordinate).filter(id) → 获取Coordinate记录
2. 存在性检查：检查记录是否存在 → 不存在抛出异常
3. 更新操作：更新各字段值
4. 提交操作：commit() → 保存到数据库
5. 结果转换：Coordinate对象 → Dict格式
6. 异常处理：rollback() + BusinessException抛出

返回数据结构：
- 成功情况：{"coordinates": [Coordinate字典]}