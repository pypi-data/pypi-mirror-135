## Named Entity Recognition Toolkit

Provide a toolkit for rapidly extracting useful entities from text using various Python packages, including [Stanza](https://stanfordnlp.github.io/stanza/index.html). 

### Features
We try to bring the complicated use of existing NLP toolkits down to earth by keeping APIs as simple as possible with best practice. 

### Installation
```pip
pip install ner-kit
```

### Examples

Example 1: Word segmention
```python
from nerkit.StanzaApi import StanzaWrapper
if __name__=="__main__":
    sw=StanzaWrapper()
    sw.download(lang="en")
    text='This is a test sentence for stanza. This is another sentence.'
    result1=sw.tokenize(text)
    sw.print_result(result1)
```

Example 2: Chinese word segmentation
```python
from nerkit.StanzaApi import StanzaWrapper
if __name__=="__main__":
    sw=StanzaWrapper()
    sw.download(lang="zh")
    text='我在北京吃苹果！'
    result1=sw.tokenize(text,lang='zh')
    sw.print_result(result1)
```

Example 3: Multi-Word Token (MWT) Expansion
```python
from nerkit.StanzaApi import StanzaWrapper
if __name__=="__main__":
    sw=StanzaWrapper()
    sw.download(lang="fr")
    text='Nous avons atteint la fin du sentier.'
    result1=sw.mwt_expand(text,lang='fr')
    sw.print_result(result1)
```

Example 4: POS tagging
```python
from nerkit.StanzaApi import StanzaWrapper
if __name__=="__main__":
    sw=StanzaWrapper()
    sw.download(lang='en')
    text='I like apple'
    result1=sw.tag(text)
    sw.print_result(result1)
    sw.download_chinese_model()
    text='我喜欢苹果'
    result2=sw.tag_chinese(text,lang='zh')
    sw.print_result(result2)
```

Example 5: Named Entity Recognition
```python
from nerkit.StanzaApi import StanzaWrapper

if __name__=="__main__":
    sw=StanzaWrapper()

    sw.download(lang='en')
    sw.download_chinese_model()

    text_en = 'I like Beijing!'
    result1 = sw.ner(text_en)
    sw.print_result(result1)

    text='我喜欢北京！'
    result2=sw.ner_chinese(text)
    sw.print_result(result2)

```

Example 6: Sentiment Analysis
```python
from nerkit.StanzaApi import StanzaWrapper

if __name__=="__main__":
    sw=StanzaWrapper()
    text_en = 'I like Beijing!'
    result1 = sw.sentiment(text_en)
    sw.print_result(result1)

    text_zh='我讨厌苹果！'
    result2=sw.sentiment_chinese(text_zh)
    sw.print_result(result2)
```

Example 7: Language detection from text
```python
from nerkit.StanzaApi import StanzaWrapper
if __name__=="__main__":
    sw=StanzaWrapper()
    list_text = ['I like Beijing!','我喜欢北京！', "Bonjour le monde!"]
    result1 = sw.lang(list_text)
    sw.print_result(result1)
```

Example 8: Language detection from text with a user-defined processing function
```python
from nerkit.StanzaApi import StanzaWrapper
if __name__=="__main__":
    sw=StanzaWrapper()
    list_text = ['I like Beijing!','我喜欢北京！', "Bonjour le monde!"]
    def process(model):# do your own business
        doc=model["doc"]
        print(f"{doc.sentences[0].dependencies_string()}")
    result1 = sw.lang_multi(list_text,func_process=process,download_lang='en,zh,fr')
    print(result1)
    sw.print_result(result1)
```

Example 9: Stanza's NER (Legacy use for Java-based Stanford CoreNLP)
```python
from nerkit.StanzaApi import StanfordCoreNLPClient
corenlp_root_path=f"stanfordcorenlp/stanford-corenlp-latest/stanford-corenlp-4.3.2"
corenlp=StanfordCoreNLPClient(corenlp_root_path=corenlp_root_path,language='zh')
text="我喜欢游览广东孙中山故居景点！"
list_token=corenlp.get_entity_list(text)
for token in list_token:
    print(f"{token['value']}\t{token['pos']}\t{token['ner']}")
```

Example 10: Stanford CoreNLP (Not official version)
```python
import os
from nerkit.StanfordCoreNLP import get_entity_list
text="我喜欢游览广东孙中山故居景点！"
current_path = os.path.dirname(os.path.realpath(__file__))
res=get_entity_list(text,resource_path=f"{current_path}/stanfordcorenlp/stanford-corenlp-latest/stanford-corenlp-4.3.2")
print(res)
for w,tag in res:
    if tag in ['PERSON','ORGANIZATION','LOCATION']:
        print(w,tag)
```

Example 11: Open IE
```python
from nerkit.StanzaApi import StanfordCoreNLPClient
corenlp_root_path=f"stanfordcorenlp/stanford-corenlp-latest/stanford-corenlp-4.3.2"
text = "Barack Obama was born in Hawaii. Richard Manning wrote this sentence."
corenlp=StanfordCoreNLPClient(corenlp_root_path=corenlp_root_path)
list_result=corenlp.open_ie(text)
for model in list_result:
    print(model["subject"],'--',model['relation'],'-->',model["object"])
out=corenlp.force_close_server() # support force closing port in Windows
print(out)
```

Example 12: Generate triples from files
```python
from nerkit.triples.text import generate_triples_from_files
input_folder='data'
output_folder='output'
list_result_all=generate_triples_from_files(input_folder=input_folder,
                                            output_folder=output_folder,
                                            return_all_results=True,
                                            ltp_data_folder='../ltp_data')

print(list_result_all)
```

Example 13: Generate a list of tripls
```python
from nerkit.triples.ltp import *
text=open("data/test.txt",'r',encoding='utf-8').read()
extractor=get_ltp_triple_instance(ltp_data_folder='D:/UIBEResearch/ltp_data')
list_event=get_ltp_triple_list(extractor=extractor,text=text)
for event in list_event:
    print(event)
```

### Credits & References

- [Stanza](https://stanfordnlp.github.io/stanza/index.html)
- [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)

### License
The `ner-kit` project is provided by [Donghua Chen](https://github.com/dhchenx). 

