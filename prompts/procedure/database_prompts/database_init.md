请为我执行以下数据库初始化操作：

- 创建data/__init__.py包初始化文件；
- 创建data/init_database.py初始化脚本文件；
- 在脚本中编写创建SQLite数据库的代码，数据库名为cube，文件路径./cube.db；
- 根据以下表结构生成创建数据库表格的代码；
- 编写插入TextInfo基础数据的代码；
- 编写执行初始化的主函数；

表结构定义：

Table表：
- id: BigInteger主键
- name: String(255)非空
- create_time: DateTime默认当前时间

TextInfo表：
- id: BigInteger主键
- color: Integer(0-8)非空唯一
- text: String可空默认空字符串

Phrase表：
- id: BigInteger主键
- text_id: BigInteger外键关联TextInfo.id非空
- word: String(255)非空
- type: Integer非空默认0

Coordinate表：
- id: BigInteger主键
- table_id: BigInteger外键关联Table.id非空，字段名"tableId"
- color: Integer(0-8)非空
- position: String(255)非空
- voc: String(255)可空
- repeated: Integer非空默认0

基础数据插入：
- TextInfo表插入9条记录，color分别为0、1、2、3、4、5、6、7、8，text字段为空字符串；
- 所有记录的id字段必须使用雪花算法生成，确保唯一性；
