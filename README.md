# Toolkit to prepare quizzes for Jutge.org

![Logo](logo.png)

## Installation

Just install it with `pip3 install jutge-quizzes-toolkit`. You can update to the latest version with `pip3 install --upgrade jutge-quizzes-toolkit`. If you want to uninstall it, just type `pip3 uninstall jutge-quizzes-toolkit`.

In case you are using Anaconda, install with `python3 -m pip install jutge-quizzes-toolkit`.



## Sample quizzes

Some sample quizzes are given under the `examples` directory.


## How to execute

In order to generate a quiz, simply execute `make-quiz` inside a directory
that contains the quiz, passing as a unique parameter an integer number that
will be used as the random seed. The output will be a JSON file with the generated
quiz.


## Documentation

A quiz is a problem that can have many different generic questions. There are several question templates.
A quiz must be placed inside a `.pbm` directory. It must have all the metadata described in the regular problem toolkit [https://github.com/jutge-org/problems-toolkit/blob/master/Help.md].

### Metadata
#### Handler
The content of the file `handler.yml` must be:
```yml
handler: quiz
```
#### Quiz
The quiz is described in the following way by the file `quiz.yml`
```yml
title: The Title of The Quiz
statement: Here you can put a statement for the quiz
questions:
  - title: Question 1
    file: question1
    score: 30
  - title: Question 2
    file: question2
    score: 70
```

Each quiz must pe provided with a title, a statement and a list of questions. Each question has a title, a file and a score. The score of all the questions in a quiz must add 100 points. The `file` of a question must be the name of the `.yml` file that describes it. In this example we must have a `question1.yml` and a `question2.yml` in the same directory as our `quiz.yml`.

### Questions
Each question is described in a `questionName.yml` file. This file must specify a `text` for the statement. Any text in the question can be generated randomly using python language. A `questionName.py` file can be created for each question, and the value of variables after the execution of the script will be swapped for expressions like ``` `$a + $b` ``` in the `questionName.yml` file, where `a` and `b` are variables defined in `questionName.py`.

The other mandatory attribute is the `type` of the question, which can be described in the following way:

* `SingleChoice`: A question with multiple pre-defined answers where only one is true. Each answer must have a `text` field and can have a `hint` field with text to be displayed if that answer is chosen. There must be one and only one choice with a `correct: true` attribute.
```yml
type: SingleChoice
text: "The statement of the question"
choices:
    -   text: "Correct answer"
        correct: true
        hint: "You did well!"
    -   text: ""Nearly correct answer`"
        hint: "Sorry..."
    -   text: "Wrong answer"
```
* `MultipleChoice`: A question with multiple pre-defined answers where one or more of them are true. Each answer must have a `text` field and can optionally have a `hint` field with text to be displayed if that answer is chosen. There can be more than one choice with a `correct: true` attribute.
```yml
type: MultipleChoice
text: "Which of the following are true?"
choices:
    -   text: "1 + 1 = 2"
        correct: true
    -   text: "`$s != $a + $b`"
        hint: "Sorry..."
    -   text: "`$a + $b >= $s`"
        correct: true
```
* `FillIn`: A fill-in-the-blanks question with a `context` and a list of `items`:
  * `context`: is a text where some words are replaced with the attributes in the item list.
  * `items`: can be either a blank space where the student can type the answer or a dropdown list with multiple pre-defined choices. A blank space has the following attributes:
    * `correct`: describes the correct answer.
    * `maxlength`: integer maximum length of the answer.
    * `placeholder`: `OPTIONAL` text to display when the answer is blank. Default is `?`.
    * `ignorecase`: `OPTIONAL` indicates whether to ignore the case of the answer or not. Default is `true`.
    * `trim`: `OPTIONAL` indicates whether to ignore the blanks before and after the answer. Default is `true`.

    A dropdown list of items has the following attributes:
      * `correct`: describes the correct answer.
      * `options`: a list of all the other possible answers that are not correct.

  > For code examples on FillIn questions please check the `quizzes/demo.pbm/en` folder.

* `Ordering`: A question with a list of `items` that has to be permutated to a specific order. The `label` attribute expects a text which will be the title of the box containing the items.
```yml
type: Ordering
text: Drag and drop the item to place the list in alfabetic order.
label: Programming language
items:
    - A
    - B
    - C
    - D
    - F
    - Z
```

* `Matching`: A match between pairs of items in two lists. An attribute `labels` is needed, with two titles for the left and right boxes. A `left` and a `right` list of items is needed, with the same number of elements in each one.
```yml
type: Matching
text: Match the lower case with their capitals.
labels:
    - Lower Case
    - Capitals
left:
    - p
    - b
    - m
right:
    - P
    - B
    - M
```
* `OpenQuestion`: A simple text field where anything can be written. The open question has only a `placeholder` attribute which is the text dsplayed in the answer box as a hint to the student.
```yml
type: OpenQuestion
text: What is your name/quest/favourite color?
placeholder: 'My name is Arthur, I want to pass this course and blue. No, yel... '
```

> Examples for all question templates can be found in the `quizzes/demo.pbm/en` folder.


#### Random question/answer generation
As mentioned before, there can be a python script for every different question that calculates the value of any string preceded by the sigil `$`. After the python code is executed, all variables in the yml file will be swapped for their values in the python program. Please note that:
  * You don't need to import the random module since it will be already imported and given a seed in the jutge code.
  * Some question types don't support multiple identyc answers, you may need to check if the random generated numbers are the same.
> Check the demo directory for more examples and uses of this feature.


### Optional attributtes

#### Quiz
* Shuffle: the `shuffle` attribute indicates whether the order of the questions in the quiz must be changed everytime the quiz is taken. If not specified it's default value is `true`.
```yml
shuffle: False
```
> In this case the questions will always appear in the same order as in the `quiz.yml` file.

#### Questions
* Shuffle: The `shuffle` attribute will change the order of the question's choices or options.
  > Does **not** apply to Ordering, Matching or Open questions.
* Partial answer: The attribute `partial_answer` will divide the question's score by all the possible answers and take into account a partial correct answer. The default value of this attribute is `false`.
  > Only applies to Multiple Choice, Fill-in and Matching questions.

### Images
You can add images to quiz statements. In rder to do so, use the following code `![](FIG_DIR/yourimage.png)`.All images must have the `.png` extension and they have to be placed directly inside the same directory as the language's `.yml` files. Please note that the `FIG_DIR/` prefix is mandatory in order for the jutge to be able to diplay the image.
> More examples of this feature in the demo quiz directory.

### Maths

You can use LaTeX mathematics in the quiz statements. Just write LaTeX formulas between high dots, such as ·\sqrt{x^2+y^2}·. The system uses [MathJax](https://www.mathjax.org/) to display the formulas.

### Hide scores

You can hide the sccore of a particular question in the quiz by setting
```yml
hide_score: true
```



# Credits

- Jordi Petit https://github.com/jordi-petit
- Cristina Raluca https://github.com/ralucado
- Jordi Reig https://github.com/jordireig



# License

[Apache License 2.0](https://raw.githubusercontent.com/jutge-org/jutge-quizzes-toolkit/master/LICENSE.txt)
