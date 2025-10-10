#!/usr/bin/env python3
"""
智能文档生成器 Web 界面
使用 Streamlit 构建的现代化 Web 界面
"""

import streamlit as st
import os
import logging
from datetime import datetime
from markdown_generator import MarkdownGenerator
from word_converter import WordConverter
from llm_client import LLMClient
from config import Config

# 设置页面配置
st.set_page_config(
    page_title="智能文档生成器",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session_state():
    """初始化会话状态"""
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'generated_files' not in st.session_state:
        st.session_state.generated_files = []
    if 'edit_md_content' not in st.session_state:
        st.session_state.edit_md_content = ""
    if 'edit_md_text' not in st.session_state:
        st.session_state.edit_md_text = ""
    if 'refresh_editor' not in st.session_state:
        st.session_state.refresh_editor = False

@st.cache_resource
def get_generator():
    """获取文档生成器实例"""
    try:
        return DocumentGenerator()
    except Exception as e:
        st.error(f"初始化失败: {str(e)}")
        return None

class DocumentGenerator:
    """智能文档生成器类"""
    
    def __init__(self):
        self.markdown_generator = MarkdownGenerator()
        self.word_converter = WordConverter()
        self.llm_client = LLMClient()
    
    def generate_document(self, input_content: str, custom_prompt: str = None,
                         markdown_filename: str = None, word_filename: str = None):
        """生成文档"""
        try:
            # 生成Markdown
            markdown_content, markdown_path = self.markdown_generator.generate_from_content(
                input_content, custom_prompt, markdown_filename
            )
            
            # 转换为Word
            word_path = self.word_converter.markdown_to_word(
                markdown_content, word_filename
            )
            
            return {
                'success': True,
                'markdown_content': markdown_content,
                'markdown_path': markdown_path,
                'word_path': word_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def main():
    """主函数"""
    initialize_session_state()
    
    # 标题
    st.title("📝 智能文档生成器")
    st.markdown("---")
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # API密钥检查（DashScope/Qwen）
        if not Config.DASHSCOPE_API_KEY:
            st.error("⚠️ 请设置 DASHSCOPE_API_KEY 环境变量（兼容OPENAI_API_KEY）")
            st.info("请复制 .env.example 为 .env 并填入您的API密钥")
            return

        st.success("✅ API密钥已配置（通义千问）")

        # 模型选择（通义千问）
        model = st.selectbox(
            "选择模型",
            [Config.QWEN_MODEL, "qwen-turbo", "qwen-plus", "qwen-max"],
            index=0
        )
        
        # 输出目录
        output_dir = st.text_input("输出目录", value=Config.OUTPUT_DIR)
        
        st.markdown("---")
        
        # 模板选择
        st.header("📋 模板选择")
        templates = {
            "默认模板": "使用默认的通用模板",
            "技术文档": "适合技术文档的模板",
            "报告格式": "适合正式报告的模板",
            "会议纪要": "适合会议纪要的模板"
        }
        
        selected_template = st.selectbox("选择模板", list(templates.keys()))
        st.info(templates[selected_template])
    
    # 编辑模式开关
    st.sidebar.markdown("---")
    edit_mode = st.sidebar.toggle("✏️ 开启文档编辑模式", value=False)

    # 主界面
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 输入内容")
        
        # 输入方式选择
        input_method = st.radio(
            "选择输入方式",
            ["直接输入", "上传文件"],
            horizontal=True
        )
        
        input_content = ""
        
        if input_method == "直接输入":
            input_content = st.text_area(
                "请输入要转换的内容:",
                height=300,
                placeholder="在这里输入您的内容..."
            )
        else:
            uploaded_file = st.file_uploader(
                "上传文件",
                type=['txt', 'md'],
                help="支持 .txt 和 .md 文件"
            )
            
            if uploaded_file:
                input_content = str(uploaded_file.read(), "utf-8")
                st.success(f"已上传文件: {uploaded_file.name}")
        
        # 自定义提示词
        st.subheader("🎯 自定义提示词 (可选)")
        use_custom_prompt = st.checkbox("使用自定义提示词")
        
        custom_prompt = None
        if use_custom_prompt:
            custom_prompt = st.text_area(
                "自定义提示词:",
                height=150,
                placeholder="请输入您的自定义提示词...",
                help="使用 {input_content} 作为输入内容的占位符"
            )
        
        # 编辑模式：加载并编辑已有Markdown
        if edit_mode:
            st.subheader("✏️ 编辑已有Markdown")
            md_file = st.file_uploader("上传要编辑的Markdown文件", type=['md'], key="edit_md")
            if md_file is not None:
                load_col1, load_col2 = st.columns([1,1])
                with load_col1:
                    st.caption(f"待载入文件：{md_file.name}")
                with load_col2:
                    if st.button("载入到编辑器", key="btn_load_md"):
                        try:
                            existing_md = md_file.read().decode('utf-8')
                            st.session_state["edit_md_content"] = existing_md
                            st.session_state["refresh_editor"] = True
                            st.success("已载入到编辑器")
                            st.rerun()
                        except Exception as e:
                            st.error(f"加载Markdown失败：{e}")
            # 若需要刷新，先同步编辑器值后再渲染控件
            if st.session_state.get("refresh_editor", False):
                st.session_state["edit_md_text"] = st.session_state.get("edit_md_content", "")
                st.session_state["refresh_editor"] = False

            st.text_area(
                "Markdown内容编辑区",
                value=st.session_state.get("edit_md_content", ""),
                key="edit_md_text",
                height=300,
                placeholder="在这里粘贴或编辑Markdown内容...",
            )
            st.session_state["edit_md_content"] = st.session_state.get("edit_md_text", "")
    
    with col2:
        st.header("⚙️ 输出设置")
        
        # 文件名设置
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            markdown_filename = st.text_input(
                "Markdown文件名",
                value=f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                help="不包含扩展名"
            )
        
        with col2_2:
            word_filename = st.text_input(
                "Word文件名",
                value=f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                help="不包含扩展名"
            )
        
        # 编辑模式：插入图片与表格
        if edit_mode:
            st.markdown("---")
            st.subheader("🖼️ 插入图片 / 表格")
            img_col, tbl_col = st.columns(2)
            with img_col:
                img = st.file_uploader("上传图片以插入", type=["png","jpg","jpeg","gif","bmp"], key="insert_img")
                img_width_in = st.number_input("图片宽度(英寸)", value=5.0, min_value=1.0, max_value=8.0, step=0.5)
                if img is not None:
                    if st.button("保存并插入图片", key="btn_insert_image"):
                        # 将图片保存到输出目录，并在Markdown中插入路径
                        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
                        save_path = os.path.join(Config.OUTPUT_DIR, img.name)
                        try:
                            data = img.read()
                            with open(save_path, 'wb') as f:
                                f.write(data)
                            # 在编辑内容末尾追加Markdown图片语法
                            md_to_append = f"\n\n![{os.path.splitext(img.name)[0]}]({img.name})\n"
                            st.session_state["edit_md_content"] = st.session_state.get("edit_md_content", "") + md_to_append
                            st.session_state["refresh_editor"] = True
                            st.success(f"已保存图片并插入：{save_path}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"保存图片失败：{e}")
            with tbl_col:
                rows = st.number_input("表格行数(含表头)", value=3, min_value=2, max_value=20, step=1)
                cols = st.number_input("表格列数", value=3, min_value=1, max_value=10, step=1)
                if st.button("插入空表格模板", key="btn_insert_table"):
                    header = "| " + " | ".join([f"列{i+1}" for i in range(int(cols))]) + " |\n"
                    sep = "| " + " | ".join(["---" for _ in range(int(cols))]) + " |\n"
                    data = "".join(["| " + " | ".join([" " for _ in range(int(cols))]) + " |\n" for _ in range(int(rows)-1)])
                    st.session_state["edit_md_content"] = st.session_state.get("edit_md_content", "") + "\n\n" + header + sep + data
                    st.session_state["refresh_editor"] = True
                    st.rerun()

        # 生成按钮
        st.markdown("---")
        
        if st.button("🚀 生成文档", type="primary", use_container_width=True):
            try:
                # 优先取编辑模式内容
                if edit_mode and not st.session_state.get("edit_md_text", "").strip():
                    st.error("编辑器内容为空，请先输入或载入内容后再生成。")
                    st.stop()

                if not input_content.strip():
                    if edit_mode and st.session_state.get("edit_md_text", "").strip():
                        input_content = st.session_state["edit_md_text"]
                    else:
                        st.error("请输入内容")
                        st.stop()

                with st.spinner("正在生成文档..."):
                    generator = get_generator()
                    if not generator:
                        st.error("初始化生成器失败")
                        st.stop()
                    # 编辑模式：直接使用编辑后的Markdown
                    if edit_mode and st.session_state.get("edit_md_text", "").strip():
                        edited_md = st.session_state["edit_md_text"]
                        md_path = generator.markdown_generator.save_markdown(
                            edited_md,
                            markdown_filename or f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        )
                        word_path = generator.word_converter.markdown_to_word(edited_md, word_filename)
                        result = {
                            'success': True,
                            'markdown_content': edited_md,
                            'markdown_path': md_path,
                            'word_path': word_path,
                        }
                    else:
                        result = generator.generate_document(
                            input_content,
                            custom_prompt,
                            markdown_filename,
                            word_filename,
                        )

                if result['success']:
                    st.success("✅ 文档生成成功!")
                    st.subheader("📁 生成的文件")
                    col_file1, col_file2 = st.columns(2)
                    with col_file1:
                        st.info(f"📄 Markdown: {os.path.basename(result['markdown_path'])}")
                        if st.button("📥 下载 Markdown", key="download_md"):
                            with open(result['markdown_path'], 'r', encoding='utf-8') as f:
                                st.download_button(
                                    "下载 Markdown 文件",
                                    f.read(),
                                    file_name=os.path.basename(result['markdown_path']),
                                    mime="text/markdown",
                                )
                    with col_file2:
                        st.info(f"📝 Word: {os.path.basename(result['word_path'])}")
                        if st.button("📥 下载 Word", key="download_docx"):
                            with open(result['word_path'], 'rb') as f:
                                st.download_button(
                                    "下载 Word 文件",
                                    f.read(),
                                    file_name=os.path.basename(result['word_path']),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                )
                    st.subheader("👀 Markdown 预览")
                    st.markdown(result['markdown_content'])
                    st.session_state.generated_files.append({
                        'timestamp': datetime.now(),
                        'markdown_path': result['markdown_path'],
                        'word_path': result['word_path'],
                        'content': result['markdown_content'][:200] + "...",
                    })
                else:
                    st.error(f"❌ 生成失败: {result.get('error', '未知错误')}")
            except Exception as gen_e:
                st.exception(gen_e)
    
    # 历史记录
    if st.session_state.generated_files:
        st.markdown("---")
        st.header("📚 生成历史")
        
        for i, file_info in enumerate(reversed(st.session_state.generated_files[-5:])):
            with st.expander(f"文档 {i+1} - {file_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                st.text(f"内容预览: {file_info['content']}")
                st.text(f"Markdown: {file_info['markdown_path']}")
                st.text(f"Word: {file_info['word_path']}")

if __name__ == "__main__":
    main()
