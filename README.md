# Tolino Notes Parser (Working Title)
The Tolino E-Reader saves highlighted text and notes in an unwieldy `notes.txt` file. So the purpose of this project is to parse this file
and have multiple output formats and multiple managment features available.

Currently, the output of the script is intended for use with [logseq](https://github.com/logseq/logseq)

## Usage

Once you have your `notes.txt` run:

``` bash
python main.py -i /rel/path/to/input -o /rel/path/to/output
```
The cli arguments default to `-i notes.txt` and `-o output.txt`.

There are a couple of global variables that are hard-coded at the top of the script.

The script also prints to stdout.

## Shortcomings 

* The output structure isn't configurable and so is only adjusted to my needs at the moment.
* Tolino has to be set to german
* Only Tolino firmwares `> 15.0.0` are supported.
* Duplicates are not yet accounted for. For example:
  * When a note is added to a highlight
  * When a note is edited (once or multiple times) etc.
  
