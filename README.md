# 智能文档生成器

一个基于大模型的智能文档生成工具，能够根据输入内容生成结构化的Markdown文档，并自动转换为Word格式。

## 功能特性

- 🤖 **智能内容生成**: 使用通义千问（DashScope OpenAI兼容接口）将任意内容转换为结构化Markdown
- 📝 **多格式输出**: 同时生成Markdown和Word两种格式
- 🎯 **自定义模板**: 支持多种预设模板和自定义提示词
- 🌐 **Web界面**: 提供现代化的Streamlit Web界面
- 💻 **命令行界面**: 支持命令行交互式操作
- 📁 **文件管理**: 自动管理输出文件和目录

## 安装说明

### 1. 克隆项目
```bash
git clone <repository-url>
cd intelligent-document-generator
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入您的通义千问（DashScope）API密钥
# 新变量（推荐）
DASHSCOPE_API_KEY=your_dashscope_api_key_here
QWEN_MODEL=qwen-turbo
# 可选：如需自定义OpenAI兼容Base URL
# OPENAI_COMPAT_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 兼容旧变量（可选，用于平滑迁移）：
# OPENAI_API_KEY=your_dashscope_api_key_here
# OPENAI_MODEL=qwen-turbo
OUTPUT_DIR=output
```

## 使用方法

### 方法一：Web界面（推荐）

启动Web界面：
```bash
streamlit run web_app.py
```

然后在浏览器中访问 `http://localhost:8501`

### 方法二：命令行界面

运行命令行版本：
```bash
python main.py
```

## 项目结构

```
intelligent-document-generator/
├── main.py                 # 命令行主程序
├── web_app.py             # Streamlit Web界面
├── config.py              # 配置文件
├── llm_client.py          # 大模型客户端
├── markdown_generator.py  # Markdown生成器
├── word_converter.py      # Word转换器
├── requirements.txt       # 依赖包列表
├── .env.example          # 环境变量模板
├── README.md             # 说明文档
└── output/               # 输出目录
```

## 核心组件

### 1. LLMClient (llm_client.py)
- 负责与通义千问（DashScope OpenAI兼容协议）通信
- 支持通义千问模型（例如：qwen-turbo 等）
- 提供连接测试功能

### 2. MarkdownGenerator (markdown_generator.py)
- 调用大模型生成Markdown内容
- 支持多种预设模板
- 自动文件命名和保存

### 3. WordConverter (word_converter.py)
- 将Markdown转换为Word文档
- 支持标题、列表、表格等格式
- 保持文档结构完整性

## 模板系统

系统内置多种模板：

1. **默认模板**: 通用文档格式
2. **技术文档**: 适合技术文档的结构
3. **报告格式**: 正式报告格式
4. **会议纪要**: 会议记录格式

## 配置选项

### 环境变量
- `OPENAI_API_KEY`: OpenAI API密钥（必需）
- `OPENAI_MODEL`: 使用的模型（默认：gpt-3.5-turbo）
- `OUTPUT_DIR`: 输出目录（默认：output）

### 自定义提示词
支持使用自定义提示词模板，使用 `{input_content}` 作为输入内容的占位符。

## 输出格式

### Markdown格式
- 标准Markdown语法
- 支持标题、列表、表格、代码块等
- UTF-8编码

### Word格式
- .docx格式
- 保持Markdown的结构和格式
- 支持标题样式、列表、表格等

## 故障排除

### 常见问题

1. **API密钥错误**
   - 确保在.env文件中正确设置了OPENAI_API_KEY
   - 检查API密钥是否有效且有足够额度

2. **依赖安装失败**
   - 确保Python版本 >= 3.8
   - 使用虚拟环境：`python -m venv venv && source venv/bin/activate`

3. **文件权限错误**
   - 确保对输出目录有写权限
   - 检查磁盘空间是否充足

### 日志查看
程序运行时会输出详细的日志信息，包括：
- API调用状态
- 文件生成过程
- 错误信息

## 开发说明

### 添加新模板
在 `markdown_generator.py` 的 `get_available_templates()` 方法中添加新模板。

### 扩展转换功能
在 `word_converter.py` 中添加新的格式转换支持。

### 自定义界面
修改 `web_app.py` 来自定义Web界面。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过GitHub Issues联系。
