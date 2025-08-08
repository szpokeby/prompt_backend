请按照以下代码结构编写PhraseService.get_phrases_by_color业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 数据模式：ORM查询 + 关联查询 + 数据转换
- 异常模式：BusinessException抛出

公共规范：
- 导入规范：sqlalchemy.orm.Session + TextInfo/Phrase模型 + PhraseResponse响应类 + BusinessException + typing.List
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM关联查询 + filter条件筛选

业务逻辑模板：
```
get_phrases_by_color(color: int) -> List[PhraseResponse]:
    数据获取(关联查询, 条件筛选)
    数据转换(模型转换, 响应格式)
    结果返回(数据列表)
    异常处理(业务异常)
```

实现参数：

数据获取参数：
- 关联查询：通过color获取TextInfo → 查询关联的Phrase列表
- 条件筛选：filter(TextInfo.color) + filter(Phrase.text_id)

数据转换参数：
- 模型转换：Phrase模型 → PhraseResponse响应对象
- 响应格式：id + text_id + word + phrase_type字段映射

结果返回参数：
- 数据列表：List[PhraseResponse]对象列表
- 空列表处理：TextInfo不存在时返回空列表

异常处理参数：
- 业务异常：查询词汇失败
- 异常处理：BusinessException包装原始异常

数据库操作流程：
1. 查询操作：query(TextInfo).filter(color) → 获取TextInfo记录
2. 存在性检查：TextInfo不存在 → 返回空列表
3. 关联查询：query(Phrase).filter(text_id) → 获取Phrase列表
4. 数据转换：遍历Phrase → 转换为PhraseResponse
5. 异常处理：Exception → BusinessException包装

返回数据结构：
- 成功情况：List[PhraseResponse] - PhraseResponse对象列表
- 无数据情况：[] - 空列表