### Requirement
The project requires nltk package<br>

### Features <br>
##### Usage and requirements
To get the data you need to call the file [src/statistics/project_statistics.py](src/statistics/project_statistics.py) with the following arguments:<br>
![usage](https://github.com/aozerets/web-dev/blob/master/share/options.jpg)<br>
Example of use:<br>
```
>>>python /path/to/project_statistics.py -p https://github.com/aozerets/web-dev.git -w verb -f name
```
An example of the result obtained in the console:<br>
![result](https://github.com/aozerets/web-dev/blob/master/share/result.jpg)<br>
##### Improvements in comparison with [task#1](#code-refactoring)
File [src/refactoring/modified_project.py](src/refactoring/modified_project.py) modified to new features to file [src/statistics/project_statistics.py](src/statistics/project_statistics.py).<br>
Using the OOP.<br>
Downloading projects from repositories.<br>
Different statistics possibilities.<br>
Different report format.<br>
