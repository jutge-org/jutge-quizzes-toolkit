#!/usr/bin/env python3
# coding=utf-8

# !!! Falta fer shuffle d'alguns items, ara només ho fa dels choices


import sys, string, pprint, yaml, json, random, os, time

def build_q(fname):

    py_name = fname + ".py"
    yml_name = fname + ".yml"

    # read the python code
    if os.path.exists(py_name):
        code = open(py_name).read()
    else:
        code = ""

    # read the question description
    q = open(yml_name).read()

    # execute the code, using new global and local dictionaries
    ldict = {}
    exec(code, globals(), ldict)

    # modify the question description with the local dictionary
    subs = string.Template(q).substitute(ldict)

    # get the text back to data
    output = yaml.load(subs)

    # fix fields according to type
    if output["type"] in ["SingleChoice", "MultipleChoice"]:
        # shuffle choices if needed
        if 'choices' in output and output.get('shuffle', True):
            random.shuffle(output['choices'])
    elif output["type"] == "FillIn":
        # shuffle options for all items
        for item in output["items"].values():
            if 'options' in item and item.get('shuffle', True):
                random.shuffle(item['options'])
    elif output["type"] == "Ordering":
        # shuffle items if needed
        if 'items' in output and output.get('shuffle', True):
            random.shuffle(output['items'])
    elif output["type"] == "Matching":
        if 'left' in output and output.get('shuffle', True):
            random.shuffle(output['left'])
        if 'right' in output and output.get('shuffle', True):
            random.shuffle(output['right'])
    # return the output
    return output


def main():
    seed = int(sys.argv[1])
    quiz = yaml.load(open("quiz.yml"))

    random.seed(seed)

    if quiz.get('shuffle', True):
        random.shuffle(quiz['questions'])

    quiz['seed'] = seed
    quiz['time-generation'] = time.ctime()  # !!! posar format YYYY-MM-DD HH:MM:SS

    for question in quiz['questions']:
        random.seed(seed)
        question['q'] = build_q(question['file'])
        question['a'] = {}
        question['points'] = 0

    json.dump(quiz, sys.stdout, indent=4)

main()
