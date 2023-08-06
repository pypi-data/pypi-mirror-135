# TEA - Translation Engine Architect

A command line tool to create translation engine.


## Install
First install [pipx](https://github.com/pipxproject/pipx) then (x being your python version):

```
pipx install pangeamt-tea
```

## Usage 

### Step 1: Create a new project

```
tea new --customer customer --src_lang es --tgt_lang en --flavor automotion --version 2
```

This command will create the project directory structure:


```
├── customer_es_en_automotion_2
│   ├── config.yml
│   └── data
```

Then enter in the directory

```
cd customer_es_en_automotion_2
```

### Step 2: Configuration

#### Tokenizer

A tokenizer can be applied to source and target

```
tea config tokenizer --src mecab  --tgt moses
```

To list all available tokenizer:

```
tea config tokenizer --help
```
if you would not like to use tokenizers you can run:
```
tea config tokenizer -s none -t none
```

#### Truecaser

```
tea config truecaser --src --tgt
```

if you would not like to use truecaser you can run:
```
tea config tokenizer
```


#### BPE / SentencePiece

For joint BPE:
```
tea config bpe -j
```
For not joint BPE:
```
 tea bpe -s -t
 ```
For using sentencepiece:
```
tea config bpe --sentencepiece 
```
and options --model_type TEXT (unigram) --vocab_size INTEGER (8000) if you would like to modify them from default


#### Processors
```
tea config processors -s "{processors}"
```
being processors a list of preprocesses and postprocesses.


To list all available processors:
```
tea config processors --list
```

In order to test the processors that will be applied you can run this script in the main TEA project directory:
```
debug_normalizers.py <config_file> <src_test> <tgt_test>
```
being config_file the yaml config and src_test and tgt_test the segments to test for source and target text.

#### Prepare
tea config prepare --shard_size 100000 --src_seq_length 400 --tgt_seq_length 400

#### Translation model
tea config translation-model -n onmt 


### Step 3:
Copy some multilingual ressources (.tmx, bilingual files, .af ) into the 'data' directory

### Step 4: Run
Create workflow
```
tea worflow new
```
Clean the data passing the normalizers and validators:
```
tea workflow clean -n {clean_th} -d
```
being clean_th the number of threads.

Preprocess the data (split data in train, dev or test, tokenization, BPE):
```
tea workflow prepare -n {prepare_th} -s 3
```
being prepare_th the number of threads.

Training model
```
tea workflow train --gpu 0
```
if you do not want to use gpu do not use this parameter.

Evaluate model
```
tea workflow eval --step {step} --src file.src --ref file.tgt --log file.log --out file.out --gpu 0
```

### Reset
First of all you may check the current status of the workflow using:
```
tea workflow status
```
Then you can reset your worflow at any step  (clean, prepare, train, eval) using:
```
tea worflow reset -s {step_name}
```
Or if you want to make a full reset of the workflow use:
```
tea workflow reset
```
If you need some help on how to use reset command:
```
tea workflow reset --help
```
