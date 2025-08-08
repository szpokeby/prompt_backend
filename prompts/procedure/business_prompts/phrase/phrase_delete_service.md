请按照以下代码结构编写PhraseService.delete_phrase业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 算法模式：工具类调用 + 复杂逻辑分解 + 差异化处理
- 数据模式：ORM查询 + 批量更新 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚

公共规范：
- 导入规范：sqlalchemy.orm.Session + TextInfo/Phrase模型 + TextProcessor工具类 + BusinessException + re正则 + typing.Dict/List
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + 批量更新 + 事务提交回滚 + flush立即生效
- 算法规范：工具类静态方法调用 + 正则表达式处理 + 条件分支逻辑

业务逻辑模板：
```
delete_phrase(color: int, new_text: str) -> Dict[str, Any]:
    数据获取(查询条件, 数据验证)
    算法处理(工具类调用, 差异分析, 删除策略判断)
    数据操作(删除操作, 更新操作, 批量处理)
    结果返回(差异化返回, 格式转换)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据获取参数：
- 查询条件：通过color获取TextInfo记录
- 数据验证：TextInfo存在性检查 + 获取old_text和text_info_id

算法处理参数：
- 工具类调用：TextProcessor.split_text_by_comma分割新旧文本 + TextProcessor.find_different_blocks找删除块
- 差异分析：对比新旧文本块 + 识别被删除的词汇块
- 删除策略判断：正则检查数字后缀 → 简单删除 vs 复杂删除

数据操作参数：
- 删除操作：删除对应Phrase记录
- 更新操作：更新TextInfo.text + 批量重新编号相关词汇
- 批量处理：查询相关词汇 + 批量更新type和文本

结果返回参数：
- 差异化返回：简单删除返回message / 复杂删除返回message+updated_text_infos
- 格式转换：Dict格式包装

异常处理参数：
- 业务异常：文本信息不存在 + 删除失败
- 数据库回滚：rollback回滚 + 日志记录错误

核心算法逻辑：
1. 文本差异算法：对比新旧文本块 → 找出被删除的词汇
2. 后缀检查算法：正则匹配数字后缀 → 判断删除策略
3. 简单删除算法：直接删除Phrase + 更新TextInfo
4. 复杂删除算法：删除目标 + 重新编号相关词汇 + 批量更新文本
5. 重编号算法：type-1递减 + 文本替换 + 跨TextInfo更新

数据库操作流程：
1. 查询操作：filter(color) → TextInfo记录
2. 差异分析：文本分割比较 → 识别删除块
3. 删除操作：删除目标Phrase记录
4. 更新操作：更新当前TextInfo.text
5. 批量处理：查询相关词汇 + 批量更新type和文本
6. 异常处理：rollback + BusinessException抛出

返回数据结构：
- 简单删除：{"message": "删除成功"}
- 复杂删除：{"message": "删除成功", "updated_text_infos": [TextInfo列表]}