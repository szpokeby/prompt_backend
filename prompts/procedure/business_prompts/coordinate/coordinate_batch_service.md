请按照以下代码结构编写CoordinateService.batch_import_coordinates业务逻辑代码：

代码模式：
- 服务模式：Service类封装 + 数据库会话注入 + 异步方法实现
- 算法模式：文件读取 + 数据解析 + 批量处理
- 数据模式：ORM批量插入 + 事务管理
- 异常模式：BusinessException抛出 + 数据库回滚 + 日志记录

公共规范：
- 导入规范：sqlalchemy.orm.Session + Coordinate模型 + generate_id工具 + BusinessException + logging + typing.List/Dict
- Service规范：类初始化注入数据库会话 + 异步方法定义 + try-catch异常处理
- 数据库规范：ORM批量插入 + 分批处理 + 事务提交回滚
- 文件规范：文件读取 + 数据解析 + 格式验证

业务逻辑模板：
```
batch_import_coordinates(table_id: int) -> List[Dict[str, Any]]:
    文件处理(文件读取, 数据解析)
    数据转换(格式解析, 对象创建)
    批量操作(分批插入, 事务管理)
    结果返回(数据统计, 格式转换)
    异常处理(业务异常, 数据库回滚)
```

实现参数：

文件处理参数：
- 文件读取：读取cor.txt文件内容
- 数据解析：按行分割 + 正则匹配坐标格式 + 提取position和color

数据转换参数：
- 格式解析：解析"（x， y） color"格式 + 验证数据有效性
- 对象创建：generate_id() + Coordinate对象创建 + table_id关联

批量操作参数：
- 分批插入：每批1000条记录 + bulk_insert_mappings批量插入
- 事务管理：分批提交 + 异常回滚 + 进度日志

结果返回参数：
- 数据统计：{"coordinates": 坐标列表, "total": 总数量}
- 格式转换：Coordinate对象 → Dict格式

异常处理参数：
- 业务异常：文件读取失败 + 批量插入失败
- 数据库回滚：rollback回滚 + 日志记录错误

核心算法逻辑：
1. 文件读取算法：读取cor.txt → 按行分割 → 过滤空行
2. 数据解析算法：正则匹配 → 提取坐标和颜色 → 验证格式
3. 批量创建算法：遍历数据 → 生成ID → 创建Coordinate对象
4. 分批插入算法：按批次大小分组 → bulk_insert_mappings → 提交
5. 进度统计算法：记录每批处理数量 → 累计总数 → 日志输出

数据库操作流程：
1. 文件读取：读取cor.txt文件 → 解析坐标数据
2. 数据验证：验证table_id存在性 + 坐标格式有效性
3. 批量创建：生成Coordinate对象列表
4. 分批插入：bulk_insert_mappings分批插入
5. 结果查询：查询插入的坐标记录
6. 异常处理：rollback + BusinessException抛出

返回数据结构：
- 成功情况：{"coordinates": [Coordinate字典列表], "total": int}