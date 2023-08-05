## Opinion Analysis Toolkit

A toolkit to extract opinions and useful information from text

### Installation
```pip
pip install opinionx
```

### Example Usage
1. Find opinions
```python
from opinionx.text import get_opinion
text=open("test.txt",'r',encoding='utf-8').read()
opinion_words=['表示','认为','说','介绍','提出','透露','指出','强调','：']
list_opinion,_,_=get_opinion(text,lang='zh',opinion_words=opinion_words)
for opinion in list_opinion:
    print(opinion)
```
2. Find Leader's Opinions
```python
from opinionx.text import get_leader_opinions

text=open("test.txt",'r',encoding='utf-8').read()

list_opinion = get_leader_opinions(text,save_path="", search_keywords_path="data/search_keywords.csv",leader_path="data/g20_leaders.csv")
print()
for opinion in list_opinion:
    print(opinion)
    print(opinion["opinion"])
    print(opinion["first_found_keyword"])
    print(opinion["first_found_leader"])
    print()

```
3. run tf-idf and tf models for massive text files
```python
from opinionx.tfidf_shell import *
run_tfidf_shell(input_folder="tfidf_folder/raw_data", # a list of text files
                output_folder="tfidf_folder/output", # output folder
                user_dict_path="tfidf_folder/user_dictionaries", # the folder contains csv files with each line as a word
                font_path="utils/fonts/SimHei.ttf",# use it when analysis Chinese text
                is_html=True
                )
```

### Credits & References

- [Stanza](https://stanfordnlp.github.io/stanza/index.html)
- [jieba](https://github.com/fxsjy/jieba)

### License
The `opinionx` project is provided by [Donghua Chen](https://github.com/dhchenx). 

