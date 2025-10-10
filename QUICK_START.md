# 快速开始指南

## 🚀 5分钟快速上手

### 第一步：安装依赖
```bash
pip install -r requirements.txt
```

### 第二步：配置API密钥
```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入您的通义千问（DashScope）API密钥
# DASHSCOPE_API_KEY=your_api_key_here
# QWEN_MODEL=qwen-turbo
# （可选）OPENAI_COMPAT_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 第三步：测试系统
```bash
python test_system.py
```

### 第四步：启动应用

#### 方式一：Web界面（推荐）
```bash
# Windows
run_web.bat

# Linux/Mac
./run_web.sh

# 或直接运行
streamlit run web_app.py
```

#### 方式二：命令行界面
```bash
python main.py
```

## 📝 使用示例

### Web界面使用
1. 打开浏览器访问 `http://localhost:8501`
2. 在左侧输入框中输入内容
3. 选择模板（可选）
4. 点击"生成文档"按钮
5. 下载生成的Markdown和Word文件

### 命令行使用
1. 运行 `python main.py`
2. 选择操作（生成文档）
3. 输入内容（支持多行输入）
4. 选择是否使用自定义提示词
5. 设置文件名
6. 等待生成完成

## 🔧 常见问题

### Q: API密钥在哪里获取？
A: 访问 [OpenAI官网](https://platform.openai.com/api-keys) 注册并获取API密钥。

### Q: 支持哪些模型？
A: 支持所有OpenAI GPT模型，包括gpt-3.5-turbo、gpt-4等。

### Q: 输出文件保存在哪里？
A: 默认保存在 `output/` 目录下，可在配置中修改。

### Q: 如何自定义模板？
A: 在Web界面中选择"自定义提示词"，或修改 `config.py` 中的模板。

## 📊 系统要求

- Python 3.8+
- 网络连接（用于API调用）
- 磁盘空间（用于文件存储）

## 🎯 下一步

- 查看 [README.md](README.md) 了解详细功能
- 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解项目结构
- 运行 `python test_system.py` 进行系统测试
