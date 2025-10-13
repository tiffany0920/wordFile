#!/usr/bin/env python3
"""
智能文档生成器 Web 界面（重构版）
使用 Streamlit 构建的现代化 Web 界面
📘 功能说明：
  - 拆分为两个主标签页：「生成新文档」与「修改文档」
  - 保留所有原有功能（包括 Pandoc、编辑模式、图片/表格插入、修订）
  - 各部分独立历史与回滚
  - 优化侧边栏间距
"""

import streamlit as st
import os
import logging
from datetime import datetime
from markdown_generator import MarkdownGenerator
from word_converter import WordConverter
from llm_client import LLMClient
from config import Config


# ======================
# 页面与日志配置
# ======================

st.set_page_config(
    page_title="智能文档生成器",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================
# Session 初始化
# ======================
def initialize_session_state():
    """初始化会话状态"""
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'generated_files_new' not in st.session_state:
        st.session_state.generated_files_new = []
    if 'generated_files_edit' not in st.session_state:
        st.session_state.generated_files_edit = []
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


# ======================
# 文档生成器类定义
# ======================
class DocumentGenerator:
    """智能文档生成器类"""

    def __init__(self):
        self.markdown_generator = MarkdownGenerator()
        self.word_converter = WordConverter()
        self.llm_client = LLMClient()

    def generate_document(self, input_content: str, custom_prompt: str = None,
                         markdown_filename: str = None, word_filename: str = None):
        """生成Markdown + Word文档"""
        try:
            markdown_content, markdown_path = self.markdown_generator.generate_from_content(
                input_content, custom_prompt, markdown_filename
            )
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
            return {'success': False, 'error': str(e)}


# ======================
# 主函数入口
# ======================
def main():
    """主函数"""
    initialize_session_state()

    # 页面标题
    st.title("📝 智能文档生成器")
    st.markdown("---")

    # ======================
    # 侧边栏配置（更紧凑）
    # ======================
    with st.sidebar:
        st.markdown("### ⚙️ 配置")

        if not Config.DASHSCOPE_API_KEY:
            st.error("⚠️ 请设置 DASHSCOPE_API_KEY 环境变量")
            st.info("请复制 .env.example 为 .env 并填入您的API密钥")
            st.stop()
        st.success("✅ API密钥已配置（通义千问）")

        model = st.selectbox(
            "选择模型",
            [Config.QWEN_MODEL, "qwen-turbo", "qwen-plus", "qwen-max"],
            index=0
        )

        output_dir = st.text_input("输出目录", value=Config.OUTPUT_DIR)
        st.caption("默认存放生成的 Markdown 和 Word 文件")

        st.markdown("<hr style='margin:0.3rem 0;'>", unsafe_allow_html=True)
        st.markdown("#### 📋 模板选择")

        templates = {
            "默认模板": "使用默认的通用模板",
            "技术文档": "适合技术文档的模板",
            "报告格式": "适合正式报告的模板",
            "会议纪要": "适合会议纪要的模板"
        }
        selected_template = st.selectbox("选择模板", list(templates.keys()))
        st.info(templates[selected_template])

        st.markdown("<hr style='margin:0.3rem 0;'>", unsafe_allow_html=True)
        edit_mode = st.toggle("✏️ 启用文档编辑模式", value=False)
        st.caption("开启后可加载、修改、插入表格或图片")
    
    # ======================
    # 主体内容区域（两个标签页）
    # ======================
    tab_new, tab_edit = st.tabs(["🆕 生成新文档", "🛠️ 修改文档"])

    # ----------------------
    # 🆕 生成新文档
    # ----------------------
    with tab_new:
        st.subheader("📝 输入内容")
        input_method = st.radio("选择输入方式", ["直接输入", "上传文件"], horizontal=True)

        input_content = ""
        if input_method == "直接输入":
            input_content = st.text_area("请输入要转换的内容：", height=300)
        else:
            uploaded_file = st.file_uploader("上传文件 (.txt / .md)", type=['txt', 'md'])
            if uploaded_file:
                input_content = str(uploaded_file.read(), "utf-8")
                st.success(f"已上传文件: {uploaded_file.name}")

        # 自定义提示词
        st.subheader("🎯 自定义提示词 (可选)")
        use_custom_prompt = st.checkbox("使用自定义提示词")
        custom_prompt = None
        if use_custom_prompt:
            custom_prompt = st.text_area(
                "自定义提示词：",
                height=120,
                placeholder="使用 {input_content} 作为输入占位符"
            )

        st.markdown("---")
        st.subheader("⚙️ 输出设置")
        col1, col2 = st.columns(2)
        with col1:
            markdown_filename = st.text_input(
                "Markdown文件名",
                value=f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            )
        with col2:
            word_filename = st.text_input(
                "Word文件名",
                value=f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            )

        # 生成按钮
        st.markdown("---")
        generate_clicked = st.button("🚀 生成文档", type="primary", use_container_width=True)

        # ======== 文档生成逻辑 ========
        if generate_clicked:
            try:
                if not input_content.strip():
                    st.error("请输入内容")
                    st.stop()

                with st.spinner("正在生成文档..."):
                    generator = get_generator()
                    use_hq = st.checkbox("使用高保真导出(Pandoc)", value=True)
                    if use_hq:
                        md_content, md_path = generator.markdown_generator.generate_from_content(
                            input_content, custom_prompt, markdown_filename
                        )
                        conv = WordConverter()
                        word_path = conv.markdown_to_word_pandoc(md_content, word_filename)
                        result = {
                            'success': True,
                            'markdown_content': md_content,
                            'markdown_path': md_path,
                            'word_path': word_path,
                        }
                    else:
                        result = generator.generate_document(
                            input_content, custom_prompt, markdown_filename, word_filename
                        )

                if result['success']:
                    st.success("✅ 文档生成成功！")
                    st.info(f"📄 Markdown: {os.path.basename(result['markdown_path'])}")
                    st.info(f"📝 Word: {os.path.basename(result['word_path'])}")
                    st.markdown("### 👀 预览")
                    st.markdown(result['markdown_content'])
                    st.session_state.generated_files_new.append({
                        'timestamp': datetime.now(),
                        'markdown_path': result['markdown_path'],
                        'word_path': result['word_path'],
                        'content': result['markdown_content'][:200] + "..."
                    })
                else:
                    st.error(f"❌ 生成失败：{result.get('error', '未知错误')}")

            except Exception as e:
                st.exception(e)

        # ======== 历史与回滚 ========
        st.markdown("---")
        st.subheader("📜 历史与回滚（生成新文档）")
        if st.session_state.generated_files_new:
            for idx, file_info in enumerate(
                reversed(st.session_state.generated_files_new[-10:])
            ):
                with st.expander(f"版本 {idx+1} - {file_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.text(f"内容预览: {file_info['content']}")
                    st.text(f"Markdown: {file_info['markdown_path']}")
                    st.text(f"Word: {file_info['word_path']}")
                    if st.button("回滚到此版本", key=f"rollback_new_{idx}"):
                        with open(file_info['markdown_path'], 'r', encoding='utf-8') as f:
                            md = f.read()
                        st.session_state['edit_md_content'] = md
                        st.session_state['refresh_editor'] = True
                        st.success("✅ 已回滚到该版本，内容已载入编辑器")
                        st.rerun()

    # ----------------------
    # 🛠️ 修改文档
    # ----------------------
    with tab_edit:
        st.subheader("✏️ 编辑与修订")

        # 上传 Markdown 或 Word 文件
        md_file = st.file_uploader("上传 Markdown 文件", type=['md'], key="edit_md")
        docx_file = st.file_uploader("上传 Word 文件 (.docx)", type=['docx'], key="edit_docx")

        from word_converter import WordConverter as _WC
        conv = _WC()
        pandoc_available = conv.has_pandoc()

        skip_check = st.checkbox("已安装Pandoc，跳过检测", value=False)
        effective_pandoc = True if skip_check else pandoc_available
        extract_mode = st.radio(
            "提取方式",
            ["高保真(Pandoc)", "简化提取(内置)"],
            index=0 if effective_pandoc else 1,
            horizontal=True
        )

        # ======== 文件提取与载入 ========
        if md_file and st.button("载入 Markdown 文件"):
            existing_md = md_file.read().decode('utf-8')
            st.session_state["edit_md_content"] = existing_md
            st.session_state["refresh_editor"] = True
            st.success("已载入 Markdown 文件到编辑器")
            st.rerun()

        if docx_file and st.button("提取为 Markdown"):
            os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
            tmp_path = os.path.join(Config.OUTPUT_DIR, f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx")
            with open(tmp_path, 'wb') as f:
                f.write(docx_file.read())
            if extract_mode == "高保真(Pandoc)" and effective_pandoc:
                extracted_md = conv.word_to_markdown_pandoc(tmp_path)
            else:
                extracted_md = conv.word_to_markdown(tmp_path)
            st.session_state["edit_md_content"] = extracted_md
            st.session_state["refresh_editor"] = True
            st.success("已提取并载入到编辑器")
            st.rerun()

        # 同步编辑区刷新
        if st.session_state.get("refresh_editor", False):
            st.session_state["edit_md_text"] = st.session_state.get("edit_md_content", "")
            st.session_state["refresh_editor"] = False

        # 编辑器显示
        st.text_area(
            "Markdown 内容编辑区",
            value=st.session_state.get("edit_md_content", ""),
            key="edit_md_text",
            height=300
        )
        st.session_state["edit_md_content"] = st.session_state.get("edit_md_text", "")

        # ======== 插图与表格 ========
        st.markdown("---")
        st.subheader("🖼️ 插入图片 / 表格")

        img_col, tbl_col = st.columns(2)
        with img_col:
            img = st.file_uploader("上传图片以插入", type=["png", "jpg", "jpeg", "gif"], key="insert_img")
            img_width_in = st.number_input("图片宽度(英寸)", value=5.0, min_value=1.0, max_value=8.0, step=0.5)
            if img and st.button("保存并插入图片"):
                os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
                media_dir = os.path.join(Config.OUTPUT_DIR, 'media')
                os.makedirs(media_dir, exist_ok=True)
                save_path = os.path.join(media_dir, img.name)
                with open(save_path, 'wb') as f:
                    f.write(img.read())
                st.session_state["edit_md_content"] += f"\n\n![{os.path.splitext(img.name)[0]}](media/{img.name})\n"
                st.session_state["refresh_editor"] = True
                st.success("已插入图片")
                st.rerun()

        with tbl_col:
            rows = st.number_input("表格行数(含表头)", value=3, min_value=2)
            cols = st.number_input("表格列数", value=3, min_value=1)
            if st.button("插入空表格模板"):
                header = "| " + " | ".join([f"列{i+1}" for i in range(int(cols))]) + " |\n"
                sep = "| " + " | ".join(["---" for _ in range(int(cols))]) + " |\n"
                data = "".join(["| " + " | ".join([" " for _ in range(int(cols))]) + " |\n" for _ in range(int(rows)-1)])
                st.session_state["edit_md_content"] += "\n\n" + header + sep + data
                st.session_state["refresh_editor"] = True
                st.rerun()

        # ======== 修订与导出 ========
        st.markdown("---")
        st.subheader("🛠️ 修订与导出")
        instruction = st.text_area("修订指令：", placeholder="例如：优化措辞，增加‘风险评估’一节", height=100)
        if st.button("提交修订并生成新版本"):
            try:
                if not st.session_state["edit_md_text"].strip():
                    st.error("编辑器内容为空")
                    st.stop()
                client = LLMClient()
                revised_md = client.revise_markdown(st.session_state["edit_md_text"], instruction)
                generator = get_generator()
                md_path = generator.markdown_generator.save_markdown(
                    revised_md, f"revised_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                )
                word_path = generator.word_converter.markdown_to_word(revised_md, None)
                st.success("已生成修订版本")
                st.session_state["edit_md_content"] = revised_md
                st.session_state["refresh_editor"] = True
                st.session_state.generated_files_edit.append({
                    'timestamp': datetime.now(),
                    'markdown_path': md_path,
                    'word_path': word_path,
                    'content': revised_md[:200] + "..."
                })
                st.rerun()
            except Exception as e:
                st.error(f"修订失败：{e}")

        # ======== 历史与回滚 ========
        st.markdown("---")
        st.subheader("📜 历史与回滚（修改文档）")
        if st.session_state.generated_files_edit:
            for idx, file_info in enumerate(
                reversed(st.session_state.generated_files_edit[-10:])
            ):
                with st.expander(f"版本 {idx+1} - {file_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.text(f"内容预览: {file_info['content']}")
                    if st.button("回滚到此版本", key=f"rollback_edit_{idx}"):
                        with open(file_info['markdown_path'], 'r', encoding='utf-8') as f:
                            md = f.read()
                        st.session_state['edit_md_content'] = md
                        st.session_state['refresh_editor'] = True
                        st.success("✅ 已回滚到该版本")
                        st.rerun()


# ======================
# 入口调用
# ======================
if __name__ == "__main__":
    main()
