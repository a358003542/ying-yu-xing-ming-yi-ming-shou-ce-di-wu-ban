from pywander_text.process_text import MarkdownProcesser

from dataclasses import dataclass
import re


def remove_unwanted_symbol(s):
    """

    """
    new_s = re.sub(r"['-]", '', s)
    new_s = re.sub(r"è", 'e', new_s)
    new_s = re.sub(r"é", 'e', new_s)
    new_s = re.sub(r"ñ", 'n', new_s)
    new_s = re.sub(r"ü", 'u', new_s)
    new_s = re.sub(r"ä", 'a', new_s)
    new_s = re.sub(r"ö", 'o', new_s)
    return new_s


@dataclass
class WordEntry:
    """
    A'Court 这样的省音符号会干扰排序 将其移除
    Anne-Marie 连字符移除
    临时增补规则 Bandière 其中è更改为e
    临时增补规则 Duprée 其中é更改为e
    临时增补规则 Ibañez 其中ñ更改为n
    临时增补规则 Ibargüen 其中ü更改为u
    临时增补规则 Irenäus 其中ä更改为a
    临时增补规则 Möbius 其中ö更改为o
    """
    content: str
    map: tuple

    def __lt__(self, other):
        self_content = remove_unwanted_symbol(self.content).lower()
        other_content = remove_unwanted_symbol(other.content).lower()
        return self_content < other_content

    def __eq__(self, other):
        self_content = remove_unwanted_symbol(self.content).lower()
        other_content = remove_unwanted_symbol(other.content).lower()
        return self_content == other_content

    def __repr__(self):
        return f"<WordEntry: {self.content} in map: {self.map}>"


if __name__ == "__main__":
    with open("英语姓名译名手册（第五版）.md", "r", encoding="utf-8") as f:
        sample_md = f.read()

    p = MarkdownProcesser(sample_md)

    # 已经确认无误 自动跳过
    p.try_extract_table(skip=True)

    for table in p.table_blocks:
        english_name_col_data = table.get_tbody_col_data(col_index=1)

        english_col_data = [WordEntry(item.get('content'), item.get(
            'map')) for item in english_name_col_data]

        check_set = set()

        for col_data in english_col_data:
            content = col_data.content
            map = col_data.map


            # 空白行
            if not content:
                print('触发空白行检测')
                print(f'{table.get_target_lines(map)}')

                continue


            # 是否首字母大写
            if not content[0].isupper():
                print('触发首字母大写检测')
                print(f'{table.get_target_lines(map)}')

                continue


            # 是否重复
            if content in check_set:            
                print('触发重复检测')
                print(f'{table.get_target_lines(map)}')

                continue

            check_set.add(content)   

            


