# Words Correction Program

## About
The *Words Correction Program* is a small personal project to correct orthography in LaTeX and html files.
It was created to spell-check my thesis which contains lots of french and english
 words plus some extra scientific words plus a bunch of mistakes :P

## Usage
to run:
python words_correction_program.py [the path of your target file "/u/username/Documents/example.tex"]

## Functions
It loads french, english dictionaries plus a extra words dictionary, found in the repo.
It reads line by line, word by word the target file and search each word in the 3 dictionaries.
If it is not found, then it reports it with the corresponding document line to the user.

