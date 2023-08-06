# BERT-STEM

BERT model fine-tuned on Science Technology Engineering and Mathematics (STEM) lessons.

## Install:

To install from pip:

```
pip install bertstem
```

## Quickstart

To encode sentences :

```python
from BERT_STEM.BertSTEM import *
bert = BertSTEM()

# Example dataframe with text in spanish
data = {'col_1': [3, 2, 1], 
'col_2': ['hola como estan', 'alumnos queridos', 'vamos a hablar de matematicas']}

df = pd.DataFrame.from_dict(data)

# Encode sentences using BertSTEM:
bert._encode_df(df, column='col_2', encoding='sum')

```
To classify sentences with COPUS models:

```python
from BERT_STEM.BertSTEM import *

# Download BERT for classification (guiding/presenting/administration)
bert_classification = BertSTEMForTextClassification(2, model_name = 'pablouribe/bertstem-copus-guiding')

# Example dataframe with text in spanish
data = {'col_1': [3, 2, 1], 
'col_2': ['hola como estan', 'alumnos queridos', 'vamos a hablar de matematicas']}

df = pd.DataFrame.from_dict(data)

# Classify sentences using BertSTEM for COPUS (Guiding):
bert_classification.predict(df,'col_2')

```


To use it from HuggingFace:

```python
from BERT_STEM.Encode import *
import pandas as pd
import transformers

# Download spanish BERTSTEM:
model = transformers.BertModel.from_pretrained("pablouribe/bertstem")

# Download spanish tokenizer:
tokenizer = transformers.BertTokenizerFast.from_pretrained("dccuchile/bert-base-spanish-wwm-uncased",
                                                            do_lower_case=True, 
                                                            add_special_tokens = False)

# Example dataframe with text in spanish
data = {'col_1': [3, 2, 1], 
        'col_2': ['hola como estan', 'alumnos queridos', 'vamos a hablar de matematicas']}
        
df = pd.DataFrame.from_dict(data)

# Encode sentences using BertSTEM:
sentence_encoder(df, model, tokenizer, column = 'col_2', encoding = 'sum')
```


