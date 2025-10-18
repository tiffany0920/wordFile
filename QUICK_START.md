# 智能文档生成器 - 快速开始指南

## 🚀 5分钟快速上手智能文档生成

### 📋 前置要求
- Python 3.8 或更高版本
- 通义千问DashScope API密钥
- 网络连接（用于API调用）

### 🗝️ 第一步：安装依赖
```bash
# 安装Python依赖包
pip install -r requirements.txt

# 如果遇到依赖冲突，建议使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 🔑 第二步：配置API密钥
```bash
# 复制环境变量模板文件
cp .env.example .env

# 编辑 .env 文件，填入您的通义千问API密钥
nano .env  # 或使用其他编辑器
```

**在.env文件中配置以下内容：**
```bash
# 通义千问API配置（必需）
DASHSCOPE_API_KEY=your_dashscope_api_key_here
QWEN_MODEL=qwen-turbo
OPENAI_COMPAT_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OUTPUT_DIR=output

# 兼容性配置（可选）
# OPENAI_API_KEY=your_dashscope_api_key_here
# OPENAI_MODEL=qwen-turbo
```

**📌 获取API密钥：**
1. 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通DashScope服务
4. 在API密钥管理页面创建新密钥

### 🧪 第三步：系统测试
```bash
# 运行系统测试，验证所有功能正常
python test_system.py
```

**测试内容包括：**
- ✅ 模块导入检查
- ✅ API连接验证
- ✅ Markdown生成测试
- ✅ Word转换测试
- ✅ 完整工作流程验证

### 🚀 第四步：启动应用

#### 🌐 方式一：Web界面（强烈推荐）
```bash
# 使用便捷脚本
# Windows用户
run_web.bat

# Linux/Mac用户
./run_web.sh

# 或直接运行Streamlit
streamlit run web_app.py
```

**Web界面功能：**
- 📝 智能文档生成
- 🛠️ 文档编辑修订
- 📁 文件上传下载
- 🖼️ 图片表格插入
- 📚 版本历史管理

#### 💻 方式二：命令行界面
```bash
# 启动交互式命令行界面
python main.py
```

**命令行功能：**
- 🎯 交互式文档生成
- 📋 模板选择
- ⚙️ 自定义配置
- 🧪 系统测试工具

## 📝 使用示例和指南

### 🌐 Web界面详细使用流程
1. **启动访问**: 打开浏览器访问 `http://localhost:8501`
2. **选择工作区**:
   - **"生成新文档"**: 从零开始创建文档
   - **"修改文档"**: 上传现有文档进行编辑
3. **输入内容**:
   - 直接输入文本内容
   - 或上传.txt/.md文件
4. **选择模板**:
   - 默认模板（通用）
   - 技术文档（开发者专用）
   - 报告格式（企业文档）
   - 会议纪要（会议记录）
   - 自定义提示词
5. **配置输出**: 设置文件名（可选）
6. **生成文档**: 点击"🚀 生成文档"按钮
7. **预览下载**: 实时预览并下载生成的文件

### 💻 命令行界面详细使用流程
```bash
# 启动程序
python main.py

# 交互式操作流程：
1. 选择操作类型：
   - 1. 生成文档
   - 2. 查看可用模板
   - 3. 测试系统
   - 4. 退出

2. 输入文档内容（支持多行）：
   - 输入完成后按 Ctrl+Z+Enter（Windows）
   - 或 Ctrl+D（Linux/Mac）

3. 配置生成选项：
   - 是否使用自定义提示词？(y/n)
   - Markdown文件名（回车使用默认）
   - Word文件名（回车使用默认）

4. 等待生成完成，查看输出文件路径
```

### 🛠️ 文档编辑功能（Web界面）
1. **上传文档**: 支持.md和.docx文件
2. **选择提取方式**:
   - 高保真（Pandoc）- 推荐用于复杂文档
   - 简化提取（内置）- 快速处理
3. **在线编辑**:
   - 直接编辑Markdown内容
   - 插入图片和表格
   - 实时预览效果
4. **AI修订**:
   - 输入修订指令（如："优化措辞，添加风险评估"）
   - AI自动修改并生成新版本
5. **导出下载**: 生成修订后的Markdown和Word文件

## ❓ 常见问题解答

### 🔑 API和模型相关
**Q: 通义千问API密钥在哪里获取？**
A: 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)，注册账号后开通服务即可获取API密钥。

**Q: 支持哪些通义千问模型？**
A: 支持qwen-turbo（快速）、qwen-plus（均衡）、qwen-max（高质量）等多种模型。

**Q: API调用有费用吗？**
A: DashScope按调用量计费，新用户通常有免费额度。具体价格请查看阿里云官方定价。

### 📁 文件和输出相关
**Q: 生成的文件保存在哪里？**
A: 默认保存在 `output/` 目录下，包括Markdown文件和Word文档，图片等媒体文件保存在 `output/media/` 目录。

**Q: 支持哪些文件格式？**
A:
- **输入**: .txt、.md、.docx
- **输出**: .md、.docx
- **媒体**: .png、.jpg、.jpeg、.gif、.bmp、.webp

### ⚙️ 配置和自定义相关
**Q: 如何创建自定义模板？**
A: 在Web界面中选择"自定义提示词"，使用 `{input_content}` 作为内容占位符。或在 `config.py` 的 `get_available_templates()` 方法中添加新模板。

**Q: 如何提高生成质量？**
A:
1. 使用更高质量的模型（如qwen-max）
2. 提供更详细的输入内容
3. 使用专业的提示词模板
4. 在生成后使用编辑功能进行优化

### 🐛 故障排除相关
**Q: 系统测试失败怎么办？**
A:
1. 检查网络连接
2. 验证API密钥是否正确
3. 确认账户余额充足
4. 查看详细错误日志

**Q: Word转换出现问题？**
A:
1. 确保已安装Pandoc以获得最佳转换质量
2. 系统会自动回退到内置转换器
3. 检查输出目录权限

## 📊 系统要求

- Python 3.8+
- 网络连接（用于API调用）
- 磁盘空间（用于文件存储）

## 🎯 下一步

- 查看 [README.md](README.md) 了解详细功能
- 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解项目结构
- 运行 `python test_system.py` 进行系统测试
