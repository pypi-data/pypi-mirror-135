## About The Project

This is a part of project that we are working on it for the Cyber-Physical Group (i6) at the Technical University of Munich. In this part, we develop a script extractor to extract the information such as abstract, author(s), supervisor(s), advisor(s), date of submission, etc.

### Built With

Python script has been used for this part of the project.

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
```Python
from Extract_info import Extract
directory = "D:\CPS\HiWiProjects\Parse\data\mnt\current" #This is a sample directory. You have to change it to your desired directory.
format = "tex" #For now, the code can extract the information from LaTeX(.tex) and Text(.txt) files.
E = Extract(directory, format)
All_information = E.Extract_all_together()
Only_Abstracts = E.Extract_Abstract() #This will give you the English and German version of the abstract. The German version may be empty.
Only_Authors = E.Extract_Author()
Only_Titles_en = E.Extract_Titles_en() #English titles
Only_Titles_de = E.Extract_Titles_de() #German titles
Only_Dates = E.Extract_Date()
Only_Supervisors = E.Extract_Supervisor()
Only_Advisors = E.Extract_Advisor()
Only_ThesisTypes = E.Extract_ThesisType()

```
## Features
- [x] Multi-language Support
    - [x] English
    - [x] German
- [ ] Generic
