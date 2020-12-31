import argparse
import uuid

from pierogis import Dish, Pierogi, Sort, Quantize, Threshold, Recipe


class Chef:
    ingredient_classes = {
        'pierogi': Pierogi,
        'sort': Sort,
        'quantize': Quantize,
        'threshold': Threshold
    }

    # seasoning_classes = {
    #     'threshold': Threshold
    # }

    def __init__(self):
        sort_parser = argparse.ArgumentParser(add_help=False)
        sort_parser.set_defaults(create_dish_desc=self.create_sort_desc)
        sort_parser.add_argument('-t', '--turns', default=0, type=int)
        sort_parser.add_argument('-l', '--lower-threshold', default=64, type=int,
                                 help='Pixels with lightness below this threshold will not get sorted')
        sort_parser.add_argument('-u', '--upper-threshold', default=180, type=int,
                                 help='Pixels with lightness above this threshold will not get sorted')

        quantize_parser = argparse.ArgumentParser(add_help=False)
        quantize_parser.set_defaults(create_dish_desc=self.create_quantize_desc)
        quantize_parser.add_argument('-k', '--colors', default=8)

        recipe_parser = argparse.ArgumentParser(add_help=False)
        recipe_parser.set_defaults(create_dish_desc=self.create_recipe_desc)
        recipe_parser.add_argument('recipe_path', type=str, default='./recipe.txt')

        self.menu = {
            'sort': sort_parser,
            'quantize': quantize_parser,
            'recipe': recipe_parser
        }

    def read_recipe(self, ingredients, seasoning_links, recipes, file_links, recipe_text):
        lines = recipe_text.split(';')

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        for command, command_parser in self.menu.items():
            subparsers.add_parser(command, parents=[command_parser], add_help=False)

        for i in range(len(lines)):
            line = lines[i]
            phrases = line.split()

            parsed, unknown = parser.parse_known_args(phrases)
            parsed_vars = vars(parsed)
            create_dish_desc = parsed_vars.pop('create_dish_desc')

            ingredients, seasoning_links, recipes, file_links = create_dish_desc(ingredients, seasoning_links, recipes,
                                                                              file_links, **parsed_vars)

        return ingredients, seasoning_links, recipes, file_links

    def create_recipe_desc(self, ingredients, seasoning_links, recipes, file_links, recipe_path, **kwargs):
        try:
            with open(recipe_path) as recipe_file:
                ingredients, seasoning_links, recipes, file_links = self.read_recipe(ingredients, seasoning_links, recipes,
                                                                             file_links, recipe_file.read())

            return ingredients, seasoning_links, recipes, file_links

        except Exception as err:
            print(err)

    def create_pierogi_desc(self, ingredients, seasoning_links, recipes, file_links, path):
        pierogi_uuid = str(uuid.uuid4())
        file_uuid = str(uuid.uuid4())

        ingredients[pierogi_uuid] = {
            'type': 'pierogi',
            'args': [],
            'kwargs': {
                'file': file_uuid
            }
        }

        file_links[file_uuid] = path

        recipes.append([pierogi_uuid])

        return ingredients, seasoning_links, recipes, file_links

    def create_sort_desc(self, ingredients, seasoning_links, recipes, file_links, **kwargs):
        """
        Sort pixels in an image by intensity
        """
        try:
            # seasoning is for things that process but don't return a array
            sort_dict = {
                'type': 'sort',
                'args': [],
                'kwargs': {
                    **kwargs
                }
            }
            sort_uuid = str(uuid.uuid4())
            ingredients[sort_uuid] = sort_dict

            # check for implied threshold
            lower_threshold = kwargs.pop('lower_threshold')
            upper_threshold = kwargs.pop('upper_threshold')
            if (lower_threshold is not None) or (upper_threshold is not None):
                threshold_dict = {
                    'type': 'threshold',
                    'args': [],
                    'kwargs': {
                        'lower_threshold': lower_threshold,
                        'upper_threshold': upper_threshold
                    }
                }
                season_uuid = str(uuid.uuid4())
                ingredients[season_uuid] = threshold_dict

                seasoning_links[sort_uuid] = season_uuid

            recipes.append([sort_uuid])

            return ingredients, seasoning_links, recipes, file_links

        except Exception as err:
            print(err)

    def create_quantize_desc(self, ingredients, seasoning_links, recipes, file_links, **kwargs):
        quantize_dict = {
            'type': 'quantize',
            'args': [],
            'kwargs': {
                **kwargs
            }
        }
        quantize_uuid = str(uuid.uuid4())
        ingredients[quantize_uuid] = quantize_dict

        recipes.append([quantize_uuid])

        return ingredients, seasoning_links, recipes, file_links

    def cook_dish_desc(self, ingredient_descs, seasoning_links, recipe_orders, file_links):
        """
        Cook a dish from a series of descriptive dicts
        """

        ingredients = {}
        target = None

        for ingredient_name, ingredient_desc in ingredient_descs.items():
            # if path is one of the kwargs, we should look it up in the linking paths dictionary
            file_name = ingredient_desc['kwargs'].get('file')
            if file_name is not None:
                file = file_links[file_name]
                ingredient_desc['kwargs']['file'] = file

            # now create an ingredient as specified in the description
            ingredient_class = self.ingredient_classes[ingredient_desc['type']]
            ingredient = ingredient_class(*ingredient_desc['args'], **ingredient_desc['kwargs'])

            ingredients[ingredient_name] = ingredient

        for recipe_order in recipe_orders:
            recipe = Recipe(ingredients=[])
            if target is not None:
                recipe.add(target)
            # loop through the ingredient keys specified by the recipe
            for ingredient_name in recipe_order:
                # get an "initialization request" in the form of a dict
                ingredient = ingredients[ingredient_name]

                # if there is a season to be applied to this ingredient
                seasoning_name = seasoning_links.get(ingredient_name)
                if seasoning_name is not None:
                    # get the ingredient to apply the season
                    seasoning = ingredients[seasoning_name]
                    seasoning.target = target
                    seasoning.season(ingredient)

                # add this created ingredient to the dish recipe for return
                recipe.add(ingredient)

            dish = Dish(recipe=recipe)
            target = dish.serve()

        return target
