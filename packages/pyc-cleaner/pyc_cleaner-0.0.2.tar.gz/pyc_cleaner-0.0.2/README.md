# Python cache cleaner

Python cache cleaner is simple CLI's tool which help to remove python cache files from folders and projects

# Installation

## 1. Using pip
```
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install pyc-cleaner
```
> Note that in Windows you should activate virtual enviroment this way: `\..> .\venv\Scripts\activate`

# How to use
After installing run this command in your terminal:
```
$ python -m python_cleaner -p "PATH/TO/PARENT_FOLDER" -sl yes
```
`-p` (or `--path`) flag means where program should clean cache, **if this flag not specified then program will use directory where you start running script**

`-sl` (or `--show_logs`) flag means whether the program should output logs to the console (default yes)
