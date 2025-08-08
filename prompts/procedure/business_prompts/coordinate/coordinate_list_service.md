请按照以下代码结构编写CoordinateService.get_phrases_by_coordinate业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM多表关联查询 + 条件筛选
- 异常模式：BusinessException抛出 + 日志记录

公共规范：
- 导入规范：sqlalchemy.orm.Session + TextInfo/Phrase模型 + BusinessException + logging + typing.List/Dict
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM关联查询 + 多条件筛选

业务逻辑模板：
```
get_phrases_by_coordinate(color: int, table_id: int, coordinate_id: int) -> List[Dict[str, Any]]:
    数据获取(关联查询, 条件筛选)
    数据转换(模型转换, 格式转换)
    结果返回(数据统计, 格式包装)
    异常处理(业务异常)
```

实现参数：

数据获取参数：
- 关联查询：通过color获取TextInfo → 查询关联的Phrase列表
- 条件筛选：filter(TextInfo.color) + filter(Phrase.text_id) + coordinate相关条件

数据转换参数：
- 模型转换：Phrase对象 → Dict格式
- 格式转换：包含id、text_id、word、type字段

结果返回参数：
- 数据统计：{"phrases": 词汇列表, "total": 总数量}
- 格式包装：Dict格式包装返回结果 + 日志记录

异常处理参数：
- 业务异常：查询词汇列表失败
- 日志记录：记录查询参数和结果数量

数据库操作流程：
1. 查询操作：query(TextInfo).filter(color) → 获取TextInfo记录
2. 存在性检查：TextInfo不存在 → 返回空结果
3. 关联查询：query(Phrase).filter(text_id) → 获取Phrase列表
4. 数据转换：遍历Phrase → 转换为Dict格式
5. 结果包装：组装phrases和total字段
6. 日志记录：记录查询成功信息
7. 异常处理：Exception → BusinessException包装

业务规范：
- 坐标关联：通过color关联TextInfo，再关联Phrase
- 参数验证：验证color、table_id、coordinate_id的有效性

返回数据结构：
- 成功情况：{"phrases": [Phrase字典列表], "total": int}
- 无数据情况：{"phrases": [], "total": 0}