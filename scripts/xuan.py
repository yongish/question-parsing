import argparse
import json
import pinyin_jyutping
import pprint

def getJson(raw_passage):
    raw_paragraphs = raw_passage.replace(' ','').split('\n')

    question_index = 0
    question_flag = False

    curr_option = 1
    options = []

    num_questions = 0

    p = pinyin_jyutping.PinyinJyutping()
    passage = []
    for raw_paragraph in raw_paragraphs:
        all_solutions = p.pinyin_all_solutions(raw_paragraph)
        # Assume every line starts with a tab.
        paragraph_list = [{'characters': '\u2003'}]
        for (hanzi, solutions) in zip(all_solutions['word_list'], all_solutions['solutions']):
            if hanzi == '（' or hanzi == '(':
                question = {'questionIndex': question_index, 'options': []}
                question_flag = True
                num_questions += 1
                continue

            if hanzi == '）' or hanzi == ')':
                question['options'].append(options)
                options = []
                curr_option = 1

                question_index += 1
                question_flag = False
                paragraph_list.append(question)
                continue

            if hanzi in ['c1', 'c2', 'c3', 'c4']:
                correct_index = int(hanzi[1]) - 1
                question['correctIndex'] = correct_index

            solution0 = solutions[0]

            if hanzi in ['2', '3', '4', 'c2', 'c3', 'c4']:
                if hanzi != curr_option:    # Finished processing the option.
                    question['options'].append(options)
                    options = []
                    curr_option += 1
                continue
            if hanzi in ['c1', '1']:
                continue

            # BUG. Need to handle the case with multiple characters.
            if hanzi == solution0:
                word = {'characters': hanzi}
            else:
                word = {'characters': hanzi, 'pinyin': solutions[0]}

            if question_flag:
                options.append(word)
            else:
                paragraph_list.append(word)
            
        passage.append(paragraph_list)

    pp = pprint.PrettyPrinter()
    pp.pprint(passage)
    output = {'numQuestions': int(num_questions), 'passage': passage}
    return json.dumps(output, ensure_ascii=False, indent=2)

def process(filename):
    f = open(filename, 'r')
    raw_passage = f.read()
    
    output = getJson(raw_passage)

    with open('data.json', 'w') as f:
        f.write(output)


# parser = argparse.ArgumentParser()
# parser.add_argument('filename')
# args = parser.parse_args()
# process(args.filename)

parser = argparse.ArgumentParser()
parser.add_argument('raw_passage')
args = parser.parse_args()
print(getJson(args.raw_passage))
