# Random-brain

[![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)


[![](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![](https://img.shields.io/website-up-down-green-red/http/monip.org.svg)](https://einelson.github.io/projects/random_brain/random_brain.html)
[![](https://img.shields.io/bitbucket/issues/einelson/Random-brain)]()


## About
Random brain is the neural network implementation of a random forest. Its purpose is to combine the strengths of multiple nerual networks.

## Background on random forests
A random forest is a machine learning model that is composed of multiple decision trees. These trees in the forest all predict an outcome and the majority rules.

## Similarities
Just as the random forest is a vote based ML algorithm, the random brain is a vote based algorithm as well, but uses neural networks specified by the user rather than decision forests.

## Setting up Random brain
```
pip install random-brain
```

## API
Init the brain module and class.
```
from random_brain import random_brain
brain = random_brain.random_brain()
```

**import models()**

Import models will take in a directory or a single .h5 file. Sub directories will be ignored.
```
brain.import_models(model_path = 'path/to/model.h5')
brain.import_models(model_path = 'path/to/directory')
```

**show_brain()**

Shows the keys used in the brain. This should just be the name of each imported model
```
brain.show_brain()
```


**clear_brain()**

Clear a single model or more by entering in the model name as a list. Leave blank to clear all models.
```
brain.clear_brain(item_list = ['model to remove'])
```

**vote**

Add in yTest to cast votes. Vote() will only return the votes as a numpy array and not actual predictions. This is useful if you want to run your own statistics on the votes.

```
brain.vote(yTest = [1, 2, 3, 4, ...])
```

**predict (in development)**

Add in your yTest to make predictions. This will attempt to make a prediction based off of the networks and will return a single answer. This is still in development.

In the future prediction and threading options will be added and improved.
```
brain.predict(yTest = [1, 2, 3, 4, ...])
```
