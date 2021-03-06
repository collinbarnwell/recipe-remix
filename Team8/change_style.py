from style_transformations import *
import copy

def removeNones(i):
    keys = ['descriptor', 'preparation', 'prep-description']
    for k in keys:
        if i[k] == 'none' or i[k] == None:
            i[k] = ''
    return i

def change_style(transformations, ingredients, steps):
    new_ingredients_list = []
    for i in ingredients:
        new_ingredient = transformations.get(i['name'].lower())
        if new_ingredient:
            formatted_ingredient = None
            if isinstance(new_ingredient, list):
                # measurement conversion
                formatted_ingredient = copy.deepcopy(i)
                formatted_ingredient['name'] = new_ingredient[0]
                if not new_ingredient[1]:
                    # remove descriptors, etc.
                    formatted_ingredient['descriptor'] = 'none'
                    formatted_ingredient['preparation'] = 'none'
                    formatted_ingredient['prep-description'] = 'none'
            else:
                # measurement conversion
                measurement_mapping = new_ingredient.get(i['measurement'])
                if measurement_mapping:
                    formatted_ingredient= {
                        'name': measurement_mapping[2],
                        'quantity': measurement_mapping[0] * i['quantity'],
                        'measurement': measurement_mapping[1],
                        'descriptor': '',
                        'preparation': '',
                        'prep-description': ''
                    }
                if not measurement_mapping and new_ingredient.get('other'):
                    formatted_ingredient = copy.deepcopy(i)
                    formatted_ingredient['name'] = new_ingredient.get('other')

            if formatted_ingredient is not None:
                new_ingredients_list.append(formatted_ingredient)
                steps = [step.replace(i['name'], formatted_ingredient['name']) for step in steps]
        else:
            new_ingredients_list.append(i)

    new_ingredients_list = [removeNones(i) for i in new_ingredients_list]
    return [new_ingredients_list, steps]


def change_style_to(new_style, ingredients, steps):
    if new_style == 'asian':
        transformations = to_asian
    elif new_style == 'mexican':
        transformations = to_mex
    elif new_style == 'vegetarian':
        transformations = to_veggie
    elif new_style == 'vegan':
        to_vegan.update(to_veggie)
        transformations = to_vegan
    else:
        raise ValueError('Transformation parameter not recognized')
    return change_style(transformations, ingredients, steps)


# ingredient format (for reference)
# {
#     "name":	"salt",
#     "quantity":	1,
#     "measurement":	"pinch",
#     "descriptor":	"table",
#     "preparation":	"none",
#     "prep-description":	"none"
# }
