import argparse
import pinyin_jyutping
# import json
# import pprint

def getJson(raw_passage):
    raw_paragraphs = raw_passage.replace(' ','').split('\n')
    
    print('raw', raw_paragraphs)
    
    p = pinyin_jyutping.PinyinJyutping()
    choices = []
    it = iter(raw_paragraphs)
    while (raw_paragraph := next(it)) and raw_paragraph != '\n':
        all_solutions = p.pinyin_all_solutions(raw_paragraph)
        choice = {"words": []}
        for (hanzi, solutions) in zip(all_solutions['word_list'], all_solutions['solutions']):
            choice['words'].append({'hanzi': hanzi, 'pinyin': solutions[0]})
        choices.append(choice)

    passage = []
    question_index = 0
    while (raw_paragraph := next(it, None)) is not None:
        all_solutions = p.pinyin_all_solutions(raw_paragraph)
        # Assume every line starts with a tab.
        paragraph_list = [{'characters': '\u2003'}]
        for (hanzi, solutions) in zip(all_solutions['word_list'], all_solutions['solutions']):
            solution0 = solutions[0]
            if hanzi[0] == 'a':
                word = {'questionIndex': question_index, 'correctIndex': int(hanzi[1:])}
                question_index += 1
            elif hanzi == solution0 or hanzi.isdigit():
                word = {'characters': hanzi}
            else:
                word = {'characters': hanzi, 'pinyin': solution0}

            paragraph_list.append(word)
        passage.append(paragraph_list)

    # pp = pprint.PrettyPrinter()
    # pp.pprint(passage)
    output = {'numQuestions': question_index, 'choices': choices, 'passage': passage}
    return str(output)

parser = argparse.ArgumentParser()
parser.add_argument('raw_passage')
args = parser.parse_args()
print(getJson(args.raw_passage))

# def process(filename):
#     f = open(filename, 'r')
#     raw_passage = f.read()
#     output = getJson(raw_passage)
#     with open('data.json', 'w') as f:
#         json.dump(output, f, ensure_ascii=False, indent=2)

# parser = argparse.ArgumentParser()
# parser.add_argument('filename')
# args = parser.parse_args()
# process(args.filename)
