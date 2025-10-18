#!/usr/bin/env python3
"""
智能文档生成器系统测试脚本
用于验证文档生成、转换、LLM连接等核心功能的完整性
"""

import os
import sys
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """测试智能文档生成器的所有核心模块导入是否正常"""
    try:
        from config import Config
        from llm_client import LLMClient
        from markdown_generator import MarkdownGenerator
        from word_converter import WordConverter
        logger.info("✅ 所有模块导入成功")
        return True
    except Exception as e:
        logger.error(f"❌ 模块导入失败: {str(e)}")
        return False

def test_config():
    """测试智能文档生成器的配置设置，包括API密钥等关键参数"""
    try:
        from config import Config
        
        if not Config.DASHSCOPE_API_KEY:
            logger.warning("⚠️  DASHSCOPE_API_KEY 未设置（兼容OPENAI_API_KEY）")
            return False
        
        logger.info("✅ 配置检查通过")
        return True
    except Exception as e:
        logger.error(f"❌ 配置检查失败: {str(e)}")
        return False

def test_llm_connection():
    """测试智能文档生成器与通义千问LLM的连接状态和API调用能力"""
    try:
        from llm_client import LLMClient
        
        client = LLMClient()
        if client.test_connection():
            logger.info("✅ LLM连接测试成功")
            return True
        else:
            logger.error("❌ LLM连接测试失败")
            return False
    except Exception as e:
        logger.error(f"❌ LLM连接测试失败: {str(e)}")
        return False

def test_markdown_generation():
    """测试智能文档生成器的Markdown内容生成功能"""
    try:
        from markdown_generator import MarkdownGenerator
        
        generator = MarkdownGenerator()
        test_content = "这是一个测试内容，用于验证Markdown生成功能。"
        
        markdown_content, file_path = generator.generate_from_content(
            test_content, 
            filename="test_markdown.md"
        )
        
        if os.path.exists(file_path):
            logger.info("✅ Markdown生成测试成功")
            return True
        else:
            logger.error("❌ Markdown生成测试失败")
            return False
    except Exception as e:
        logger.error(f"❌ Markdown生成测试失败: {str(e)}")
        return False

def test_word_conversion():
    """测试智能文档生成器的Markdown到Word转换功能"""
    try:
        from word_converter import WordConverter
        
        converter = WordConverter()
        test_markdown = """# 测试文档

这是一个测试文档。

## 功能测试

- 列表项1
- 列表项2

### 代码示例

```python
print("Hello, World!")
```
"""
        
        word_path = converter.markdown_to_word(
            test_markdown, 
            "test_word.docx"
        )
        
        if os.path.exists(word_path):
            logger.info("✅ Word转换测试成功")
            return True
        else:
            logger.error("❌ Word转换测试失败")
            return False
    except Exception as e:
        logger.error(f"❌ Word转换测试失败: {str(e)}")
        return False

def test_full_workflow():
    """测试智能文档生成器的完整工作流程：从输入内容到生成Markdown和Word文档"""
    try:
        from main import DocumentGenerator
        
        generator = DocumentGenerator()
        test_content = "这是一个完整工作流程测试，包含多个段落和不同的内容类型。"
        
        result = generator.generate_document(test_content)
        
        if result['success']:
            logger.info("✅ 完整工作流程测试成功")
            return True
        else:
            logger.error(f"❌ 完整工作流程测试失败: {result.get('error', '未知错误')}")
            return False
    except Exception as e:
        logger.error(f"❌ 完整工作流程测试失败: {str(e)}")
        return False

def main():
    """智能文档生成器系统测试主函数"""
    print("=" * 60)
    print("智能文档生成器 - 系统功能完整性测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("配置检查", test_config),
        ("LLM连接", test_llm_connection),
        ("Markdown生成", test_markdown_generation),
        ("Word转换", test_word_conversion),
        ("完整工作流程", test_full_workflow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 测试: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
        except Exception as e:
            logger.error(f"测试 {test_name} 时发生异常: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
        return True
    else:
        print("⚠️  部分测试失败，请检查配置和依赖。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
