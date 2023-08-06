# Recipe Tagger

This package provides a classification, a tagging system and a water footprint calculator for ingredients and recipes.  
The functioning of the package is based on a dataset containing more than 700 ingredients mapped with their own class and water footprint. 
If a provided ingredient is not mapped into the dataset, the library search for it on wikipedia pages, into the dictionary and into NLTK Wordnet to find the best possible class. 
The water footprint is computed based on its ingredients. Every ingredient has a water footprint, measured in l/kg. 

An ingredient could be classified in one of the following class: 
- Vegetable
- Fruit
- Legume
- Meat
- Egg
- Diary
- Staple
- Condiment
- Nut
- Seafood
- Snack
- Mushroom
- Dessert
- Beverage

A recipe is tagged based on its ingredients class. 
The library also provides a function to get the class percentage of recipe ingredients. 

## Installation

```
pip install recipe_tagger
```
## Recipe Tagger module 

**How to use**

```python
from recipe_tagger import recipe_tagger
```

**Get the class of a single ingredient**

```python
recipe_tagger.get_ingredient_class('aubergine')
# vegetable
```

**Get tags of a recipe (it is needed to provide all the ingredient of the recipe)**

```python
recipe_tagger.get_recipe_tags(['aubergine', 'chicken'])
# ['vegetable', 'meat']
```

**Get class percentage of a recipe (it is needed to provide all the ingredient of the recipe)**

```python
recipe_tagger.get_recipe_class_percentage(['aubergine', 'chicken', 'beef'])
# [('vegetable', '33.33%'), ('meat', '66.67%')]
```

## Recipe Water Footprint module

**How to use**

```python
from recipe_tagger import recipe_waterfootprint as wf
```

**Get the water footprint of a single ingredient**

```python
wf.get_ingredient_waterfootprint("tomato", 20, process=True, language="en")
# 4.28
```

**Get the water footprint of a recipe (it is needed to prived all the ingredients and the quantity of the recipe)**

In order to provide a precise calculation of the WF, it is needed to provide also the quantity used for the ingredient in the recipe. 
Quanities must be provided matching the following pattern: "{number}{unit}". Unit can be one of ml, gr, kg, l, ounce, teaspoon, tablespoon, cup, pint quart, gallon, pound, clove, lb, or their abbreviation.

```python
wf.get_recipe_waterfootprint(
            ["tomato", "apple", "chicken"], 
            ["20gr", "5ml", "1l"], 
            language="en")
# 4329.28
```

**Get the water footprint of a recipe and informations about the ingredients water footprint**
```python
wf.get_recipe_waterfootprint(
            ["tomato", "apple", "chicken"],
            ["20gr", "5ml", "1l"],
            language="en",
            information=True,
        )
# (4329.28, {"tomato": 4.28, "apple": 0.0, "chicken": 4325.0})
```


## Language support
Every method of the package provide the language support. Use the "language" parameter along with the abbreviation of a supported language. 
Default language is English, if the "language" argument is not provided. 

- English ("en")
- Italian ("it")


## Todo
- [x] Handling of Wikipedia pages.
- [x] Better search over dictionary and Wikipedia pages of ingredient.
- [x] Calculate the water foorprint of a recipe
- [ ] Add the possibility to add an ingredient after search if it is not present into the embedding.
- [ ] An explanation in order to provided an other language. 
- [ ] A method for automatic translation when providing another language. 
