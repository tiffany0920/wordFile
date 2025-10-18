# 智能文档生成器 - 项目架构结构

## 📁 完整项目结构图

```
智能文档生成器/
├── 📁 核心处理模块
│   ├── config.py              # 配置管理中心
│   ├── llm_client.py          # 通义千问LLM客户端
│   ├── markdown_generator.py  # 智能Markdown生成器
│   ├── word_converter.py      # Word文档转换器
│   └── normalize_media.py     # 媒体文件规范化工具
│
├── 📁 用户界面层
│   ├── main.py               # 命令行界面主程序
│   └── web_app.py            # Streamlit Web界面
│
├── 📁 系统工具层
│   ├── test_system.py        # 系统功能测试脚本
│   ├── run_web.bat          # Windows Web启动脚本
│   └── run_web.sh           # Linux/Mac Web启动脚本
│
├── 📁 配置和依赖
│   ├── requirements.txt      # Python依赖包清单
│   ├── .env.example         # 环境变量配置模板
│   └── .env                 # 用户环境变量配置
│
├── 📁 项目文档
│   ├── README.md            # 项目详细说明文档
│   ├── QUICK_START.md       # 快速开始指南
│   ├── PROJECT_STRUCTURE.md # 项目架构说明
│   └── 项目总结.md          # 项目开发总结
│
└── 📁 输出存储
    └── output/              # 生成的文档和媒体文件存储
        ├── 📄 *.md         # Markdown文档
        ├── 📄 *.docx       # Word文档
        └── 📁 media/       # 图片等媒体资源
```

## 🔄 智能文档生成数据流程图

```
用户输入内容
    ↓
LLMClient (通义千问API调用)
    ↓
生成结构化Markdown内容
    ↓
WordConverter (双向格式转换)
    ↓
输出: Markdown + Word文档 + 媒体资源
```

## 🏗️ 系统架构分层说明

### 1. 📋 配置管理层 (config.py)
- **环境变量管理**: 统一管理DASHSCOPE_API_KEY等配置
- **模型配置**: 支持多种通义千问模型配置
- **模板管理**: 内置多种专业文档模板
- **兼容性支持**: 支持旧版OpenAI配置自动回退

### 2. 🤖 大模型处理层 (llm_client.py)
- **通义千问集成**: 通过DashScope OpenAI兼容协议调用
- **智能生成**: 根据输入内容生成结构化文档
- **文档修订**: 支持基于指令的智能编辑和修改
- **连接管理**: 自动测试连接和错误恢复

### 3. 📝 内容生成层 (markdown_generator.py)
- **智能生成**: 调用LLM生成高质量Markdown内容
- **模板系统**: 支持技术文档、报告、会议纪要等模板
- **文件管理**: 自动命名、版本控制和目录组织
- **内容优化**: 支持自定义提示词和格式控制

### 4. 🔄 文档转换层 (word_converter.py)
- **双向转换**: Markdown ↔ Word文档完整转换
- **高保真输出**: 集成Pandoc引擎的专业级转换
- **媒体处理**: 图片、表格等复杂元素智能处理
- **格式保持**: 完整保留文档结构和样式

### 5. 🖼️ 媒体管理层 (normalize_media.py)
- **路径规范化**: 统一图片和媒体文件路径格式
- **资源同步**: 确保修订版本中媒体文件可用性
- **自动修复**: 智能检测和修复文件引用问题

### 6. 🎨 用户界面层
- **Web界面** (web_app.py):
  - 现代化Streamlit界面
  - 双工作区设计（生成+编辑）
  - 文件上传下载、实时预览
  - 版本历史管理
- **命令行界面** (main.py):
  - 交互式文档生成
  - 系统测试和配置
  - 脚本化支持

### 7. 🛠️ 系统工具层
- **系统测试** (test_system.py): 完整的功能验证测试
- **启动脚本**: 跨平台的应用启动脚本
- **文档系统**: 完整的使用和开发文档

## 🎯 核心技术栈

### 后端技术
- **Python 3.8+**: 核心开发语言
- **通义千问**: 大语言模型服务
- **DashScope API**: 阿里云智能服务API
- **python-docx**: Word文档处理
- **pypandoc**: 高质量文档转换

### 前端技术
- **Streamlit**: Web应用框架
- **Markdown**: 轻量级标记语言
- **HTML/CSS**: 界面样式和布局

### 工具和库
- **python-dotenv**: 环境变量管理
- **requests**: HTTP请求处理
- **logging**: 日志记录系统
- **Pillow**: 图像处理支持
