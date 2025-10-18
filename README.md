# 智能文档生成器

一个基于通义千问大模型的智能文档生成系统，能够根据输入内容智能生成结构化的Markdown文档，并自动转换为Word格式。支持文档编辑、双向转换、媒体资源管理等高级功能。

## 🌟 核心功能特性

- 🤖 **智能文档生成**: 集成通义千问大模型（DashScope API），将任意内容智能转换为结构化Markdown文档
- 📝 **多格式支持**: 同时生成Markdown和Word文档，支持双向转换（Word ↔ Markdown）
- 🎯 **专业模板系统**: 内置技术文档、报告格式、会议纪要等多种专业模板，支持自定义提示词
- 🌐 **现代化Web界面**: 基于Streamlit的直观Web界面，支持文件上传、实时预览、版本管理
- 💻 **命令行工具**: 功能完整的命令行界面，支持脚本化和批量处理
- 🔄 **文档编辑修订**: 支持上传现有文档进行AI辅助编辑和智能修订
- 🖼️ **媒体资源管理**: 自动处理图片插入、路径管理和资源同步
- 📚 **版本历史管理**: 独立的生成和编辑历史记录，支持版本回滚和比较
- 🛠️ **高保真转换**: 集成Pandoc引擎，提供专业级的文档格式转换质量

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
# 主要配置（推荐）
DASHSCOPE_API_KEY=your_dashscope_api_key_here
QWEN_MODEL=qwen-turbo
OPENAI_COMPAT_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OUTPUT_DIR=output

# 兼容性配置（自动回退支持）
# OPENAI_API_KEY=your_dashscope_api_key_here
# OPENAI_MODEL=qwen-turbo
```

**📌 获取API密钥**：
- 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
- 注册/登录阿里云账号
- 开通DashScope服务并获取API密钥

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

## 🏗️ 核心架构组件

### 1. LLMClient (llm_client.py) - 智能处理核心
- **通义千问集成**: 通过DashScope OpenAI兼容协议与通义千问大模型通信
- **模型支持**: 支持qwen-turbo、qwen-plus、qwen-max等多种通义千问模型
- **智能编辑**: 提供文档修订和内容增强功能
- **连接管理**: 自动连接测试和错误恢复机制

### 2. MarkdownGenerator (markdown_generator.py) - 内容生成引擎
- **智能生成**: 调用通义千问LLM生成高质量Markdown内容
- **模板系统**: 内置技术文档、报告、会议纪要等专业模板
- **文件管理**: 自动文件命名、版本管理和目录组织

### 3. WordConverter (word_converter.py) - 格式转换中心
- **双向转换**: 支持Markdown ↔ Word文档的双向转换
- **高保真输出**: 集成Pandoc引擎，提供专业级转换质量
- **媒体处理**: 自动处理图片、表格等复杂元素的转换
- **格式保持**: 完整保留文档结构、样式和格式

### 4. Web界面 (web_app.py) - 现代化交互平台
- **双标签设计**: 独立的"生成新文档"和"修改文档"工作区
- **文件处理**: 支持拖拽上传、在线编辑、实时预览
- **媒体管理**: 图片插入、表格创建、资源同步
- **版本控制**: 历史记录、版本回滚、变更追踪

## 📋 专业模板系统

智能文档生成器内置多种专业模板，适用于不同场景：

### 🏢 企业文档模板
1. **默认模板**: 通用业务文档格式，适用于日常办公需求
2. **报告格式**: 标准企业报告结构，包含摘要、正文、结论等部分
3. **会议纪要**: 专业会议记录格式，包含参会人员、议题、决议等要素

### 🛠️ 技术文档模板
4. **技术文档**: 面向开发者和工程师的技术规范文档
   - 清晰的技术文档结构
   - 代码块和表格支持
   - API文档格式优化

### 🎨 自定义模板
- **灵活定制**: 支持用户自定义提示词模板
- **占位符系统**: 使用 `{input_content}` 作为内容占位符
- **格式控制**: 精确控制输出格式和结构

## ⚙️ 配置选项

### 环境变量配置
- `DASHSCOPE_API_KEY`: 通义千问API密钥（**必需**）
- `QWEN_MODEL`: 使用的通义千问模型（默认：qwen-turbo）
- `OPENAI_COMPAT_BASE_URL`: DashScope OpenAI兼容接口地址
- `OUTPUT_DIR`: 文档输出目录（默认：output）

### 支持的通义千问模型
- **qwen-turbo**: 快速响应，适合一般文档生成
- **qwen-plus**: 平衡性能和质量，推荐日常使用
- **qwen-max**: 最高质量输出，适合重要文档

### 兼容性配置
系统支持以下环境变量作为备选（自动回退机制）：
- `OPENAI_API_KEY`: 兼容旧配置
- `OPENAI_MODEL`: 兼容旧模型配置

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

## 🔧 故障排除

### 常见问题解决方案

1. **🔑 API密钥相关问题**
   - **问题**: API密钥无效或未配置
   - **解决**:
     - 确保在.env文件中正确设置了 `DASHSCOPE_API_KEY`
     - 访问 [DashScope控制台](https://dashscope.console.aliyun.com/) 确认API密钥状态
     - 检查账户余额和API调用额度

2. **📦 依赖安装问题**
   - **问题**: pip安装依赖失败
   - **解决**:
     - 确保Python版本 >= 3.8
     - 使用虚拟环境：`python -m venv venv && source venv/bin/activate`
     - 升级pip：`pip install --upgrade pip`

3. **📁 文件和权限问题**
   - **问题**: 无法创建输出文件
   - **解决**:
     - 确保对输出目录有写权限
     - 检查磁盘空间是否充足
     - 创建输出目录：`mkdir -p output`

4. **🌐 网络连接问题**
   - **问题**: 无法连接到DashScope API
   - **解决**:
     - 检查网络连接和防火墙设置
     - 确认API地址可访问：`curl https://dashscope.aliyuncs.com`

5. **🔄 Pandoc转换问题**
   - **问题**: 高保真转换失败
   - **解决**:
     - 安装Pandoc：[官方下载页面](https://pandoc.org/installing.html)
     - 系统会自动回退到内置转换器

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
