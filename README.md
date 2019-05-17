# Demo projects web-dev
## Installation
The project requires Python3.*<br>
The project can be installed by downloading [source codes](https://github.com/aozerets/web-dev/releases/) 
as a zip archive or by cloning this repository.
***
## Содержание
1. [Task#1 Code Refactoring](#code-refactoring-)
2. [Task#2 Features](#features-)
***
### Code Refactoring <br>
The project requires nltk package<br>
File [src/raw_project.py](src/raw_project.py) modified to file [src/modified_project.py](src/modified_project.py).<br>
Using decomposition, right naming of functions and variables, adding docstrings.<br>
To get the data you need to call the file [src/modified_project.py](src/modified_project.py) without arguments.
***
### Features <br>
##### Usage and requirements
The project requires nltk package<br>
To get the data you need to call the file [src/project_statistics.py](src/project_statistics.py) with the following arguments:<br>
![usage](https://github.com/aozerets/web-dev/blob/master/options.jpg)<br>
Example of use:<br>
```
>>>python /path/to/dclnt_class.py -p https://github.com/aozerets/web-dev.git -w verb -f name
```
An example of the result obtained in the console:<br>
![result](https://github.com/aozerets/web-dev/blob/master/result.jpg)<br>
##### Improvements in comparison with [task#1](#code-refactoring)
File [src/modified_project.py](src/modified_project.py) modified to new features to file [src/project_statistics.py](src/project_statistics.py).<br>
Using the OOP.<br>
Downloading projects from repositories.<br>
Different statistics possibilities.<br>
Different report format.<br>