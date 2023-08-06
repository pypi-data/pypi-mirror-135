# simager
Tools for Auto Machine Learning and Text Preprocessing.
End to end ML research (preprocessing, modelling, hyperparameter tuning) just using a few line of codes

## Features
```
- Auto Classification
- Text Preprocessing
```

## Instalation
```
pip install simager
```
## Getting Started
- Auto Classification
```
from simager.ml import ConfigData, ConfigPreprocess, ConfigModel, AutoClassifier

config_data = ConfigData(
    target="target",
    cat_features = ["column1", "column2"],
    num_features = ["column3","column4", "column5"]
)
config_preprocess = ConfigPreprocess(
    cat_imputer="SimpleImputer",
    num_imputer="SimpleImputer",
    scaler="RobustScaler",
    encoder="OneHotEncoder"
)
config_model=ConfigModel(algoritm=algoritm=[
    "DecisionTreeClassifier",
    "KNeighborsClassifier",
    "LogisticRegression",
    "SVC",
    "RandomForestClassifier",
    "AdaBoostClassifier",
    "XGBClassifier",
    "LGBMClassifier",
    "CatBoostClassifier"
])

model = AutoClassifier(config_data = config_data,
                 config_preprocess=config_preprocess,
                 config_model=config_model)

model.fit(df)

model.hp_tuning()
```

- Text Preprocessing
```
from simager.preprocess import TextPreprocess

methods = [
    "rm_hastag",
    "rm_mention",
    "rm_nonascii",
    "rm_emoticons",
    "rm_html",
    "rm_url",
    "sparate_str_numb",
    "pad_punct",
    "rm_punct",
    "rm_repeat_char",
    "rm_repeat_word",
    "rm_numb",
    "rm_whitespace",
    "normalize",
    "stopwords"
]

cleaner = TextPreprocess(methods=methods)

cleaner("your text here)
```

Full Example of Usage [Here](https://github.com/ulwan/simager/tree/master/simager/example)

