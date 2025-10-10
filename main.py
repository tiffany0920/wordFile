#!/usr/bin/env python3
"""
智能文档生成器主程序
支持根据输入内容生成Markdown，并转换为Word文档
"""

import os
import sys
import logging
from typing import Optional
from markdown_generator import MarkdownGenerator
from word_converter import WordConverter
from llm_client import LLMClient
from config import Config

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DocumentGenerator:
    """智能文档生成器主类"""
    
    def __init__(self):
        """初始化文档生成器"""
        self.markdown_generator = MarkdownGenerator()
        self.word_converter = WordConverter()
        self.llm_client = LLMClient()
    
    def generate_document(self, input_content: str, custom_prompt: Optional[str] = None,
                         markdown_filename: Optional[str] = None,
                         word_filename: Optional[str] = None) -> dict:
        """
        生成完整文档（Markdown + Word）
        
        Args:
            input_content: 输入内容
            custom_prompt: 自定义提示词
            markdown_filename: Markdown文件名
            word_filename: Word文件名
            
        Returns:
            包含生成文件路径的字典
        """
        try:
            logger.info("开始生成文档...")
            
            # 1. 生成Markdown内容
            markdown_content, markdown_path = self.markdown_generator.generate_from_content(
                input_content, custom_prompt, markdown_filename
            )
            
            # 2. 转换为Word文档
            word_path = self.word_converter.markdown_to_word(
                markdown_content, word_filename
            )
            
            result = {
                'success': True,
                'markdown_content': markdown_content,
                'markdown_path': markdown_path,
                'word_path': word_path,
                'message': '文档生成成功'
            }
            
            logger.info(f"文档生成完成: Markdown={markdown_path}, Word={word_path}")
            return result
            
        except Exception as e:
            logger.error(f"生成文档时出错: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': '文档生成失败'
            }
    
    def test_system(self) -> bool:
        """测试系统功能"""
        try:
            logger.info("测试系统功能...")
            
            # 测试LLM连接
            if not self.llm_client.test_connection():
                logger.error("LLM连接测试失败")
                return False
            
            # 测试简单内容生成
            test_content = "这是一个测试内容，用于验证系统功能。"
            result = self.generate_document(test_content)
            
            if result['success']:
                logger.info("系统功能测试通过")
                return True
            else:
                logger.error(f"系统功能测试失败: {result.get('error', '未知错误')}")
                return False
                
        except Exception as e:
            logger.error(f"系统测试时出错: {str(e)}")
            return False

def main():
    """主函数"""
    print("=" * 60)
    print("智能文档生成器")
    print("=" * 60)
    
    # 检查配置
    if not Config.DASHSCOPE_API_KEY:
        print("错误: 请设置DASHSCOPE_API_KEY环境变量")
        print("请复制 .env.example 为 .env 并填入您的API密钥")
        return
    
    # 初始化生成器
    generator = DocumentGenerator()
    
    # 测试系统
    print("正在测试系统功能...")
    if not generator.test_system():
        print("系统测试失败，请检查配置")
        return
    
    print("系统测试通过！")
    print()
    
    # 主循环
    while True:
        print("\n" + "=" * 40)
        print("请选择操作:")
        print("1. 生成文档")
        print("2. 查看可用模板")
        print("3. 测试系统")
        print("4. 退出")
        print("=" * 40)
        
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == '1':
            # 生成文档
            print("\n请输入要转换的内容 (输入完成后按Ctrl+Z+Enter结束):")
            print("(Windows: Ctrl+Z+Enter, Linux/Mac: Ctrl+D)")
            
            try:
                content_lines = []
                while True:
                    try:
                        line = input()
                        content_lines.append(line)
                    except EOFError:
                        break
                
                input_content = '\n'.join(content_lines)
                
                if not input_content.strip():
                    print("输入内容为空，请重新输入")
                    continue
                
                # 询问是否使用自定义提示词
                use_custom = input("\n是否使用自定义提示词? (y/n): ").strip().lower()
                custom_prompt = None
                
                if use_custom == 'y':
                    print("请输入自定义提示词:")
                    custom_prompt = input()
                
                # 询问文件名
                markdown_filename = input("\nMarkdown文件名 (回车使用默认): ").strip()
                if not markdown_filename:
                    markdown_filename = None
                
                word_filename = input("Word文件名 (回车使用默认): ").strip()
                if not word_filename:
                    word_filename = None
                
                # 生成文档
                print("\n正在生成文档...")
                result = generator.generate_document(
                    input_content, custom_prompt, markdown_filename, word_filename
                )
                
                if result['success']:
                    print(f"\n✅ 文档生成成功!")
                    print(f"📄 Markdown文件: {result['markdown_path']}")
                    print(f"📝 Word文件: {result['word_path']}")
                else:
                    print(f"\n❌ 文档生成失败: {result['message']}")
                    
            except KeyboardInterrupt:
                print("\n操作已取消")
                continue
        
        elif choice == '2':
            # 查看可用模板
            templates = generator.markdown_generator.get_available_templates()
            print("\n可用模板:")
            for name, template in templates.items():
                print(f"\n{name}:")
                print("-" * 20)
                print(template[:200] + "..." if len(template) > 200 else template)
        
        elif choice == '3':
            # 测试系统
            print("\n正在测试系统...")
            if generator.test_system():
                print("✅ 系统测试通过")
            else:
                print("❌ 系统测试失败")
        
        elif choice == '4':
            # 退出
            print("感谢使用智能文档生成器！")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()
