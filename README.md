# Tolino Notes Parser (Working Title)
The Tolino E-Reader saves highlighted text and notes in an unwieldy `notes.txt` file. So the purpose of this project is to parse this file and export the data
in markdown format.

But once the data is ingested, further functionality and output formats would be easy to implement.

## Usage

The input file (`notes.txt`) in the same directory by default. But it could be specified as an arguemt as follows:
``` bash
python main.py -i /rel/path/to/file
```
The output type (either to file `output.txt` or to stdout) is hard-coded right now.

## Shortcomings 

* Duplicates are not yet accounted for.
  * When a note is added to a highlight
  * When a note is edited (once or multiple times) etc.
  
