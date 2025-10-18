import os
import logging
from datetime import datetime
from typing import Optional
from llm_client import LLMClient
from config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarkdownGenerator:
    """智能文档生成器的Markdown生成器类，负责通过LLM生成结构化的Markdown内容"""
    
    def __init__(self):
        """初始化智能文档生成器的Markdown生成器"""
        self.llm_client = LLMClient()
        self.output_dir = Config.OUTPUT_DIR
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_from_content(self, input_content: str, custom_prompt: Optional[str] = None,
                            filename: Optional[str] = None) -> tuple[str, str]:
        """
        智能文档生成器核心功能：根据输入内容通过LLM生成结构化的Markdown文档

        Args:
            input_content: 用户输入的原始内容，将被LLM转换为结构化文档
            custom_prompt: 自定义提示词模板（可选），用于定制生成风格和格式
            filename: 指定输出Markdown文件名（可选），默认自动生成带时间戳的文件名

        Returns:
            (markdown_content, file_path) 元组，包含生成的Markdown内容和保存的文件路径
        """
        try:
            logger.info("开始生成Markdown内容...")
            
            # 调用LLM生成Markdown内容
            markdown_content = self.llm_client.generate_markdown(input_content, custom_prompt)
            
            # 生成文件名
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_document_{timestamp}.md"
            elif not filename.endswith('.md'):
                filename += '.md'
            
            # 构建完整文件路径
            file_path = os.path.join(self.output_dir, filename)
            
            # 保存Markdown文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Markdown文件已保存: {file_path}")
            
            return markdown_content, file_path
            
        except Exception as e:
            logger.error(f"生成Markdown文档时出错: {str(e)}")
            raise Exception(f"生成Markdown文档失败: {str(e)}")
    
    def save_markdown(self, markdown_content: str, filename: str) -> str:
        """
        智能文档生成器辅助功能：将Markdown内容保存到文件

        Args:
            markdown_content: 要保存的Markdown格式内容
            filename: 目标文件名（会自动添加.md扩展名）

        Returns:
            保存后的完整文件路径
        """
        try:
            if not filename.endswith('.md'):
                filename += '.md'
            
            file_path = os.path.join(self.output_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Markdown文件已保存: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"保存Markdown文件时出错: {str(e)}")
            raise Exception(f"保存Markdown文件失败: {str(e)}")
    
    def get_available_templates(self) -> dict:
        """
        智能文档生成器模板管理功能：获取所有可用的文档生成提示词模板

        Returns:
            包含各种文档类型的提示词模板字典，如技术文档、报告格式、会议纪要等
        """
        templates = {
            "默认模板": Config.DEFAULT_PROMPT_TEMPLATE,
            "技术文档": """
请将以下内容转换为技术文档格式的Markdown：

输入内容：{input_content}

要求：
1. 使用清晰的技术文档结构
2. 包含目录、概述、详细说明等部分
3. 使用代码块、表格等格式
4. 确保技术术语准确
""",
            "报告格式": """
请将以下内容转换为正式报告格式的Markdown：

输入内容：{input_content}

要求：
1. 使用正式的报告结构
2. 包含摘要、正文、结论等部分
3. 使用适当的标题层级
4. 确保内容逻辑清晰
""",
            "会议纪要": """
请将以下内容转换为会议纪要格式的Markdown：

输入内容：{input_content}

要求：
1. 使用会议纪要的标准格式
2. 包含会议信息、参会人员、议题、决议等
3. 使用列表和表格整理信息
4. 确保时间线清晰
"""
        }
        return templates
