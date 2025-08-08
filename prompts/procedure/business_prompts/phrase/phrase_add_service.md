请按照以下代码结构编写PhraseService.add_phrase业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 算法模式：工具类调用(可选) + 复杂逻辑分解 + 数据处理流程
- 数据模式：ORM查询 + 批量操作 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚 + 日志记录

公共规范：
- 导入规范：sqlalchemy.orm.Session + models模型类 + utils工具类 + schemas响应类 + typing类型提示
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM查询 + 批量操作 + 事务提交回滚 + flush立即生效
- 算法规范：工具类静态方法调用(可选) + 数据结构转换 + 逻辑步骤分解

业务逻辑模板：
```
add_phrase(color: int, new_text: str) -> Dict[str, Any]:
    数据获取(查询条件, 数据验证)
    算法处理(工具类调用, 数据转换, 逻辑判断)
    数据操作(ORM操作, 批量处理, 关联更新)
    结果返回(数据组装, 格式转换)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

数据获取参数：
- 查询条件：通过color获取TextInfo记录
- 数据验证：TextInfo存在性检查 + 获取old_text和text_info_id

算法处理参数：
- 工具类调用：TextProcessor.split_text_by_comma分割新旧文本 + TextProcessor.find_different_blocks找差异 + TextProcessor.get_block_index_map获取索引映射
- 数据转换：old_blocks/new_blocks/tail_text提取 + diff_phrase_list差异列表
- 逻辑判断：差异列表为空时返回无新增 + 遍历差异文本块处理

数据操作参数：
- ORM操作：query(TextInfo).filter查询 + query(Phrase).all查询 + 新Phrase对象创建 + update更新 + delete删除
- 批量处理：批量插入新词汇 + 文本块计数和编号
- 关联更新：更新TextInfo.text字段 + commit提交事务

结果返回参数：
- 数据组装：构建最终文本 + 组装TextInfo对象字典
- 格式转换：{"message": str, "text_info": dict}格式

异常处理参数：
- 业务异常：文本信息不存在 + 添加词汇失败
- 数据库回滚：rollback回滚 + 日志记录错误

核心算法逻辑：
1. 文本分割算法：按顿号切割 → blocks列表 + tail_text
2. 差异识别算法：Counter统计 → 找出新增文本块
3. 词汇计数算法：全局Phrase统计 → word相同数量count
4. 自动编号算法：count > 0时拼接数字后缀
5. 文本重构算法：modified_blocks + tail_text → final_text

数据库操作流程：
1. 查询操作：filter(color) → TextInfo记录
2. 查询操作：query(Phrase).all() → 统计词汇
3. 创建操作：generate_id() + Phrase对象 → add_all批量插入
4. 更新操作：TextInfo.text更新 → commit提交
5. 异常处理：rollback + BusinessException抛出

返回数据结构：
- 成功情况：{"message": "添加成功", "text_info": {id, color, text}}
- 无新增情况：{"message": "没有新增词汇", "text_info": {id, color, text}}