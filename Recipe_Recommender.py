from recipe_scrapers import scrap_me

### recipe_scrapers via github user hhursev https://github.com/hhursev/recipe-scraper
### used to scrape recipe information from allrecipes.com and uses the following license
### The MIT License (MIT)
### Copyright (c) 2015 Hristo Harsev
### Permission is hereby granted, free of charge, to any person obtaining a copy of
### this software and associated documentation files (the "Software"), to deal in
### the Software without restriction, including without limitation the rights to
### use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
### the Software, and to permit persons to whom the Software is furnished to do so,
### subject to the following conditions:
### The above copyright notice and this permission notice shall be included in all
### copies or substantial portions of the Software.
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
### IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
### FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
### COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
### IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
### CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

import re
import webbrowser
import time
from collections import OrderedDict

# Start with the web address and image file address for each allrecipes.com recipe
recipe_dict = {0: ["http://allrecipes.com/recipe/18805/old-fashioned-mac-and-cheese/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/250x250/792047.jpg"],
              1: ["http://allrecipes.com/recipe/18443/bolognese-sauce/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/600x600/632273.jpg"],
              2: ["http://allrecipes.com/recipe/85148/fast-and-friendly-meatballs/?internalSource=hn_carousel%2002_Fast%20and%20Friendly%20Meatballs&referringId=15455&referringContentType=recipe%20hub&referringPosition=carousel%2002",
              "http://images.media-allrecipes.com/userphotos/250x250/570651.jpg"],
              3: ["http://allrecipes.com/recipe/14830/hummus-iii/?internalSource=hub%20recipe&referringId=1281&referringContentType=recipe%20hub",
              "http://images.media-allrecipes.com/userphotos/250x250/196404.jpg"],
              4: ["http://allrecipes.com/recipe/19632/turkey-burgers/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/720x405/697161.jpg"],
              5: ["http://allrecipes.com/recipe/13206/grandmas-chicken-noodle-soup/?internalSource=hub%20recipe&referringId=1246&referringContentType=recipe%20hub",
              "http://images.media-allrecipes.com/userphotos/250x250/894017.jpg"],
              6: ["http://allrecipes.com/recipe/244632/turkish-chicken-kebabs/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/600x600/2451266.jpg"],
              7: ["http://allrecipes.com/recipe/36002/bbq-steak/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/250x250/94934.jpg"],
              8: ["http://allrecipes.com/recipe/16468/tuna-fish-salad/?internalSource=hub%20recipe&referringId=2809&referringContentType=recipe%20hub",
              "http://images.media-allrecipes.com/userphotos/720x405/236438.jpg"],
              9: ["http://allrecipes.com/recipe/16428/baked-beans-ii/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/250x250/395974.jpg"],
              10: ["http://allrecipes.com/recipe/220151/citrus-chicken-stir-fry/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/720x405/2167053.jpg"],
              11: ["http://allrecipes.com/recipe/94374/shrimp-leek-and-spinach-risotto/?internalSource=search%20result&referringContentType=search%20results",
              "http://images.media-allrecipes.com/userphotos/720x405/3503174.jpg"],
              12: ["http://allrecipes.com/recipe/14057/yummy-veggie-omelet/?internalSource=search%20result&referringContentType=search%20results",
               "http://images.media-allrecipes.com/userphotos/720x405/627913.jpg"],
              13: ["http://allrecipes.com/recipe/14280/fresh-broccoli-salad/?internalSource=search%20result&referringContentType=search%20results",
               "http://images.media-allrecipes.com/userphotos/720x405/727586.jpg"],
              14: ["http://allrecipes.com/recipe/19960/avocado-salad/?internalSource=search%20result&referringContentType=search%20results",
               "http://images.media-allrecipes.com/userphotos/720x405/256657.jpg"],
              15:  ["http://allrecipes.com/recipe/21736/pan-seared-salmon-i/?internalSource=hn_carousel%2001_Pan-Seared%20Salmon%20I&referringId=416&referringContentType=recipe%20hub&referringPosition=carousel%2001",
               "http://images.media-allrecipes.com/userphotos/720x405/998740.jpg"],
              16:  ["http://allrecipes.com/recipe/34746/baked-salmon-ii/?internalSource=hub%20recipe&referringId=416&referringContentType=recipe%20hub",
               "http://images.media-allrecipes.com/userphotos/720x405/593567.jpg"],
              17:  ["http://allrecipes.com/recipe/236918/salvadorian-baked-fish/?internalSource=search%20result&referringContentType=search%20results",
               "http://images.media-allrecipes.com/userphotos/600x600/3113116.jpg"],
              18: ["http://allrecipes.com/recipe/25345/tofu-lasagna/?internalSource=staff%20pick&referringId=270&referringContentType=recipe%20hub",
               "http://images.media-allrecipes.com/userphotos/720x405/106924.jpg"],
              19: ["http://allrecipes.com/recipe/21321/grilled-scampi/?internalSource=search%20result&referringContentType=search%20results",
               "http://images.media-allrecipes.com/userphotos/250x250/230834.jpg"],
              20: ["http://allrecipes.com/recipe/53302/grilled-asian-ginger-pork-chops/?internalSource=staff%20pick&referringId=674&referringContentType=recipe%20hub",
               "http://images.media-allrecipes.com/userphotos/720x405/1001324.jpg"],
              21: ["http://allrecipes.com/recipe/216642/black-bean-soup-with-bacon/?internalSource=search%20result&referringContentType=search%20results",
               "http://images.media-allrecipes.com/userphotos/250x250/922535.jpg"]
              }

# Recipe class definition
class Recipe():
    # Initialize empty lists to house Indredient and Recipe isntance information
    all_ingredient_list = []
    recipe_list = []
    recipe_dict = {}

    # pure_ingredient_dict is used to create all the instances of Ingredient
    # class, and to find Ingredients inside recipes
    pure_ingredient_dict = {'rice': [1, 1], 
                             'Cheddar cheese': [1, 0], 
                             'Parmesan cheese': [1, 0], 
                             'Swiss cheese': [1, 0], 
                             'Worcestershire sauce': [0, 0], 
                             'almond': [1, 1], 'almonds': [1, 1],
                             'avocado': [1, 1], 'avocados': [1, 1],
                             'bacon': [0, 0], 
                             'baked bean': [1, 1], 'baked beans': [1, 1],
                             'basil': [1, 1], 
                             'beef bouillon': [0, 0], 
                             'bell pepper': [1, 1], 'bell peppers': [1, 1],
                             'black bean': [1, 1], 'black beans': [1, 1],
                             'black pepper': [1, 1], 'black peppers': [1, 1],
                             'bread crumb': [1, 0], 'bread crumbs': [1, 0],
                             'broccoli': [1, 1], 'broccolis': [1, 1],
                             'brown sugar': [1, 1], 
                             'butter': [1, 0], 
                             'caper': [0, 0], 'capers': [0, 0],
                             'carrot': [1, 1], 'carrots': [1, 1],
                             'celery': [1, 1], 'celeries': [1, 1],
                             'cheese food': [1, 0], 'cheese food': [1, 0],
                             'chicken': [0, 0], 'chickens': [0, 0],
                             'chicken broth': [0, 0], 
                             'chicken stock': [0, 0], 
                             'cilantro': [1, 1], 
                             'cinnamon': [1, 1], 
                             'cornstarch': [1, 1], 
                             'cumin': [1, 1], 
                             'egg': [1, 0], 'eggs': [1, 0],
                             'egg noodle': [1, 0], 'egg noodles': [1, 0],
                             'flour': [1, 1], 
                             'frozen vegetable': [1, 1], 'frozen vegetables': [1, 1],
                             'garbanzo bean': [1, 1], 'garbanzo beans': [1, 1],
                             'garlic': [1, 1], 'garlics': [1, 1],
                             'garlic chile paste': [1, 1], 
                             'garlic powder': [1, 1], 
                             'ginger': [1, 1], 
                             'beef': [0, 0], 'beefs': [0, 0],
                             'pork': [0, 0], 'porks': [0, 0],
                             'turkey': [0, 0], 'turkeys': [0, 0],
                             'hot pepper sauce': [1, 1], 
                             'ketchup': [1, 1], 
                             'lasagna noodle': [1, 0], 'lasagna noodles': [1, 0],
                             'leek': [1, 1], 'leeks': [1, 1],
                             'lemon': [1, 1], 'lemons': [1, 1],
                             'lime': [1, 1], 'limes': [1, 1],
                             'macaroni': [1, 1], 
                             'mayonnaise': [1, 0], 
                             'milk': [1, 0], 
                             'mozzarella cheese': [1, 0], 
                             'mushroom': [1, 1], 'mushrooms': [1, 1],
                             'mustard': [1, 1], 
                             'noodle': [1, 1], 'noodles': [1, 1],
                             'nutmeg': [1, 1],
                             'olive oil': [1, 1], 
                             'onion': [1, 1], 'onions': [1, 1],
                             'onion soup mix': [1, 0],
                             'orange': [1, 1], 'oranges': [1, 1],
                             'orange juice': [1, 1],
                             'orange marmalade': [1, 1],
                             'oregano': [1, 1],
                             'paprika': [1, 1],
                             'parsley': [1, 1],
                             'pasta': [1, 1],
                             'peanut oil': [1, 1],
                             'pepper': [1, 1], 'peppers': [1, 1],
                             'pork chop': [0, 0], 'pork chops': [0, 0],
                             'poultry seasoning': [0, 0],
                             'raisin': [1, 1], 'raisin': [1, 1],
                             'red chile pepper': [1, 1], 'red chile peppers': [1, 1],
                             'red onion': [1, 1], 'red onions': [1, 1],
                             'red pepper': [1, 1], 'red peppers': [1, 1],
                             'rosemary': [1, 1],
                             'salmon': [0, 0],
                             'salt': [1, 1],
                             'scallop': [0, 0], 'scallops': [0, 0],
                             'shrimp': [0, 0], 'shrimps': [0, 0],
                             'sour cream': [1, 0],
                             'soy sauce': [1, 1],
                             'spaghetti sauce': [0, 0],
                             'spinach': [1, 1],
                             'steak': [0, 0], 'steaks': [0, 0],
                             'sugar': [1, 1],
                             'sweet onion': [1, 1], 'sweet onions': [1, 1],
                             'tahini': [1, 1],
                             'tamari sauce': [1, 1],
                             'tofu': [1, 1],
                             'tomato': [1, 1], 'tomatoes': [1, 1],
                             'tomato sauce': [1, 1],
                             'tuna': [0, 0],
                             'vegetable broth': [1, 1],
                             'vegetable oil': [1, 1],
                             'vinegar': [1, 1],
                             'water': [1, 1],
                             'white fish': [0, 0],
                             'white wine': [1, 1],
                             'white wine vinegar': [1, 1],
                             'bean':[1,1], 'beans':[1,1],
                             'yogurt': [1, 0]}

    # Recipe initializer users scrap_me to scrape recipe information from allrecipes.com
    def __init__(self, recipe_link ="", image_link=""):
        recipe_count = 0
        from recipe_scrapers import scrap_me
        scraped_recipe = scrap_me(recipe_link)
                   
        self.title = scraped_recipe.title()
        self.number = "Recipe_" + str(len(Recipe.recipe_list)).zfill(2)
        self.time = scraped_recipe.total_time()
        self.ingredient_list = scraped_recipe.ingredients()
        self.instructions = scraped_recipe.instructions()
        self.image_link = image_link
        
        Recipe.recipe_dict[self] = [self.number, self.title]
        Recipe.recipe_list.append([self, self.number, self.title])
        Recipe.all_ingredient_list.append(self.ingredient_list)
    
    def __str__(self):
        return (str(self.title))

    @property
    def ingredients(self):
        clean_ingredient_list = []
        for i in range(len(self.ingredient_list)):
            if self.ingredient_list[i] == "ADVERTISEMENT":
                j = self.ingredient_list[i].replace("ADVERTISEMENT","")
                self.ingredient_list.pop(i)
            else:
                j = self.ingredient_list[i].replace(" ADVERTISEMENT","")
                clean_ingredient_list.append(j)
        return clean_ingredient_list
            
    @property
    def search_ingredients(self):
        search_ingredients_list = []
        for i in Recipe.pure_ingredient_dict:
            if re.search(i,str(self.ingredient_list)):
                search_ingredients_list.append(Ingredient.ingredient_dict[i][0])
            continue
        return {j.name: j for j in search_ingredients_list}
    
    def lookup_byname(self):
        lookup_list = [i[0] for i in Recipe.recipe_list if i[2] == self]
        return lookup_list[0]
    
    def lookup_bynumber(self):
        lookup_list = [i[0] for i in Recipe.recipe_list if i[1] == "Recipe_" + str(self).zfill(2)]
        return lookup_list[0]
    
    def display_image(self):
        return webbrowser.open(self.image_link)
    
    def display_recipe(self):
        print ("\n")
        print (self.title)
        print ("Total time:", self.time, "minutes")
        print("\nIngredients:")
        for x in self.ingredients:
            print(x)
        print("\nInstructions:")
        print(self.instructions)

# Ingredient class definition
class Ingredient():
    ingredient_dict = {}

    def __init__(self, name, veggie_flag=0, vegan_flag=0):
        self.name = name
        self.veggie = veggie_flag
        self.vegan = vegan_flag

        Ingredient.ingredient_dict[self.name] = [self, self.veggie, self.vegan, self.alt_name]
                                      
    def __str__(self):
        return (str(self.name))
    
    @property
    def alt_name(self):
        return [self.name+"s",self.name+"es"]

# Define find_recipe function
def find_recipe(ingredient_list):
    # Error trapping for non alpha input
    if not "".join(ingredient_list).isalpha():
        print ("\nYou seem to have entered a special character or a number incorrectly",
              "\nFor recipes, only enter the number without any other characters")
        return ""

    # Dealing with list that is less that three items, 

    ingredient_1 = ingredient_list[0]
        
    if ingredient_list[1] == "":        
        ingredient_2 = ingredient_1
    else:
        ingredient_2 = ingredient_list[1]
    
    if ingredient_list[2] == "":        
        ingredient_3 = ingredient_2
    else:
        ingredient_3 = ingredient_list[2]

    # Building sets for recipes matching each ingredient, as well as accomodating for plural input
    ingredient1_set = {Recipe.recipe_list[i][0] for i in range(len(Recipe.recipe_list)) \
    if ((re.search(ingredient_1, str(Recipe.recipe_list[i][0].search_ingredients))) \
        or (re.search(re.sub('s$','',ingredient_1), str(Recipe.recipe_list[i][0].search_ingredients)))\
        or (re.search(re.sub('es$','',ingredient_1), str(Recipe.recipe_list[i][0].search_ingredients))))\
                       and ingredient_1 in Recipe.pure_ingredient_dict}

    ingredient2_set = {Recipe.recipe_list[i][0] for i in range(len(Recipe.recipe_list)) \
    if ((re.search(ingredient_2, str(Recipe.recipe_list[i][0].search_ingredients))) \
        or (re.search(re.sub('s$','',ingredient_2), str(Recipe.recipe_list[i][0].search_ingredients)))\
        or (re.search(re.sub('es$','',ingredient_2), str(Recipe.recipe_list[i][0].search_ingredients))))\
                       and ingredient_2 in Recipe.pure_ingredient_dict}

    ingredient3_set = {Recipe.recipe_list[i][0] for i in range(len(Recipe.recipe_list)) \
    if ((re.search(ingredient_3, str(Recipe.recipe_list[i][0].search_ingredients))) \
        or (re.search(re.sub('s$','',ingredient_3), str(Recipe.recipe_list[i][0].search_ingredients))))\
                       or (re.search(re.sub('es$','',ingredient_3), str(Recipe.recipe_list[i][0].search_ingredients)))\
                       and ingredient_3 in Recipe.pure_ingredient_dict}

    # Inititalize output_dict, to populate it with recipes based on ingredient match    
    output_dict = {"Complete Match":[], ingredient_1 + "&" + ingredient_2:[],
              ingredient_2 + "&" + ingredient_3:[], ingredient_1 + "&" + ingredient_3:[],\
                  ingredient_1:[], ingredient_2:[], ingredient_3:[]}
    
    # Iterate through all recipes matching any of the ingredients
    for j in  ingredient1_set | ingredient2_set | ingredient3_set:   

        # fill in output_dict based on ingredient matches
        if j in ingredient1_set & ingredient2_set & ingredient3_set:
            output_dict["Complete Match"].append([j.number, j.title])
        elif j in (ingredient1_set & ingredient2_set) - ingredient3_set and ingredient_1 != ingredient_2:
            output_dict[ingredient_1 + "&" + ingredient_2].append([j.number, j.title])
        elif j in (ingredient2_set & ingredient3_set) - ingredient1_set and ingredient_2 != ingredient_3:
            output_dict[ingredient_2 + "&" + ingredient_3].append([j.number, j.title])
        elif j in (ingredient1_set & ingredient3_set) - ingredient2_set and ingredient_1 != ingredient_3:
            output_dict[ingredient_1 + "&" + ingredient_3].append([j.number, j.title])
        elif j in ingredient1_set:
            output_dict[ingredient_1].append([j.number, j.title])
        elif j in ingredient2_set:
            output_dict[ingredient_2].append([j.number, j.title])
        elif j in ingredient3_set:
            output_dict[ingredient_3].append([j.number, j.title])
        elif len(ingredient1_set | ingredient2_set | ingredient3_set) == 0:
            print ("\nSorry no recipes found that include any of your ingredients")
            return ""
    if len(ingredient1_set | ingredient2_set | ingredient3_set) == 0:
        print ("\nSorry no recipes found that include any of your ingredients")
        return ""                       

    # Print out search results, where they exist
    if len(output_dict["Complete Match"]) == 0:
        print("\nSorry no recipes found that include all your ingredients")
    else:
        print ("\nRecipes that include all your ingredients:")    
        output_dict["Complete Match"].sort()
        for k in output_dict["Complete Match"]:       
            print (k[0], ":", k[1])
    
    if ingredient_1 != ingredient_2 and len(output_dict[ingredient_1 + "&" + ingredient_2]) > 0:
        print ("\nRecipes that only include", ingredient_1, "&", ingredient_2, ":")
        output_dict[ingredient_1 + "&" + ingredient_2].sort()
        for l in output_dict[ingredient_1 + "&" + ingredient_2]:       
            print (l[0], ":", l[1])
    
    if ingredient_2 != ingredient_3 and len(output_dict[ingredient_2 + "&" + ingredient_3]) > 0:
        print ("\nRecipes that only include", ingredient_2, "&", ingredient_3, ":")
        output_dict[ingredient_2 + "&" + ingredient_3].sort()
        for m in output_dict[ingredient_2 + "&" + ingredient_3]:       
            print (m[0], ":", m[1])
    
    if ingredient_1 != ingredient_3 and len(output_dict[ingredient_1 + "&" + ingredient_3]) > 0:
        print ("\nRecipes that only include", ingredient_1, "&", ingredient_3, ":")
        output_dict[ingredient_1 + "&" + ingredient_3].sort()
        for n in output_dict[ingredient_1 + "&" + ingredient_3]:       
            print (n[0], ":", n[1])
        
    if len(output_dict[ingredient_1]) > 0:
        print ("\nRecipes that only include", ingredient_1, ":")
        output_dict[ingredient_1].sort()
        for p in output_dict[ingredient_1]:       
            print (p[0], ":", p[1])
       
    if ingredient_2 != ingredient_1 and len(output_dict[ingredient_2]) > 0:
        print ("\nRecipes that only include", ingredient_2, ":")
        output_dict[ingredient_2].sort()
        for q in output_dict[ingredient_2]:       
            print (q[0], ":", q[1])
                                        
    if ingredient_3 != ingredient_2 and len(output_dict[ingredient_3]) > 0:
        print ("\nRecipes that only include", ingredient_3, ":")
        output_dict[ingredient_3].sort()
        for r in output_dict[ingredient_3]:       
            print (r[0], ":", r[1])
    
    return ""

# Print calming words for user to wait while scrap_me scrapes recipe data from allrecipes.com and Recipe opjects are initialized
print("\nPlease wait, loading delicious recipes from the interwebs...\n")

# Initialize instances of Recipe based on recipe_dict
# Code adapted from stack overflow http://stackoverflow.com/questions/16820075/creating-multiple-class-instances-from-a-list-of-names-in-python
recipe_inst_list = [Recipe(recipe_dict[i][0],recipe_dict[i][1]) for i in range(len(recipe_dict))]
print("\nREADY!\n")
        
# Initialize instances of Ingredient based on Recipe.pure_ingredient_dict
# Code adapted from stack overflow
# http://stackoverflow.com/questions/16820075/
# creating-multiple-class-instances-from-a-list-of-names-in-python
ingredient_inst_list = [Ingredient(ingredient,Recipe.pure_ingredient_dict[ingredient][0], \
                                   Recipe.pure_ingredient_dict[ingredient][1]) \
                        for ingredient in Recipe.pure_ingredient_dict]

# Program main body
# Request input from user. Accepts up to 3 ingredients, as well as Recipe
# call-up by number. q quits the program
while True:
    print("\nEnter up to three ingredients you would like to use, separated by a space")
    user_input_ingredients = input("You may also enter a recipe number to display that recipe (q to quit):").lower().split(" ")

    if user_input_ingredients == ["q"]:
        quit()
    # This catches a numerical entry and interprests as a Recipe number
    # and displays Recipe, with option of displaying the image in a browser
    elif user_input_ingredients[0].isdigit():
        if int(re.sub('^0','', user_input_ingredients[0])) < len(Recipe.recipe_list):
            Recipe.display_recipe(Recipe.lookup_bynumber(int(re.sub('^0','', user_input_ingredients[0])))) 
            show_image = input("Would you like to see an image of this recipe in your browser? (y/yes to display):").lower()
            if show_image == "y" or show_image == "yes":
                Recipe.display_image(Recipe.lookup_bynumber(int(user_input_ingredients[0])))
            else:
                continue
        else:
            print("\nSorry, not a valid recipe number")
            continue

    # Checking number of input ingrendients are less than 4
    if len(user_input_ingredients) < 4:
        if len(user_input_ingredients) == 1:
            user_input_ingredients.append("")
            user_input_ingredients.append("")
        elif len(user_input_ingredients) == 2:
            user_input_ingredients.append("")
        print (find_recipe(user_input_ingredients))
        continue
    else:
        print("You have entered more than three ingredients or included special characters.\nPlease enter a maximum of three ingredients!\n")

print("Out of the loop")





