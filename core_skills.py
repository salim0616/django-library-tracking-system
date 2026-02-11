import random
rand_list = [random.randint(1,20) for i in range(10)]
print(rand_list)

list_comprehension_below_10 = [j for j in rand_list if j<10]
print(list_comprehension_below_10)

list_comprehension_below_10_using_filter = list(filter(lambda x:x<10,rand_list))
print(list_comprehension_below_10_using_filter)

