import json
str_j = '''{ 
        "name": "High Protein Starter",
        "ingredients": {
            "Salt": "2 tsp",
            "Sugar": "1 tsp",
            "Soya Chaap": "3 pieces",
            "Mashroon": "50g",
            "Rajma": "1 cup"
        },
        "instructions": "1. Heat up some oil in a pan.
                       2. Add Soya Chaap and sauté for 2 minutes.
                       3. Add rajma, mashroon, salt and sugar and cook for 10 minutes or until the rajma is well 
cooked.
                       4. Serve hot.",
        "nutritional_details": {
            "Protein": "9g",
            "Total Fat": "2g",
            "Carbs": "13g",
            "Fiber": "2g"
        }
    }'''  
print(type(str_j))
json_string = json.loads(str_j)
print(json_string["name"]["Ingredients"])
print(type(json_string)) 