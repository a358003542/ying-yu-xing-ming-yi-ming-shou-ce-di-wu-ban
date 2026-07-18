#!/usr/bin/env python3
"""
将指定格式的 JSON 文件转换为 Markdown 表格，支持输出到文件。
JSON 格式示例：
[
    {"text": "Aaberg 艾伯格", "head": "Aaberg", "page": 1},
    {"text": "Aabye 阿比",   "head": "Aabye",   "page": 1}
]
输出 Markdown 表格：
| 英文名 | 中文名 |
|--------|--------|
| Aaberg | 艾伯格 |
| Aabye  | 阿比   |

用法：
    python script.py input.json                  # 输出到 input.md
    python script.py input.json output.md        # 输出到指定文件
    python script.py input.json -                # 输出到控制台（UTF-8）
"""

import json
import sys
import re
import os

def extract_chinese_name(text: str, head: str) -> str:
    """从 text 中移除第一次出现的 head（英文名），返回剩余部分（中文名）。"""
    if not head:
        return text.strip()
    pattern = re.escape(head)
    match = re.search(pattern, text)
    if match:
        start, end = match.start(), match.end()
        result = text[:start] + text[end:]
        return result.strip()
    else:
        return text.strip()  # 未找到 head 时保留原文本

def convert_json_to_markdown(json_file_path: str) -> str:
    """读取 JSON 文件，返回 Markdown 表格字符串。"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON 根元素应为数组")

    rows = []
    for item in data:
        head = item.get('head', '').strip()
        text = item.get('text', '').strip()
        if not text:
            continue
        chinese_name = extract_chinese_name(text, head)
        rows.append((head, chinese_name))

    # 构建 Markdown 表格（转义竖线）
    table_lines = [
        "| 英文名 | 中文名 |",
        "|--------|--------|"
    ]
    for eng, chn in rows:
        eng_esc = eng.replace('|', '\\|')
        chn_esc = chn.replace('|', '\\|')
        table_lines.append(f"| {eng_esc} | {chn_esc} |")

    return "\n".join(table_lines)

def write_output(content: str, output_path: str):
    """将内容写入文件或控制台（统一 UTF-8 编码）。"""
    if output_path == '-':
        # 输出到控制台：强制使用 UTF-8
        sys.stdout.reconfigure(encoding='utf-8')  # Python 3.7+
        print(content)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content + '\n')

def main():
    # 解析命令行参数
    args = sys.argv[1:]
    if not args:
        print("用法: python script.py <input.json> [output.md|-]", file=sys.stderr)
        sys.exit(1)

    input_file = args[0]
    if len(args) >= 2:
        output_file = args[1]
    else:
        # 默认输出到与输入同名的 .md 文件
        base = os.path.splitext(input_file)[0]
        output_file = base + '.md'

    try:
        md_content = convert_json_to_markdown(input_file)
        write_output(md_content, output_file)
        if output_file != '-':
            print(f"已生成: {output_file}", file=sys.stderr)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()