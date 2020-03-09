#!/usr/bin/env python3
# coding=utf-8

# !!! Falta fer shuffle d'alguns items, ara només ho fa dels choices


import sys, string, pprint, yaml, json, random, os, time

def error(title,reason):
    raise Exception('--- ERROR in question '+str(title)+' --- '+str(reason))

# function to build Single Choice questions
def build_sc(output, title):
    #make sure choices are provided
    if not output.get("choices",False):
        error(title,'A list of Choices must be defined!')
    #make sure each choice has text
    correct = False
    false_answers = []
    for choice in output["choices"]:
        text = choice.get("text", False)
        if not text:
            error(title,'Text must be provided for every choice!')

        #check types
        check_not_dict_list(text, title, "Text", "basic type")
        check_not_dict_list(choice.get("hint"), title, "Hint", "basic type")
        #check that at most one correct answer is provided
        if choice.get("correct", False):
            if correct:
                error(title,'Only one correct answer must be provided!')
            correct = True
            correct_text = choice.get("text")
        else:
            false_answers.append(text)
    #check that at least one correct answer is provided
    if not correct:
        error(title,'A correct answer must be provided!')
    #check that correct answer is not repeated
    if correct_text in false_answers:
        error(title, 'Only one correct answer with the same text must be provided!')
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
        text = choice.get("text", False)
        if not text:
            error(title,'Text must be provided for every choice!')
        check_not_dict_list(text, title, "Text", "basic type")
        check_not_dict_list(choice.get("hint"), title, "Hint", "basic type")

    
    #shuffle the choices if needed
    if (output.get('shuffle', True)):
        random.shuffle(output['choices'])

    return output


# function to build Ordering questions
def build_o(output, title):
    #check non empty label
    label = output.get("label")
    if label == None:
        error(title,'A label for the choice list must be provided!')
    check_not_dict_list(label, title, "label", "text")
    #check non empty items
    items = output.get("items", False)
    if not items:
        error(title,'A list of items must be provided!')
    check_list(items, title, "items")
    for item in items:
        check_not_dict_list(item, title, "Items", "text")
    output["items_rand"] = list(items)
    random.shuffle(output["items_rand"])
    return output

# function to build FillIn questions
def build_fi(output, title):
    #check non empty context
    context = output.get("context", False)
    if not context:
        error(title,'A context must be provided!')
    check_not_dict_list(context, title, "Context", "text")
    #check non empty items
    if not output.get("items", False):
        error(title,'An item list must be provided!')
    for name, item in output["items"].items():
        if not name in context:
            error(title, "Item "+ str(name) +" is not in the context!")
        if not item.get("options", False):
            check_writable_item(item, title)
        else:
            check_dropdown_item(item, title)
    return output

def check_writable_item(item, title):
    #check for mandatory fields
    maxlength = item.get("maxlength") 
    if maxlength == None:
        error(title,'Invalid item! Did you forget the list of options or maxlength?')
    if not isinstance(maxlength, int):
        error(title, "Maxlength must be an integer!")

    correct = item.get("correct")
    if correct == None:
        error(title,'All correct answers must be provided!')
    check_not_dict_list(correct, title, "Correct", "basic type")

    item.update({'ignorecase' : item.get("ignorecase", True), 'trim' : item.get("trim", True), 'placeholder' : item.get("placeholder", '?')})
    # ??? placeholder es opcional ??? TBD

    check_not_dict_list(item.get("ignorecase"), title, "ignorecase", "true or false")
    check_not_dict_list(item.get("trim"), title, "trim", "true or false")
    check_not_dict_list(item.get("placeholder"), title, "placeholder", "a text")

def check_dropdown_item(item, title):
    correct = item.get("correct")
    if correct == None:
        error(title,'All correct answers must be provided!')
    check_not_dict_list(correct, title, "Correct", "basic type")

    options = item.get("options")
    if options == None:
        error(title,'A list of options must be provided!')
    check_list(options, title, "options")
    #check that the correct option is available
    correct = False
    false_answers = []
    for option in options:
        if option == item.get("correct"):
            correct = True
        check_not_dict_list(option, title, "All options", "basic type")
    # !!! potser podriem cambiar la manera de llegir opcions per no haver d'escriure la correcta a la llista tambe
    if not correct:
        error(title, "The correct answer must be in the options!")


# function to build Matching questions
def build_m(output, title):
    #check for labels, left and 
    labels = output.get("labels", False)
    check_list(labels, title, "labels")
    if not labels or len(labels) != 2:
        error(title, "A list with two labels must be provided!")
    left = output.get("left", False)
    right = output.get("right", False)
    if not left or not right:
        error(title, "Two lists (right and left) must be provided!")
    check_list(left, title, "left")
    check_list(right, title, "right")
    #make sure left and right have the same size
    if len(right) != len(left):
        error(title,"The right and left lists must have the same size")
    for item in left:
        check_not_dict_list(item, title, "left list's items", "basic type")
    for item in right:
        check_not_dict_list(item, title, "right list's items", "basic type")
    output["right_rand"] = list(right)
    output["left_rand"] = list(left)
    random.shuffle(output["right_rand"])
    random.shuffle(output["left_rand"])

    return output


# function to build Open Questions
def build_oq(output, title):
    #this is always good i guess
    return output

def build_q(fname, title):

    py_name = str(fname) + ".py"
    yml_name = str(fname) + ".yml"

    # read the python code
    if os.path.exists(py_name):
        code = open(py_name).read()
    else:
        code = ""

    # read the question description
    q = open(yml_name).read()

    # execute the code, using new global and local dictionaries
    def all_different(*x):
        return len(x) == len(set(x))
    ldict = {'all_different': all_different}
    exec(code, globals(), ldict)

    # modify the question description with the local dictionary
    subs = string.Template(q).substitute(ldict)

    # get the text back to data
    output = yaml.load(subs)
    #make sure we have the mandatory attributes
    text = output.get("text")
    if text == None:
        error(title, "Missing text!")
    check_not_dict_list(text, title, "Text", "string")

    qtype = output.get("type")
    if qtype == None:
        error(title, "Missing type!")
    check_not_dict_list(text, title, "Question type", "just a word")


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

#so many arguments :(
def check_not_dict_list(thing,title,name,goal):
    if isinstance(thing, list) or isinstance(thing,dict):
        error(title, str(name) +" must be a "+ str(goal) +"!")

def check_list(thing,title,name):
    if not isinstance(thing, list):
        error(title, str(name) +" must be a list!")

def main():
    seed = int(sys.argv[1])
    quiz = yaml.load(open("quiz.yml"))

    random.seed(seed)

    if quiz.get('shuffle', True):
        random.shuffle(quiz['questions'])

    quiz['seed'] = seed
    quiz['time-generation'] = time.ctime()  # !!! posar format YYYY-MM-DD HH:MM:SS

    #Check types
    check_not_dict_list(quiz.get("statement"), "Quiz", "Statement", "text")

    score_sum = 0
    for question in quiz['questions']:
        score = question.get("score", 0)
        weight = question.get("weight", 1) 
        if not isinstance(score,int) or score <= 0:
            error("quiz", "All scores must be positive integers")
        if not isinstance(weight,int) or weight <= 0:
            error("quiz", "All weights must be positive integers")
        score_sum += score
        if not question.get("file", False) or not question.get("title", False):
            error("quiz","All questions need a file and a title!")
        question['q'] = build_q(question['file'], question['title'])
        question['a'] = {}
        question['points'] = 0
    if score_sum != 100:
        error("quiz", "Scores don't add to 100!!!")

    json.dump(quiz, sys.stdout, indent=4)

main()