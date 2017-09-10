# Toolkit to prepare quizzes for Jutge.org

## Installation

In order to use the Jutge.org quizzes toolkit,
please install its dependencies: Python3 and YAML for Python.

In order to install YAML for Python, simply execute

```bash
pip3 install pyyaml
```

(You may have to use `pip` rather than `pip3` depending on your Python installation).


## Sample quizzes

Some sample quizzes are given under the `quizzes` directory.


## How to execute

In order to generate a quiz, simply execute `make-quiz.py` inside a directory
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
    file: question1
    score: 70
```

Each quiz must pe provided with a title, a statement and a list of questions. Each question has a title, a file and a score. The score of all the questions in a quiz must add 100 points. The file of a question must be the name of the `.yml` file that describes it. In this example we must have a `question1.yml` and a `question2.yml` in the same directory as our `quiz.yml`.

### Questions
Each question is described in a `questionName.yml` file. This file must specify a `text` for the statement. Any text in the question can be generated randomly using python language. A `questionName.py` file can be created for each question, and the value of variables after the execution of the script will be swapped for expressions like ``` `$a + $b` ``` in the `questionName.yml` file, where `a` and `b` are variables defined in `questionName.py`.
> Check the demo directory for more examples and uses of this feature.

The other mandatory attribute is the `type` of the question, which can be described in the following way:

* `SingleChoice`: A question with multiple pre-defined answers where only one is true. Each answer must have a `text` field and can have a `hint` field with text to be displayed if that answer is chosen. There must be one and only one choice with a `correct: true` attribute.
* `MultipleChoice`: A question with multiple pre-defined answers where one or more of them are true. Each answer must have a `text` field and can optionally have a `hint` field with text to be displayed if that answer is chosen. There can be more than one choice with a `correct: true` attribute.
* `FillIn`: A fill-in-the-blanks question with a `context` and a list of `items`. 
  * `context`: is a text where some words are replaced with the attributes in the item list.
  * `items`: describe a blank space where the student can type the answer or a dropdown list with multiple pre-defined choices. A blank space has a `correct` answer, a `maxlength` field where an integer marks the maximum length of the answer [... TO DO !!! ...] and a list of other possible `options`.
* `Ordering`:
* `Matching`:
* `OpenQuestion`:

### Optional attributtes

#### Quiz
* Shuffle: the shuffle attribute indicates whether the order of the questions in the quiz must be changed everytime the quiz is taken. If not specified it's default value is true.
```yml
shuffle: False
```
> In this case the questions will always appear in the same order as in the `quiz.yml` file.

#### Questions
* Shuffle: The shuffle attribute will change the order of the question's choices or options.
>Does not apply to Open questions.


