请按照以下代码结构编写API接口和数据验证代码：

代码模式：
- 验证模式：Pydantic基础模型 + Field字段约束 + 类型提示 + 序列化配置
- 路由模式：FastAPI路由器 + 依赖注入 + 异常处理 + 响应模型绑定
- 集成模式：Schema定义 → Router导入 → Service调用 → 统一异常
- 组织模式：模块分离 + 统一导入 + 标准命名

公共规范：
- 导入规范：pydantic(BaseModel + Field + ConfigDict + field_serializer) + fastapi(APIRouter + Depends + HTTPException + status) + typing(Optional + List)
- Schema规范：基础模型继承 + 字段约束定义 + 序列化器配置 + ConfigDict设置
- Router规范：路由器配置 + HTTP方法装饰器 + 依赖注入 + 异常处理
- 序列化规范：ID字段转字符串 + from_attributes=True + populate_by_name支持
- 路由注册规范：main.py（根目录）中使用app.include_router({module}.router)注册

信息组模板：
```
{模块名}信息组({操作名}):
- 路由信息：{HTTP方法} "{路径}" + prefix="{前缀}" + tags=["{标签}"]
- 数据校验：{请求参数类型}
- 返回信息：{响应数据格式}
- Schema规范：{Schema字段定义}
- 业务规范：{特殊业务逻辑}
```

基础Schema模板：
```
- {Schema名}：{字段定义}
```

实现参数：
TextInfo模块(prefix="/text", tags=["text_info"]):
- 查询信息组(GET "/find", 无参数, List[TextInfoResponse], TextInfoResponse继承Base+id+序列化器)
- 更新信息组(PUT "/update", TextInfoUpdate, TextInfoResponse, TextInfoUpdate含id+color约束0-8+text最大1000)
- 基础Schema：TextInfoBase(color约束0-8 + text可选最大1000) + TextInfoColorUpdate(color约束0-8 + text必需最大1000)

Phrase模块(prefix="/phrase", tags=["phrases"]):
- 添加信息组(POST "/add", TextInfoColorUpdate, Dict含message+text_info, 智能词汇处理+自动编号)
- 删除信息组(DELETE "/delete", TextInfoColorUpdate, Dict含message或message+updated_text_infos, 差异化删除逻辑)
- 查询信息组(GET "/list", color查询参数, PhraseListResponse, PhraseResponse含多ID序列化器)
- 基础Schema：PhraseBase(word长度1-255 + phrase_type非负整数alias="type") + PhraseResponse(id+text_id+word+phrase_type+多ID序列化器+populate_by_name)

Table模块(prefix="/table", tags=["tables"]):
- 创建信息组(POST "/add", TableCreate, TableResponse, TableCreate继承Base+name约束1-255)
- 查询信息组(GET "/page", 无参数, TableListResponse, TableResponse含id+create_time+序列化器)
- 更新信息组(PUT "/update", TableUpdate, message字典, TableUpdate含id+name约束)
- 删除信息组(DELETE "/delete", id查询参数, message字典, 级联删除坐标数据)
- 基础Schema：TableBase(name长度1-255) + TableListResponse(tables列表+total计数)

Coordinate模块(prefix="/coordinate", tags=["coordinates"]):
- 批量导入信息组(GET "/batch", id查询参数, coordinates+total字典, 从cor.txt导入)
- 删除信息组(DELETE "/delete", id查询参数, message字典, 删除表格所有坐标)
- 查询信息组(GET "/find", id查询参数, coordinates+total字典, 获取表格坐标)
- 词汇关联信息组(GET "/list", color+table_id+coordinate_id查询参数, phrases+total字典, 坐标关联词汇)
- 更新信息组(PUT "/update", CoordinateUpdate, coordinates字典, CoordinateUpdate含全字段)
- 基础Schema：CoordinateUpdate(id+table_id+color+position+voc可选默认空+repeated默认0)

路由注册要求：
更新main.py文件（项目根目录），在"# 注册路由"部分添加：
- app.include_router(table.router)
- app.include_router(text_info.router)  
- app.include_router(phrase.router)
- app.include_router(coordinate.router)

导入声明：
在main.py顶部添加：
- from app.routers import table, text_info, phrase, coordinate