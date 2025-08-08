请按照以下代码结构编写TextInfoService.update_text_info_by_data业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM查询 + 更新操作 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚

公共规范：
- 导入规范：sqlalchemy.orm.Session + TextInfo模型 + BusinessException + typing.Optional
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + merge更新 + 事务提交回滚

业务逻辑模板：
```
update_text_info_by_data(text_info_data: dict) -> TextInfo:
    数据获取(ID查询, 存在性验证)
    数据操作(字段更新, 数据库保存)
    结果返回(更新对象)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据获取参数：
- ID查询：通过text_info_data["id"]获取TextInfo记录
- 存在性验证：检查TextInfo是否存在

数据操作参数：
- 字段更新：更新color和text字段
- 数据库保存：merge更新 + commit提交

结果返回参数：
- 更新对象：返回更新后的TextInfo对象

异常处理参数：
- 业务异常：文本信息不存在 + 更新文本信息失败
- 数据库回滚：rollback回滚 + BusinessException包装

数据库操作流程：
1. 查询操作：get_text_info_by_id() → 获取现有记录
2. 存在性检查：检查记录是否存在 → 不存在抛出异常
3. 更新操作：更新color和text字段
4. 保存操作：merge() + commit() → 保存到数据库
5. 异常处理：rollback() + BusinessException抛出

返回数据结构：
- 成功情况：TextInfo - 更新后的TextInfo对象