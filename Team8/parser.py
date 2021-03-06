from recipeparser import parseHtml
from cooking_methods import METHODS
from tools import toolFinder
from ingredients import findIngredients
from extract_cooking_methods import extract_cooking_methods


class Parser:
    def __init__(self, url):
        self.full_recipe = None
        self.url = url
        self.parse_html()

    def __package__(self):
        return self.__name__

    def parse_html(self):
        parsed = parseHtml(self.url)
        self.ingredients = [i.encode('ascii', 'ignore') for i in parsed["ingredients"]]
        self.steps = [s.encode('ascii', 'ignore') for s in parsed["directions"]]
        self.cook_time = parsed["cook time"].encode('ascii', 'ignore')
        self.prep_time = parsed["prep time"].encode('ascii', 'ignore')
        self.name = parsed["name"].encode('ascii', 'ignore')

    def separate_ingredients(self):
        return findIngredients(self.ingredients)

    def get_tools(self):
        return toolFinder(self.steps, self.ingredients)

    def get_primary_cooking_method(self):
        for m in reversed(METHODS):
            if m in self.name.lower():
                return m
        if 'preheat' in self.steps[0].lower():
            return 'bake'
        for step in reversed(self.steps):
            for m in METHODS:
                if m in step.lower():
                    return m
        return 'mix'

    def get_cooking_methods(self):
        return extract_cooking_methods(self.steps, self.name)

    def fully_parsed(self):
        if self.full_recipe == None:
            self.full_recipe = {
                "url": self.url,
                "ingredients": self.separate_ingredients(),
                "primary cooking method": self.get_primary_cooking_method(),
                "cooking methods": self.get_cooking_methods(),
                "cooking tools": self.get_tools(),
                "name": self.name
            }
        return self.full_recipe
