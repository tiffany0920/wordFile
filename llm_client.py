import openai
from typing import Optional
from config import Config
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    """大模型客户端类"""
    
    def __init__(self):
        """初始化LLM客户端"""
        if not Config.DASHSCOPE_API_KEY:
            raise ValueError("请设置DASHSCOPE_API_KEY环境变量（兼容OPENAI_API_KEY）")

        # 使用OpenAI兼容的Base URL调用通义千问（DashScope）
        self.client = openai.OpenAI(
            api_key=Config.DASHSCOPE_API_KEY,
            base_url=Config.OPENAI_COMPAT_BASE_URL,
        )
        self.model = Config.QWEN_MODEL
    
    def generate_markdown(self, input_content: str, custom_prompt: Optional[str] = None) -> str:
        """
        根据输入内容生成Markdown格式文档
        
        Args:
            input_content: 输入的内容
            custom_prompt: 自定义提示词，如果为None则使用默认模板
            
        Returns:
            生成的Markdown内容
        """
        try:
            # 使用自定义提示词或默认模板
            if custom_prompt:
                prompt = custom_prompt.format(input_content=input_content)
            else:
                prompt = Config.DEFAULT_PROMPT_TEMPLATE.format(input_content=input_content)
            
            logger.info("开始调用大模型生成Markdown内容...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文档生成助手，擅长将各种内容转换为结构化的Markdown格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            markdown_content = response.choices[0].message.content.strip()
            logger.info("Markdown内容生成完成")
            
            return markdown_content
            
        except Exception as e:
            logger.error(f"生成Markdown内容时出错: {str(e)}")
            raise Exception(f"生成Markdown内容失败: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        测试与通义千问（DashScope OpenAI兼容接口）的连接
        
        Returns:
            连接是否成功
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            logger.info("API连接测试成功")
            return True
        except Exception as e:
            logger.error(f"API连接测试失败: {str(e)}")
            return False
