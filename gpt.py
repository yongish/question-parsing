import re
import json

# Input text
input_text = """
“铃…“一阵闱钟的铃声把我从睡梦中(1提醒c2叫醒3清醒4觉醒)。我打开窗户一着(c1东方2西方3南方4北方已经透出红光。在空气(1清寒2清淡3清秀c4清新)的早晨，我爱到屋外散步，这几乎已成了我每天早晨的(1习俗2习性c3习惯4习尚)。
我在路上走着,这时两旁的商店,还(1紧紧地2匆匆地3慢慢地c4轻轻地)闭着大门。在这幺一个寂静的世界里，我仿佛是在无人的地方漫步，十分写意。
一会儿，远:处传来汽车声，还有行人的脚步声。当我踏上(1路途c2归途3前途4旅途)时，太阳已经露出半个 脸来。街旁的店铺也（1早早c2纷纷3偏偏4呼呼）打开大门。随着三三两两的行人和来来往往的车辆，整个地方又(1恢复2重复3反复c4收复)了热闹的景象。
"""

# Regular expression patterns to extract text and options
pattern_passage = r'“(.+?)”'  # Matches the passage
pattern_questions = r'\((.+?)\)'  # Matches the options within parentheses

# Extracting passage and questions
# passage = re.findall(pattern_passage, input_text, re.DOTALL)[0]
passage = re.findall(pattern_passage, input_text, re.DOTALL)
questions = re.findall(pattern_questions, input_text, re.DOTALL)

# Mapping question indices to Chinese characters
index_mapping = {
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    'c': 'c'
}

# Function to extract question options and correct index
def extract_question_data(question_text):
    options = []
    correct_index = None
    for match in re.finditer(r'(\d+)(\S+)', question_text):
        index = match.group(1)
        text = match.group(2)
        if index == 'c':
            correct_index = index_mapping[index]
        else:
            options.append({
                "characters": text,
                "pinyin": None  # You can include Pinyin here if available
            })
    return options, correct_index

# Constructing JSON structure
json_output = {
    "numQuestions": len(questions),
    "passage": []
}

for i, question in enumerate(questions):
    options, correct_index = extract_question_data(question)
    question_data = [{
        "characters": char,
        "pinyin": None  # You can include Pinyin here if available
    } for char in passage]
    
    if correct_index is not None:
        question_data.append({
            "questionIndex": i,
            "options": options,
            "correctIndex": correct_index
        })

    json_output["passage"].append(question_data)

# Output JSON
print(json.dumps(json_output, indent=2, ensure_ascii=False))
