from pywander_text.process_text import MarkdownProcesser


def has_space(text):
    if ' ' in text:
        return True
    else:
        return False

def has_space_in_chinese(text):
    """
    额外的格式 瓦利； 瓦莉（女名） 这是容忍的
    """
    if '；' in text:
        names = text.split('；')
        for name in names:
            if ' ' in name.strip():
                return True
    else:
        if ' ' in text:
            return True

    return False




if __name__ == "__main__":
    with open("英语姓名译名手册（第五版）.md", "r", encoding="utf-8") as f:
        sample_md = f.read()

    p = MarkdownProcesser(sample_md)

    p.try_extract_table()

    for table in p.table_blocks:
        table.check_tbody_data_iter_col(col_index=1, check_func = has_space)

        table.check_tbody_data_iter_col(col_index=2, check_func = has_space_in_chinese)
