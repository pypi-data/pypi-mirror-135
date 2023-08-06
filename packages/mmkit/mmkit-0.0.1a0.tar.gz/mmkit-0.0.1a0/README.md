## MMKit: Multimodal Kit

A toolkit for multimodal information processing

### Installation

```
    pip install mmkit
```

### An example

A Neural Network in PyTorch for Tabular Data with Categorical Embeddings. [Here](https://yashuseth.wordpress.com/2018/07/22/pytorch-neural-network-for-tabular-data-with-categorical-embeddings/#8230)

```python
from mmk.prediction import MultimodalPredictionModel
input_features=[ ... ]
categorical_features = [...]
output_feature = "..."
output_error=0
all_features=input_features+[output_feature]
mmpm=MultimodalPredictionModel("data/multimodal_data.csv",
                               all_features,
                               categorical_features,
                               output_feature,
                               output_error)
mmpm.train()
acc=mmpm.get_last_accuracy()
print(acc)
```

### License
The `mmkit` project is provided by [Donghua Chen](https://github.com/dhchenx). 

