# Chopin Score Onset Data Generator
Various data generator scripts in the `data_generator` folder uses third party GitHub repositories; `musicXML_parser` and `chopin_piano_score_dataset`.

## How to genereate Training Data Set

1. Git clone current repository and go inside `chopin_score_onset_data_generator` folder.
```console
$ git clone https://github.com/mac-marg-pianist/chopin_score_onset_data_generator.git
$ cd chopin_score_data_generator
```

2. Download `musicXML_parser` repository in the `chopin_score_onset_data_generator`.
```
chopin_score_data_generator$ git clone https://github.com/mac-marg-pianist/musicXML_parser.git
```

3. Download `chopin piano score dataset` repository.
```
chopin_score_data_generator$ git clone https://github.com/mac-marg-pianist/chopin_piano_score_dataset.git
```

4. Go to `data_generator` folder and run python file.

```
chopin_score_onset_data_generator$ cd data_generator
chopin_score_onset_data_generator/data_generator$ python3 complete.py
```

5. Go to top project directory and check output directory. : `essence`, `complete` or `moderate`.
e.g) `complete` is a generated output directory name.

```sys
chopin_score_onset_data_generator/data_generator$ cd ..
chopin_score_onset_data_generator$ ls
README.md                  complete                          musicXML_parser
data_generator             chopin_piano_onset_score_dataset 
```
