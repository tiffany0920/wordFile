#!/usr/bin/env python3
"""
智能文档生成器 Web 界面 - 基于Streamlit的现代化文档处理平台
📘 核心功能：
  - 智能文档生成：通过通义千问LLM将输入内容转换为结构化Markdown和Word文档
  - 文档编辑修改：支持上传现有文档进行AI辅助编辑和修订
  - 多格式支持：支持Markdown和Word文档的双向转换
  - 媒体资源处理：自动处理图片插入和路径管理
  - 模板系统：提供多种文档生成模板（技术文档、报告、会议纪要等）
  - 历史版本管理：独立的生成和编辑历史记录，支持版本回滚
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
    """初始化智能文档生成器Web界面的会话状态变量"""
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
    if 'markdown_filename' not in st.session_state:
        st.session_state.markdown_filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if 'word_filename' not in st.session_state:
        st.session_state.word_filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


@st.cache_resource
def get_generator():
    """获取智能文档生成器实例（缓存优化）"""
    try:
        return DocumentGenerator()
    except Exception as e:
        st.error(f"初始化失败: {str(e)}")
        return None


# ======================
# 文档生成器类定义
# ======================
class DocumentGenerator:
    """智能文档生成器Web界面专用类，整合文档生成和转换功能"""

    def __init__(self):
        self.markdown_generator = MarkdownGenerator()
        self.word_converter = WordConverter()
        self.llm_client = LLMClient()

    def generate_document(self, input_content: str, custom_prompt: str = None,
                         markdown_filename: str = None, word_filename: str = None):
        """
        智能文档生成器Web界面核心功能：生成Markdown和Word文档
        """
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
    """智能文档生成器Web界面主函数"""
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

        # 模板选择
        st.subheader("📋 模板选择")
        template_mode = st.radio(
            "选择模板类型",
            ["使用预设模板", "自定义提示词"],
            horizontal=True
        )

        custom_prompt = None
        if template_mode == "使用预设模板":
            templates = {
                "默认模板": {
                    "description": "使用默认的通用模板，适合一般文档转换",
                    "prompt": Config.DEFAULT_PROMPT_TEMPLATE
                },
                "技术文档": {
                    "description": "适合技术文档的模板，包含技术规范和结构化内容",
                    "prompt": """
请将以下内容转换为技术文档格式的Markdown：

输入内容：{input_content}

要求：
1. 使用清晰的技术文档结构
2. 包含目录、概述、详细说明等部分
3. 使用代码块、表格等格式
4. 确保技术术语准确
"""
                },
                "报告格式": {
                    "description": "适合正式报告的模板，包含规范的报告结构",
                    "prompt": """
请将以下内容转换为正式报告格式的Markdown：

输入内容：{input_content}

要求：
1. 使用正式的报告结构
2. 包含摘要、正文、结论等部分
3. 使用适当的标题层级
4. 确保内容逻辑清晰
"""
                },
                "会议纪要": {
                    "description": "适合会议纪要的模板，包含会议要素和时间线",
                    "prompt": """
请将以下内容转换为会议纪要格式的Markdown：

输入内容：{input_content}

要求：
1. 使用会议纪要的标准格式
2. 包含会议信息、参会人员、议题、决议等
3. 使用列表和表格整理信息
4. 确保时间线清晰
"""
                }
            }

            selected_template = st.selectbox("选择预设模板", list(templates.keys()))
            st.info(templates[selected_template]["description"])
            custom_prompt = templates[selected_template]["prompt"]

        else:
            custom_prompt = st.text_area(
                "自定义提示词：",
                height=300,
                placeholder="使用 {input_content} 作为输入占位符\n\n示例：\n请将以下内容转换为规范的Markdown文档：\n\n输入内容：{input_content}\n\n要求：\n1. 结构清晰\n2. 格式规范\n3. 内容完整"
            )

        st.markdown("---")
        st.subheader("⚙️ 输出设置")

        # 初始化文件名在session state中
        if 'markdown_filename' not in st.session_state:
            st.session_state.markdown_filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if 'word_filename' not in st.session_state:
            st.session_state.word_filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        col1, col2 = st.columns(2)
        with col1:
            markdown_filename = st.text_input(
                "Markdown文件名（不含扩展名）",
                key="markdown_filename"
            )
        with col2:
            word_filename = st.text_input(
                "Word文件名（不含扩展名）",
                key="word_filename"
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

                    # 生成Markdown内容
                    md_content, md_path = generator.markdown_generator.generate_from_content(
                        input_content, custom_prompt, markdown_filename
                    )

                    # 根据用户选择生成Word文档（只生成一个）
                    if use_hq:
                        conv = WordConverter()
                        word_path = conv.markdown_to_word_pandoc(md_content, word_filename)
                    else:
                        word_path = generator.word_converter.markdown_to_word(md_content, word_filename)

                    result = {
                        'success': True,
                        'markdown_content': md_content,
                        'markdown_path': md_path,
                        'word_path': word_path,
                    }

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
            try:
                # 直接从上传的文件对象读取字节数据，无需保存临时文件
                docx_bytes = docx_file.read()

                if extract_mode == "高保真(Pandoc)" and effective_pandoc:
                    extracted_md = conv.word_to_markdown_pandoc_from_bytes(docx_bytes)
                else:
                    extracted_md = conv.word_to_markdown_from_bytes(docx_bytes)

                st.session_state["edit_md_content"] = extracted_md
                st.session_state["refresh_editor"] = True
                st.success("已提取并载入到编辑器")
                st.rerun()
            except Exception as e:
                st.error(f"文档提取失败: {str(e)}")

        # 同步编辑区刷新
        if st.session_state.get("refresh_editor", False):
            st.session_state["edit_md_text"] = st.session_state.get("edit_md_content", "")
            st.session_state["refresh_editor"] = False

        # 编辑器显示
        if "edit_md_text" not in st.session_state:
            st.session_state["edit_md_text"] = st.session_state.get("edit_md_content", "")

        st.text_area(
            "Markdown 内容编辑区",
            key="edit_md_text",
            height=300
        )

        # 实时同步编辑器内容
        current_editor_content = st.session_state.get("edit_md_text", "")
        if current_editor_content != st.session_state.get("edit_md_content", ""):
            st.session_state["edit_md_content"] = current_editor_content

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

                # 确保文件名是唯一的，避免覆盖
                counter = 1
                original_name = img.name
                while os.path.exists(save_path):
                    name, ext = os.path.splitext(original_name)
                    save_path = os.path.join(media_dir, f"{name}_{counter}{ext}")
                    counter += 1

                with open(save_path, 'wb') as f:
                    f.write(img.read())

                # 生成正确的相对路径（始终使用 media/filename 格式）
                filename = os.path.basename(save_path)
                relative_path = f"media/{filename}"

                st.session_state["edit_md_content"] += f"\n\n![{os.path.splitext(filename)[0]}]({relative_path})\n"
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

        # 添加导出选项
        export_mode = st.radio(
            "导出方式",
            ["AI修订后导出", "直接导出当前内容"],
            horizontal=True
        )

        if export_mode == "AI修订后导出":
            instruction = st.text_area("修订指令：", placeholder="例如：优化措辞，增加'风险评估'一节", height=100)
            submit_button = st.button("🤖 提交修订并生成新版本", type="primary")
        else:
            instruction = ""
            submit_button = st.button("💾 直接导出当前内容", type="primary")

        if submit_button:
            try:
                if not st.session_state["edit_md_text"].strip():
                    st.error("编辑器内容为空")
                    st.stop()

                # 显示当前内容用于调试
                logger.info("当前编辑器内容:")
                logger.info(st.session_state["edit_md_text"])

                # 复制媒体文件以确保修订版本中的图片可用
                _ensure_media_files_available(st.session_state["edit_md_text"])

                if export_mode == "AI修订后导出":
                    # AI修订模式
                    client = LLMClient()
                    revised_md = client.revise_markdown(st.session_state["edit_md_text"], instruction)

                    # 显示修订后的内容用于调试
                    logger.info("修订后的内容:")
                    logger.info(revised_md)

                    # 再次复制媒体文件，因为修订后的内容可能包含新的图片
                    _ensure_media_files_available(revised_md)
                else:
                    # 直接导出模式
                    revised_md = st.session_state["edit_md_text"]
                    logger.info("直接导出当前内容，无需AI修订")

                # 显示输出目录结构
                _debug_directory_structure()

                generator = get_generator()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                md_path = generator.markdown_generator.save_markdown(
                    revised_md, f"revised_{timestamp}.md"
                )
                word_path = generator.word_converter.markdown_to_word(revised_md, f"revised_{timestamp}.docx")

                if export_mode == "AI修订后导出":
                    st.success("✅ 已生成修订版本")
                else:
                    st.success("✅ 已直接导出当前内容")

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
                st.error(f"导出失败：{e}")

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


def _ensure_media_files_available(markdown_content: str):
    """
    智能文档生成器媒体资源管理功能：
    确保Markdown中引用的媒体文件在输出目录的media文件夹中可用
    这个函数专门处理文档修订过程中的图片引用和资源同步问题
    """
    try:
        import re
        import os
        import shutil

        logger.info("开始检查媒体文件可用性...")

        # 提取所有图片路径
        img_pattern = re.compile(r'!\[(?:[^\]]*)\]\(([^)]+)\)')
        matches = img_pattern.findall(markdown_content)

        logger.info(f"找到 {len(matches)} 个图片引用: {matches}")

        media_dir = os.path.join(Config.OUTPUT_DIR, 'media')
        os.makedirs(media_dir, exist_ok=True)
        logger.info(f"媒体目录: {media_dir}")

        for img_path in matches:
            logger.info(f"处理图片引用: {img_path}")

            # 跳过URL
            if img_path.startswith('http://') or img_path.startswith('https://'):
                logger.info(f"跳过URL图片: {img_path}")
                continue

            # 如果是相对路径，尝试复制文件到media目录
            if not os.path.isabs(img_path):
                source_path = None
                target_filename = None

                # 检查是否已经在media目录中
                if img_path.startswith('media/'):
                    source_path = os.path.join(Config.OUTPUT_DIR, img_path)
                    target_filename = os.path.basename(img_path)
                    logger.info(f"检查media格式路径: {source_path}")
                else:
                    # 检查是否在输出目录根目录
                    source_path = os.path.join(Config.OUTPUT_DIR, img_path)
                    target_filename = os.path.basename(img_path)
                    logger.info(f"检查根目录路径: {source_path}")

                # 检查是否在嵌套的media/media目录中
                if source_path and not os.path.isfile(source_path):
                    nested_media_path = os.path.join(Config.OUTPUT_DIR, 'media', img_path)
                    if os.path.isfile(nested_media_path):
                        source_path = nested_media_path
                        logger.info(f"找到嵌套media目录中的文件: {source_path}")

                if source_path and os.path.isfile(source_path):
                    # 确保文件在media目录中（不是嵌套的）
                    target_path = os.path.join(media_dir, target_filename)

                    logger.info(f"源文件存在: {source_path}")

                    if not os.path.isfile(target_path):
                        shutil.copy2(source_path, target_path)
                        logger.info(f"复制媒体文件: {source_path} -> {target_path}")
                    else:
                        logger.info(f"媒体文件已存在: {target_path}")
                else:
                    logger.warning(f"找不到源文件: {source_path}")

    except Exception as e:
        logger.warning(f"确保媒体文件可用时出错: {e}")


def _debug_directory_structure():
    """智能文档生成器调试功能：输出和分析目录结构"""
    try:
        import os
        logger.info("=== 目录结构调试 ===")
        logger.info(f"输出目录: {Config.OUTPUT_DIR}")

        if os.path.exists(Config.OUTPUT_DIR):
            logger.info("输出目录存在")
            for root, dirs, files in os.walk(Config.OUTPUT_DIR):
                level = root.replace(Config.OUTPUT_DIR, '').count(os.sep)
                indent = ' ' * 2 * level
                logger.info(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    file_path = os.path.join(root, file)
                    logger.info(f"{subindent}{file} (存在: {os.path.isfile(file_path)})")
        else:
            logger.warning("输出目录不存在")

        logger.info("=== 目录结构调试结束 ===")
    except Exception as e:
        logger.warning(f"调试目录结构时出错: {e}")


# ======================
# 入口调用
# ======================
if __name__ == "__main__":
    main()
