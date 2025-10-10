import os
import logging
import markdown
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
from typing import Optional
import re
from config import Config

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WordConverter:
    """Markdown到Word转换器类"""
    
    def __init__(self):
        """初始化Word转换器"""
        self.output_dir = Config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def markdown_to_word(self, markdown_content: str, output_filename: Optional[str] = None) -> str:
        """
        将Markdown内容转换为Word文档
        
        Args:
            markdown_content: Markdown内容
            output_filename: 输出文件名
            
        Returns:
            生成的Word文件路径
        """
        try:
            logger.info("开始转换Markdown到Word...")
            
            # 创建新的Word文档
            doc = Document()
            
            # 解析Markdown内容（含图片、表格块）
            lines = [ln.rstrip('\r') for ln in markdown_content.split('\n')]
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    doc.add_paragraph()
                    i += 1
                    continue
                # 图片: ![alt](path "title") 或 ![alt](path)
                img_match = re.match(r'^!\[(.*?)\]\(([^\)\s]+)(?:\s+"(.*?)")?\)$', line)
                if img_match:
                    alt_text = img_match.group(1)
                    img_path = img_match.group(2)
                    self._add_image(doc, img_path, alt_text)
                    i += 1
                    continue
                # 表格块：header | line, 分隔线 |---|---|，随后多行数据
                if self._is_table_header(line) and i + 1 < len(lines) and self._is_table_separator(lines[i + 1].strip()):
                    i = self._add_table_block(doc, lines, i)
                    continue
                if line.startswith('# '):
                    heading = doc.add_heading(line[2:], level=1)
                    self._format_heading(heading)
                elif line.startswith('## '):
                    heading = doc.add_heading(line[3:], level=2)
                    self._format_heading(heading)
                elif line.startswith('### '):
                    heading = doc.add_heading(line[4:], level=3)
                    self._format_heading(heading)
                elif line.startswith('#### '):
                    heading = doc.add_heading(line[5:], level=4)
                    self._format_heading(heading)
                elif line.startswith('- ') or line.startswith('* '):
                    self._add_list_item(doc, line[2:], is_ordered=False)
                elif re.match(r'^\d+\. ', line):
                    self._add_list_item(doc, re.sub(r'^\d+\. ', '', line), is_ordered=True)
                elif line.startswith('> '):
                    self._add_quote(doc, line[2:])
                elif line.startswith('```'):
                    # 简化处理：跳过代码围栏行，代码正文以普通段落加入
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith('```'):
                        self._add_paragraph(doc, lines[i])
                        i += 1
                else:
                    self._add_paragraph(doc, line)
                i += 1
            
            # 生成输出文件名
            if not output_filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"converted_document_{timestamp}.docx"
            elif not output_filename.endswith('.docx'):
                output_filename += '.docx'
            
            # 保存Word文档
            output_path = os.path.join(self.output_dir, output_filename)
            doc.save(output_path)
            
            logger.info(f"Word文档已保存: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"转换Markdown到Word时出错: {str(e)}")
            raise Exception(f"转换Markdown到Word失败: {str(e)}")
    
    def _format_heading(self, heading):
        """格式化标题"""
        heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    def _add_list_item(self, doc, text, is_ordered=False):
        """添加列表项"""
        p = doc.add_paragraph()
        if is_ordered:
            p.style = 'List Number'
        else:
            p.style = 'List Bullet'
        p.add_run(text)
    
    def _add_quote(self, doc, text):
        """添加引用"""
        p = doc.add_paragraph()
        p.style = 'Quote'
        p.add_run(text)
    
    def _add_table_row(self, doc, line):
        """添加表格行"""
        # 简单的表格处理，实际应用中可能需要更复杂的逻辑
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if len(cells) > 1:
            table = doc.add_table(rows=1, cols=len(cells))
            table.style = 'Table Grid'
            for i, cell in enumerate(cells):
                table.cell(0, i).text = cell

    def _is_table_header(self, line: str) -> bool:
        return line.startswith('|') and '|' in line[1:]

    def _is_table_separator(self, line: str) -> bool:
        if not (line.startswith('|') and '|' in line[1:]):
            return False
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if not parts:
            return False
        return all(re.match(r'^:?-{3,}:?$', p) for p in parts)

    def _add_table_block(self, doc, lines, start_idx: int) -> int:
        """从表头开始创建完整表格，返回消耗后的下一行索引"""
        header_line = lines[start_idx].strip()
        sep_idx = start_idx + 1
        headers = [c.strip() for c in header_line.split('|')[1:-1]]
        # 收集数据行
        data_rows = []
        i = sep_idx + 1
        while i < len(lines):
            row = lines[i].strip()
            if not row.startswith('|') or '|' not in row[1:]:
                break
            cells = [c.strip() for c in row.split('|')[1:-1]]
            if len(cells) != len(headers):
                break
            data_rows.append(cells)
            i += 1
        # 创建表格（1 header row + n data rows）
        cols = max(1, len(headers))
        rows = 1 + len(data_rows)
        table = doc.add_table(rows=rows, cols=cols)
        table.style = 'Table Grid'
        # header
        for c_idx, h in enumerate(headers):
            table.cell(0, c_idx).text = h
        # data
        for r_idx, row_cells in enumerate(data_rows, start=1):
            for c_idx, cell in enumerate(row_cells):
                table.cell(r_idx, c_idx).text = cell
        return i

    def _add_image(self, doc, image_path: str, alt_text: str = ""):
        """插入图片，若找不到路径则作为普通段落插入路径文本"""
        try:
            # 支持相对路径（相对于输出目录）
            candidate_paths = [
                image_path,
                os.path.join(self.output_dir, image_path),
            ]
            actual = None
            for p in candidate_paths:
                if os.path.isfile(p):
                    actual = p
                    break
            if actual is None:
                self._add_paragraph(doc, f"[图片未找到] {image_path}")
                return
            # 默认宽度 5 英寸，可扩展解析 title 指定尺寸
            doc.add_picture(actual, width=Inches(5))
            if alt_text:
                p = doc.add_paragraph(alt_text)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as e:
            logger.error(f"插入图片失败: {str(e)}")
            self._add_paragraph(doc, f"[图片插入失败] {image_path}")
    
    def _add_paragraph(self, doc, text):
        """添加段落"""
        # 处理粗体和斜体
        text = self._format_text(text)
        p = doc.add_paragraph()
        
        # 简单的文本格式化
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                run = p.add_run(part[2:-2])
                run.bold = True
            elif part.startswith('*') and part.endswith('*'):
                run = p.add_run(part[1:-1])
                run.italic = True
            elif part.startswith('`') and part.endswith('`'):
                run = p.add_run(part[1:-1])
                run.font.name = 'Courier New'
            else:
                p.add_run(part)
    
    def _format_text(self, text):
        """格式化文本"""
        # 这里可以添加更多的文本格式化逻辑
        return text
    
    def convert_file(self, markdown_file_path: str, output_filename: Optional[str] = None) -> str:
        """
        转换Markdown文件到Word文档
        
        Args:
            markdown_file_path: Markdown文件路径
            output_filename: 输出文件名
            
        Returns:
            生成的Word文件路径
        """
        try:
            # 读取Markdown文件
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # 转换到Word
            return self.markdown_to_word(markdown_content, output_filename)
            
        except Exception as e:
            logger.error(f"转换Markdown文件时出错: {str(e)}")
            raise Exception(f"转换Markdown文件失败: {str(e)}")
