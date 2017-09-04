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

TBD !!!


