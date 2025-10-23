# 🔢Find_missing_count :

A simple desktop app built in Python + Tkinter that parses text and detects missing numbers in a sequence.

--- 

## How to use : 

- Set a prefix to distinguish the desired counter from others if necessary.
- Set a START and END for your counter.
- Does your sequence appear more than once? Don't worry, just set the number of repetitions.
- Push the left button to open a text file and the results will be shown in the text box. 

*As default the language is set as spanish*

![Image_Alt](https://github.com/lucashorminoguez/find_missing_count/blob/main/resources/screenshot.png)

---

## Compile by yourself : 

### Windows
```bash
pyinstaller --onefile --windowed --icon=resources\icono.ico --add-data "resources\meme.gif;resources" --add-data "resources\icono.ico;resources" --name=Find_Missing_Count code\main.py
```

### Linux

```bash
pyinstaller --onefile --windowed --icon=resources/icono.ico --add-data "resources/meme.gif:resources" --add-data "resources/icono.ico:resources" --name=Find_Missing_Count code/main.py
```

---

## Download .exe
[LAST RELEASE](https://github.com/lucashorminoguez/find_missing_count/releases/latest/download/Find_Missing_Count.exe)
