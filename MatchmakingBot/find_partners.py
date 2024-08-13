from first_algorithm import first_algorithm
from second_algorithm import second_algorithm
from third_algorithm import third_algorithm

async def find_gaming_partners(user_id):
    #First algorithm    
    first_algorithm_results = await first_algorithm(user_id) # Call the first algorithm
    if first_algorithm_results: # If the first algorithm found possible gaming partners
        first_algorithm_results_string = f"Your possible gaming partners (1st algorithm) are: {first_algorithm_results}."
    else: # If the first algorithm did not find possible gaming partners
        first_algorithm_results_string = "The 1st algorithm was not able to find you any gaming partners."

    #Second algorithm
    second_algorithm_results = await second_algorithm(user_id) # Call the second algorithm
    if (second_algorithm_results): # If the second algorithm found possible gaming partners
        second_algorithm_results_string = f"Your possible gaming partners (2nd algorithm) are: {second_algorithm_results}."
    else: # If the second algorithm did not find possible gaming partners
        second_algorithm_results_string = "The 2nd algorithm was not able to find you any gaming partners."
    
    #Third algorithm
    third_algorithm_results = await third_algorithm(user_id) # Call the third algorithm
    if third_algorithm_results: # If the third algorithm found possible gaming partners
        third_algorithm_results_string = f"Your possible gaming partners (3rd algorithm) are: {third_algorithm_results}."
    else: # If the third algorithm did not find possible gaming partners
        third_algorithm_results_string = "The 3rd algorithm was not able to find you any gaming partners."
    
    return [first_algorithm_results_string, second_algorithm_results_string, third_algorithm_results_string]