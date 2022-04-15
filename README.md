# Tolino Notes Parser (Working Title)
The Tolino E-Reader saves highlighted text and notes in an unwieldy `notes.txt` file. So the purpose of this project is to parse this file and export the data
in markdown format.

But once the data is ingested, further functionality and output formats would be easy to implement.

## Usage

The input file (`notes.txt`) and the output type (file or stdout) are hard-coded right now.
``` bash
python main.py
```

## Shortcomings 

* I'm still not sure how to handle sanitizing the highlighted text and notes. But here are some ideas:
  * remove newline characters from beginnings of lines
  * remove weird spacings ( multiple spaces or tabs etc. )
    * current RegEx for this also removes newline characters when they occur in the middle of the string.
* Duplicates are not yet accounted for.
  * When a note is added to a highlight
  * When a note is edited (multiple time maybe) etc.
  
