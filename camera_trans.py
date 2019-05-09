from toppings import item, pizza_item

def camera_to_robot_pizza(pizza):

    pizza.convert()
    camera_to_robot_list(pizza.holes)

def camera_to_robot_list(item_list): #update
    for item in item_list:
        item.convert()

def toppings_converter(items_dict): #im lazy so instead of rewriting everything ill just convert from jay's item output to the one i want :P
    #update
    topping_list=[]
    hole_list=[]
    pizza={}
    for pep in items_dict['red_cirs']: #exact key might change
        topping=item(pep,'pep')
        topping_list.append(topping)
    for ham in items_dict['pink_squares']: #exact key might change
        topping=item(ham,'ham')
        topping_list.append(topping)
    for pine in items_dict['yellow_triangles']:
        topping=item(pine,'pine')
        topping_list.append(topping)
    for oli in items_dict['black_rings']:
        topping=item(oli,'olive')
        topping_list.append(topping)
    for fish in items_dict['blue_fishes']:
        topping=item(fish,'fish')
        topping_list.append(topping)
    for hole in items_dict['pizza_inners']:
        temp_hole=item(hole,'hole')
        hole_list.append(temp_hole)
    pizza=pizza_item(items_dict["pizza_outers"][0],hole_list)
    return topping_list,pizza
