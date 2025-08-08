请按照以下代码结构编写TextInfoService.get_all_text_infos业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM查询 + 排序处理 + 异常处理
- 异常模式：BusinessException抛出 + 日志记录

公共规范：
- 导入规范：sqlalchemy.orm.Session + TextInfo模型 + BusinessException + typing.List + logging
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + 排序操作 + 异常处理

业务逻辑模板：
```
get_all_text_infos() -> List[TextInfo]:
    数据获取(查询条件, 排序规则)
    结果返回(数据列表)
    异常处理(业务异常)
```

实现参数：

数据获取参数：
- 查询条件：查询所有TextInfo记录
- 排序规则：按color字段升序排列

结果返回参数：
- 数据列表：List[TextInfo]对象列表
- 日志记录：记录查询到的记录数量

异常处理参数：
- 业务异常：查询文本信息失败
- 异常处理：BusinessException包装原始异常

数据库操作流程：
1. 查询操作：query(TextInfo) → 获取所有记录
2. 排序操作：order_by(TextInfo.color) → 按颜色排序
3. 结果获取：all() → 返回列表
4. 异常处理：Exception → BusinessException包装

返回数据结构：
- 成功情况：List[TextInfo] - TextInfo对象列表