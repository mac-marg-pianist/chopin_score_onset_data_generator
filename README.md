# Chopin Score Data Generator
Various data generator scripts in the `data_generator` folder uses third party GitHub repositories; `musicXML_parser` and `chopin_piano_score_dataset`.

## How to genereate Training Data Set

1. Git clone current repository.
```
$ git clone https://github.com/mac-marg-pianist/chopin_score_data_generator.git
```

2. Download `musicXML_parser` repository.
```
$ git clone https://github.com/mac-marg-pianist/musicXML_parser
```

3. Download `chopin piano score dataset` repository.
```
$ git clone https://github.com/mac-marg-pianist/chopin_piano_score_dataset.git
```

4. Go to `data_generator` folder and run python file.

```
chopin_score_data_generation$ cd data_generator
chopin_score_data_generation/data_generator$ python3 complete.py
```

5. Go to top project folder and check output directory.
e.g) `complete` folder is a generated output directory.

```
chopin_score_data_generation/data_generator$ cd ..
chopin_score_data_generation$ ls
README.md                  complete.py                   musicXML_parser
data_generator             chopin_piano_score_dataset 
```
