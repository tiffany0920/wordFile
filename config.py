import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """智能文档生成器配置管理类，包含API密钥、模型参数、输出设置等核心配置信息"""
    
    # 通义千问大模型API配置 - 智能文档生成器的核心LLM服务
    # 支持兼容旧的OpenAI变量以便平滑迁移
    # 优先使用新的DASHSCOPE环境变量，其次回退到旧的OPENAI变量
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY') or os.getenv('OPENAI_API_KEY')
    QWEN_MODEL = os.getenv('QWEN_MODEL') or os.getenv('OPENAI_MODEL', 'qwen-turbo')
    # DashScope提供的OpenAI兼容协议Base URL
    OPENAI_COMPAT_BASE_URL = os.getenv('OPENAI_COMPAT_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    
    # 智能文档生成器输出目录配置
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    
    # 智能文档生成器默认提示词模板 - 用于通义千问LLM生成结构化文档
    DEFAULT_PROMPT_TEMPLATE = """
请根据以下输入内容，生成结构化的Markdown格式文档：

输入内容：{input_content}

要求：
1. 使用标准的Markdown语法
2. 包含适当的标题层级（#、##、###等）
3. 使用列表、表格等格式增强可读性
4. 确保内容结构清晰、逻辑性强
5. 如果内容适合，可以添加代码块、引用等元素

请直接输出Markdown格式的内容，不要包含其他说明文字。
"""
