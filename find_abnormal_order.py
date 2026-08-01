from pywander_text.process_text import MarkdownProcesser
from pywander.list import NearlyOrderedList

from dataclasses import dataclass
import re


def remove_unwanted_symbol(s):
    """

    """
    new_s = re.sub(r"['-]", '', s)
    return new_s


@dataclass
class WordEntry:
    """
    A'Court 这样的省音符号会干扰排序 将其移除
    Anne-Marie 连字符移除
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

        my_list = NearlyOrderedList(english_col_data)
        abnormal_data, template_data = my_list.find_anomaly_intervals(min_size=7)

        count = 0
        while abnormal_data:
            queue_item = abnormal_data.pop(0)
            related_template_data = template_data.pop(0)

            for index,item in enumerate(queue_item):
                warning_item_map_data = item.map

                print(f'{table.get_target_lines(warning_item_map_data)}   vs     {related_template_data[index]}')

            print(f'----下一个异常区段---')
            count += 1

            if count > 50:
                print("Still have more abnormal data, but stop here to avoid too many outputs.")
                break

        else:
            print("No abnormal data found in this table.")

