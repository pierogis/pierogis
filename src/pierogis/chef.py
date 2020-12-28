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
        quantize_parser.set_defaults(create_dish_desc=self.create_quantize_dicts)

        recipe_parser = argparse.ArgumentParser(add_help=False)
        recipe_parser.set_defaults(create_dish_desc=self.create_recipe_dicts)
        recipe_parser.add_argument('recipe_path', type=str, default='./recipe.txt')

        self.menu = {
            'sort': sort_parser,
            'quantize': quantize_parser,
            'recipe': recipe_parser
        }

    def create_recipe_dicts(self, ingredients, season_links, recipes, file_links, recipe_path, **kwargs):
        try:
            with open(recipe_path) as recipe_file:
                ingredients, seasons, recipes, file_links = self.read_recipe(ingredients, season_links, recipes,
                                                                             file_links, recipe_file.read())

            return ingredients, seasons, recipes, file_links

        except Exception as err:
            print(err)

    def create_pierogi_desc(self, ingredients, season_links, recipes, file_links, path):
        pierogi_uuid = uuid.uuid4()
        file_uuid = uuid.uuid4()

        ingredients[pierogi_uuid] = {
            'type': 'pierogi',
            'args': [],
            'kwargs': {
                'file': file_uuid
            }
        }

        file_links[file_uuid] = path

        recipes.append([pierogi_uuid])

        return ingredients, season_links, recipes, file_links

    def create_sort_desc(self, ingredients, season_links, recipes, file_links, **kwargs):
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
            sort_uuid = uuid.uuid4()
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
                season_uuid = uuid.uuid4()
                ingredients[season_uuid] = threshold_dict

                season_links[sort_uuid] = season_uuid

            recipes.append([sort_uuid])

            return ingredients, season_links, recipes, file_links

        except Exception as err:
            print(err)

    def create_quantize_dicts(self, **kwargs):
        return

    def create_dish(self, ingredient_descs, seasoning_links, recipe_orders, file_links):
        """
        Create a dish from a series of descriptive dicts
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

        # for ingredient_name, ingredient in ingredients.items():
        #     # if an ingredient has a target we should look it up in the ingredient dictionary
        #     target_name = getattr(ingredient, 'target', None)
        #     if target_name is not None:
        #         target = ingredients[target_name]
        #         ingredient.target = target

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

    def read_recipe(self, ingredients, season_links, recipes, file_links, recipe_text):
        lines = recipe_text.split('\n')

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        for command, command_parser in self.menu.items():
            subparsers.add_parser(command, parents=[command_parser], add_help=False)

        for i in range(len(lines)):
            line = lines[i]
            phrases = line.split()

            parsed = parser.parse_args(phrases)
            parsed_vars = vars(parsed)
            create_dish_desc = parsed_vars.pop('create_dish_desc')

            ingredients, season_links, recipes, file_links = create_dish_desc(ingredients, season_links, recipes,
                                                                              file_links, **parsed_vars)

        return ingredients, season_links, recipes, file_links

    def cook_json_dish(self, output_file, ingredients_dict, recipe, files, seasons=None):
        """
        Use json dicts to construct ingredients and put them into a recipe in a given order
        :param output_file:
        :param ingredients_dict:
        :param recipe:
        :param files:
        :param seasons:
        :return:
        """
        ingredients = {}
        seasonings = {}

        for name, dict_ingredient in ingredients_dict.items():
            ingredient_args = dict_ingredient.get('args')
            ingredient_kwargs = dict_ingredient.get('kwargs', {})

            path = ingredient_kwargs.pop('path', None)
            if path is not None:
                ingredient_kwargs['file'] = files[path]

            # handle seasonings
            target = ingredient_kwargs.get('target')
            if target is not None:
                seasonings['name'] = target

            ingredient_class = self.ingredient_classes[dict_ingredient['type']]

            ingredient = ingredient_class(*ingredient_args, **ingredient_kwargs)
            ingredients[name] = ingredient

        for season_dict in seasons:
            seasoning = ingredients[season_dict['seasoning']]
            recipient = ingredients[season_dict['recipient']]
            seasoning.season(recipient)

        recipe = Recipe(ingredients=[ingredients[ingredient_name] for ingredient_name in recipe])
        dish = Dish(recipe=recipe)
        dish.serve()

        dish.save(output_file)
