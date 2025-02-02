# Pyzelius 1.5
## What is it?
A dashboard designed to improve workflow for manual testing, written in Python. I created it both as a tool to be used in my work, and as a little side project to kill time.

## How did you build it?
With some help from a LLM, I structured a GUI with Python's native library Tkintr, and bound relevant classes and functions to it via a Controller file (usually called business logic file).

I tried to use Classes as much as possible, and to respect the old "one method, one job" mindset. 

Apart from built-in libraries, I used Pandas and openpyxl to format the daily report, and pyperclip for added functionality. We'll see for the future. 

## What does it do?
In this version, called 1.0 for no other reason other than it is the first functioning version of the code, it has three main functionalities:
  1. Creation of a Daily Folder, also called WorkTree. The Worktree is comprised of a main folder with the current date, and two sub-directories called "Passed" and "Defects". Nothing but built-in modules used here (os, datetime);
  2. Signature generator, with values provided by entry fields in the GUI.
  3. Creation of a daily report of all the tests done, distinguishing between Passed and Defects. The class used for this iterates upon the contents of the folders "Passed" and "Defects", using their name to fill a Pandas Dataframe via a CSV (created using the " - " as a separator) which will then be printed on a spreadsheet, formatted via openpyxl.

## Why?
I'm currently working in manual testing, and it occurred to me that I did a lot of repetitive actions (searching for files, creating folders, copypasting stuff...). This is supposed to alleviate that, and to give me a base upon which to improve workflow and ability to retrace previous work in case of need. 

## What's next?
Ideally, version 2.0 will include a way to store the "signature" needed in my area of work for the tests. 
Also, hotkeys will be bound to the main functions for comfort.

As for the future, it's very abstract: one idea was to connect this dashboard to a SQLite database, in order to store the defects and be able to trace back to them and update their status whenever needed. I doubt the practicality, but I'm enthused by the possibility.

Also, statistics. I would like to use Pandas to elaborate on the tests done, making graphs, evaluating performance and so on. Just for fun.

I'm sure elaborating on the UI will also become a necessity. Tkinter is pretty fugly.

Finally, language support, for no other reason than the fact that I wanna learn how it's done.
