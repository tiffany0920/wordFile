# 项目结构图

```
智能文档生成器/
├── 📁 核心模块
│   ├── config.py              # 配置管理
│   ├── llm_client.py          # 大模型客户端
│   ├── markdown_generator.py  # Markdown生成器
│   └── word_converter.py      # Word转换器
│
├── 📁 用户界面
│   ├── main.py               # 命令行界面
│   └── web_app.py            # Web界面 (Streamlit)
│
├── 📁 配置文件
│   ├── requirements.txt      # 依赖包
│   ├── .env.example         # 环境变量模板
│   └── .env                 # 环境变量 (用户创建)
│
├── 📁 工具脚本
│   ├── test_system.py        # 系统测试
│   ├── run_web.bat          # Windows启动脚本
│   └── run_web.sh           # Linux/Mac启动脚本
│
├── 📁 文档
│   ├── README.md            # 项目说明
│   └── PROJECT_STRUCTURE.md # 项目结构说明
│
└── 📁 输出目录
    └── output/              # 生成的文档存储位置
```

## 数据流程图

```
用户输入内容
    ↓
LLMClient (调用大模型)
    ↓
生成Markdown内容
    ↓
WordConverter (转换格式)
    ↓
输出: Markdown + Word文档
```

## 功能模块说明

### 1. 配置层 (config.py)
- 管理环境变量
- 提供默认配置
- 模板管理

### 2. 大模型层 (llm_client.py)
- OpenAI API调用
- 模型选择
- 连接测试

### 3. 生成层 (markdown_generator.py)
- Markdown内容生成
- 模板系统
- 文件管理

### 4. 转换层 (word_converter.py)
- Markdown到Word转换
- 格式保持
- 样式处理

### 5. 界面层
- 命令行界面 (main.py)
- Web界面 (web_app.py)

### 6. 工具层
- 系统测试 (test_system.py)
- 启动脚本
- 文档说明
