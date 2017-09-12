#!/usr/bin/env python3
# coding=utf-8

# !!! Falta fer shuffle d'alguns items, ara només ho fa dels choices


import sys, string, pprint, yaml, json, random, os, time

def error(title,reason):
    raise Exception('--- ERROR in question '+title+' --- '+reason)

# function to build Single Choice questions
def build_sc(output, title):
    #make sure choices are provided
    if not output.get("choices",False):
        error(title,'A list of Choices must be defined!')
    #make sure each choice has text
    correct = False
    for choice in output["choices"]:
        if not choice.get("text", False):
            error(title,'Text must be provided for every choice!')
        #check that at most one correct answer is provided
        if choice.get("correct", False):
            if correct:
                error(title,'Only one correct answer must be provided!')
            correct = True
    #check that at least one correct answer is provided
    if not correct:
        error(title,'A correct answer must be provided!')

    #shuffle the choices if needed
    if (output.get('shuffle', True)):
        random.shuffle(output['choices'])

    return output


# function to build Multiple Choice questions
def build_mc(output, title):
    #make sure choices are provided
    if not output.get("choices",False):
        error(title,'A list of Choices must be defined!')
    
    #make sure each choice has text
    correct = False
    for choice in output["choices"]:
        if not choice.get("text", False):
            error(title,'Text must be provided for every choice!')
        #check that at least one correct answer is provided
        if choice.get("correct", False):
            correct = True
    if not correct:
        error(title,'At least one correct answer must be provided!')

    #shuffle the choices if needed
    if (output.get('shuffle', True)):
        random.shuffle(output['choices'])

    return output


# function to build Ordering questions
def build_o(output, title):
    #check non empty label
    if output.get("label") == None:
        error(title,'A label for the choice list must be provided!')
    #check non empty items
    items = output.get("items", False)
    if not items:
        error(title,'A list of items must be provided!')
    return output

def check_writable_item(item, title):
    #check for mandatory fields
    if item.get("maxlength") == None:
        error(title,'Invalid item! Did you forget the list of options or maxlength?')
    if item.get("correct") == None:
        error(title,'All correct answers must be provided!')
    item.update({'ignorecase' : item.get("ignorecase", True), 'trim' : item.get("trim", True), 'placeholder' : item.get("placeholder", '?')})
    # ??? placeholder es opcional ??? TBD

def check_dropdown_item(item, title):
    if item.get("correct") == None:
        error(title,'All correct answers must be provided!')
    if item.get("options") == None:
        error(title,'A list of options must be provided!')
    #check that the correct option is available
    correct = False
    for option in item.get("options"):
        if option == item.get("correct"):
            correct = True
    # !!! potser podriem cambiar la manera de llegir opcions per no haver d'escriure la correcta a la llista tambe
    if not correct:
        error(title, "All correct answers must be in the options!")

# function to build FillIn questions
def build_fi(output, title):
    #check non empty context
    if not output.get("context", False):
        error(title,'A context must be provided!')
    #check non empty items
    if not output.get("items", False):
        error(title,'An item list must be provided!')
    for item in output["items"]:
        if not output["items"].get(item).get("options", False):
            check_writable_item(output["items"].get(item), title)
        else:
            check_dropdown_item(output["items"].get(item), title)
    return output


# function to build Matching questions
def build_m(output, title):
    #check for labels, left and right
    if not output.get("labels", False) or len(output["labels"]) != 2:
        error(title, "A list with two labels must be provided!")
    if not output.get("left", False) or not output.get("right", False):
        error(title, "Two lists (right and left) must be provided!")
    #make sure left and right have the same size
    if len(output.get("right")) != len(output.get("left")):
        error(title,"The right and left lists must have the same size")
    return output


# function to build Open Questions
def build_oq(output, title):
    #this is always good i guess
    return output

def build_q(fname, title):

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

    #make sure we have the mandatory attributes
    if output.get("text") == None:
        error(title, "Missing text!")
    if output.get("type") == None:
        error(title, "Missing type!")

    # fix fields according to type
    if output["type"] == "SingleChoice":
        return build_sc(output, title)
    elif output["type"] == "MultipleChoice":
        return build_mc(output, title)
    elif output["type"] == "Ordering":
        return build_o(output, title)
    elif output["type"] == "FillIn":
        return build_fi(output, title)
    elif output["type"] == "Matching":
        return build_m(output, title)
    elif output["type"] == "OpenQuestion":
        return build_oq(output, title)
    else:
       error(title, "Incorrect question type!")


def main():
    seed = int(sys.argv[1])
    quiz = yaml.load(open("quiz.yml"))

    random.seed(seed)

    if quiz.get('shuffle', True):
        random.shuffle(quiz['questions'])

    quiz['seed'] = seed
    quiz['time-generation'] = time.ctime()  # !!! posar format YYYY-MM-DD HH:MM:SS

    score_sum = 0
    for question in quiz['questions']:
        random.seed(seed)
        score_sum += question.get("score", 0)
        if not question.get("file", False) or not question.get("title", False):
            error("quiz","All questions need a file and a title!")
        question['q'] = build_q(question['file'], question['title'])
        question['a'] = {}
        question['points'] = 0
    if score_sum != 100:
        error("quiz", "Scores don't add to 100!!!")

    json.dump(quiz, sys.stdout, indent=4)

main()
