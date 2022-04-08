# vc-lexical-scanner

Lexical scanner for VC language

## Requirements

Python 3.x

## Project file structure

```
|
|_ test
|    |_ lexeme_test.py
|
|_ README.md
|_ main.py
|_ parser.py
|_ rule.py
```

## Run

Run on CLI:

```
python main.py <vc_filename>.vc
```

For example:

```
python main.py file.vc
```

The output file's name will be `<vc_filename>.vctok`.
