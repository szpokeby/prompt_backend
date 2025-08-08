请按照以下代码结构编写CoordinateService.get_coordinates_by_table业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM查询 + 数据转换
- 异常模式：BusinessException抛出

公共规范：
- 导入规范：sqlalchemy.orm.Session + Coordinate模型 + BusinessException + typing.List/Dict
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + filter条件筛选

业务逻辑模板：
```
get_coordinates_by_table(table_id: int) -> List[Dict[str, Any]]:
    数据获取(条件查询, 结果获取)
    数据转换(模型转换, 格式转换)
    结果返回(数据统计, 格式包装)
    异常处理(业务异常)
```

实现参数：

数据获取参数：
- 条件查询：query(Coordinate).filter(table_id)
- 结果获取：all()获取所有匹配记录

数据转换参数：
- 模型转换：Coordinate对象 → Dict格式
- 格式转换：包含id、table_id、color、position、voc、repeated字段

结果返回参数：
- 数据统计：{"coordinates": 坐标列表, "total": 总数量}
- 格式包装：Dict格式包装返回结果

异常处理参数：
- 业务异常：查询坐标数据失败
- 异常处理：BusinessException包装原始异常

数据库操作流程：
1. 查询操作：query(Coordinate).filter(table_id) → 获取坐标记录
2. 结果获取：all() → 返回列表
3. 数据转换：遍历Coordinate → 转换为Dict格式
4. 结果包装：组装coordinates和total字段
5. 异常处理：Exception → BusinessException包装

返回数据结构：
- 成功情况：{"coordinates": [Coordinate字典列表], "total": int}