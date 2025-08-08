# 后端项目

## 项目结构

```
├── app/                    # 业务主模块
│   ├── controller/         # 控制器层
│   ├── service/           # 服务层
│   ├── model/             # 数据模型
│   ├── schema/            # 数据模式
│   ├── config/            # 配置文件
│   └── tool/              # 工具类
├── data/                  # 数据库初始化
├── prompts/               # 提示词文档
├── tests/                 # 测试文件
├── main.py                # 主入口文件
├── requirements.txt       # 依赖包
├── .gitignore            # Git忽略文件
└── README.md             # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 开发说明

- 严格按照模块化架构设计
- 遵循分层架构原则
- 保持代码整洁和可维护性 