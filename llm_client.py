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

    def revise_markdown(self, existing_markdown: str, instruction: str, model: Optional[str] = None) -> str:
        """根据用户指令在原有Markdown基础上进行修改并返回新Markdown。

        Args:
            existing_markdown: 现有的Markdown内容
            instruction: 修改说明，如“优化措辞，保留结构，添加一节风险评估”等
            model: 可选，指定覆盖默认模型

        Returns:
            修改后的Markdown内容
        """
        try:
            used_model = model or self.model
            prompt = (
                "你是一个专业的文档编辑助手。请严格输出Markdown，不要额外解释。\n"
                "给定现有Markdown文档与用户修改指令，请在保留合理结构的基础上进行修改。\n"
                "- 保持Markdown语法正确\n"
                "- 允许插入图片与表格（使用标准Markdown语法）\n"
                "- 若用户要求创建新文件，则完整输出修改后的文档\n\n"
                f"[修改指令]\n{instruction}\n\n[现有Markdown]\n{existing_markdown}"
            )
            response = self.client.chat.completions.create(
                model=used_model,
                messages=[
                    {"role": "system", "content": "你是专业的Markdown文档编辑器。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=4000,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"修改Markdown时出错: {str(e)}")
            raise Exception(f"修改Markdown失败: {str(e)}")
