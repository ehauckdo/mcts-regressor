import random
  
production_rules = { "E": ["(E + E)", "(E - E)", "(E * E)", "(E ^ I)", "sin(E)", "x", "I"],
                     "I": [ 1, 2]}
 
def getRandomProductionRule(key):
    return random.choice(production_rules[key])

def expandExpressionRandomly(expr):
    #print("Expression to be expanded: "+ expr)
    indexes = list([pos for pos, char in enumerate(expr) if char == "E"])
    if len(indexes) == 0:
        return expr
    #print("indexes of Es: "+ str(indexes))
    chosen_index = random.choice(indexes)
    #print("Chosen index: " + str(chosen_index))
    chosen_production_rule = getRandomProductionRule("E")
    
    #random.choice(production_rules["E"])
    #print("Chosen production rule: "+ str(chosen_production_rule))
    new_expr = expr[:chosen_index] + str(chosen_production_rule) + expr[chosen_index + 1:]
    #print("New expression: "+new_expr)
    return new_expr

def expandExpression(expr, pr, term):
    #print("Expression to be expanded: "+ expr)
    indexes = list([pos for pos, char in enumerate(expr) if char == term])
    if len(indexes) == 0:
        return expr
    #print("indexes of Es: "+ str(indexes))
    chosen_index = random.choice(indexes)
    #print("Chosen index: " + str(chosen_index))
    chosen_production_rule = random.choice(pr[term])
    #print("Chosen production rule: "+ str(chosen_production_rule))
    new_expr = expr[:chosen_index] + str(chosen_production_rule) + expr[chosen_index + 1:]
    #print("New expression: "+new_expr)
    return new_expr

def substituteAllTerms(expr):
    expr = expr.replace("E", "I")
    index = expr.find("I")
    while index != -1:
        chosen_production_rule = getRandomProductionRule("I")
        expr = expr[:index] + str(chosen_production_rule) + expr[index + 1:]
        index = expr.find("I")

    return expr

def normalize(x, min_value, max_value):
    if min_value < max_value:
        normalized = (x - min_vaue) / (max_value - min_value)
        return normalized
    else
        return x   
 
def print_log(text, shouldPrint):
    if shouldPrint:
        print(text)
