#one or both below variables must be True
use_naive_solution = False 
use_constant_result = True

#implement this function, and set use_naive_solution True
# if you want use naive solution for your expected output
def naive_solution():
    return None


#format: [
    # [arguments], 
    # expected constant result,
    # use naive solution? True/False, 
    # use constant result? True/False 
    # ]
    
args_results = [
    [
        [], #arguments
        "result", #expected result
        True, #set/add False in third elements for exception not judging the naive_solution
        True, #set/add False in third fourth for exception not judging the naive_solution
    ],
    [
        [], #arguments
        "result", #expected result
        True, #set/add False in third elements for exception not judging the naive_solution
        True, #set/add False in third fourth for exception not judging the naive_solution       
    ],
    [
        [], #arguments
        "result", #expected result
        True, #set/add False in third elements for exception not judging the naive_solution
        True, #set/add False in third fourth for exception not judging the naive_solution       
    ],        
]

if __name__ ==  "__main__":
    print(naive_solution())