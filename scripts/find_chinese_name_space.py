import re

def find_names_with_spaces(md_file_path):
    """
    从 Markdown 文件中读取表格，找出中文名（第三列）中间包含空格的记录，
    并打印对应的整行原文。
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"正在检查文件: {md_file_path}")
    found = False

    for line_no, line in enumerate(lines, start=1):
        raw_line = line.rstrip('\n')
        # 跳过空行
        if not raw_line.strip():
            continue
        # 判断是否为表格行：以 | 开头且包含至少两个 |
        if raw_line.startswith('|') and raw_line.count('|') >= 2:
            # 跳过表头分隔行（例如 |---|---|）
            if re.match(r'^\|[\s\-:]+\|', raw_line):
                continue
            # 按 | 分割，取第一个单元格（英文名）
            cells = [cell.strip() for cell in raw_line.split('|')]
            # 第一个有效单元格是索引1（因为split后第一个元素是空字符串）
            if len(cells) >= 2:
                chinese_name = cells[2].strip()
                # 检查中文名中间是否有空格（排除首尾空格）
                # 如果有中文分号 是有男女名的情况
                if '；' in chinese_name:
                    # 分割后检查每个名字是否有空格
                    names = chinese_name.split('；')
                    for name in names:
                        if ' ' in name.strip():
                            print(f"[行 {line_no}] 发现空格: {raw_line}")
                            found = True

                else:
                    if ' ' in chinese_name:
                        print(f"[行 {line_no}] 发现空格: {raw_line}")
                        found = True

    if not found:
        print("未找到中文名中间包含空格的记录。")

if __name__ == "__main__":
    find_names_with_spaces("英语姓名译名手册（第五版）.md")