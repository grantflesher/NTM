import csv

#intake csv input, and format so NTM can be ran
def csvparse(input_file):

    try:
        with open(input_file,'r') as file:
            reader = csv.reader(file)
            lines = list(reader)
        
        #header lines data
        NTM_DATA = {
            "Name"    : lines[0][0],    #name of machine
            "Q"       : lines[1],       #list of state names 
            "Σ"       : lines[2],       #list of charcters in input alphabet 
            "Γ"       : lines[3],       #list of charcters in tape alphabet
            "Start"   : lines[4][0],    #start state of the machine
            "Accept"  : lines[5],       #accept states of the machine
            "Reject"  : lines[6]        #reject states of the machine
        }

        #this adds transition lines 
        NTM_DATA["transitions"] = []

        #for each transtion line, get its info
        for row in lines[7:]:
            current_line_transition = {
                "current_state"     : row[0],
                "char"              : row[1],
                "next_state"        : row[2],
                "new_char"          : row[3],
                "left_or_right"     : row[4]
            }
            #this will append each transition time to transtions
            NTM_DATA["transitions"].append(current_line_transition)

        #reutnrs formatted data
        return NTM_DATA
    
    #deal with errors
    except FileNotFoundError:
        print(f"Error: File '{input_file}' was not found.")
        return None
    except Exception as e:
        print(f"Error: problem parsing file  {e}")
        return None

def run_NTM(ntm, input_string, max_depth):
    
    #formating info for each NTM run
    print(f"Machine Name: {ntm['Name']}")
    print(f"Input String: {input_string}")
    print(f"Max Depth: {max_depth}")

    #initialize the tree and queue to implement Breadth First Search
    initial_config = ["", ntm["Start"], input_string] #[left,current,right]
    tree = [[initial_config]]
    queue = [(initial_config, None)]  
    steps = 0
    max_steps = 100
    configurations_explored = 0
    config_parents = {} #tracks tree, so i can trace path of solution later on

    while queue and len(tree) <= max_depth:

        if steps >= max_steps:
            print(f"Error: reach maximum step limit {max_steps}")
            return None

        next_level = []
        for config, parent in queue:
            left, state, right = config

            #tacks  the parent of the current configuration
            config_parents[tuple(config)] = parent

            #if accept state, accept
            if state in ntm["Accept"]:
                print(f"String accepted in {steps} steps")
                print(f"Depth of accepting path: {len(tree) - 1}")
                print(f"Total configurations explored: {configurations_explored}")
                print("Accepting Path:")
                return trace_path(config, config_parents)

            #continues if reject state
            if state in ntm["Reject"]:
                continue

            #gets tape symbol of current position
            current_symbol = right[0] if right else "_"

            #apply transitions
            for transition in ntm["transitions"]:

                if transition["current_state"] == state and transition["char"] == current_symbol:

                    #gets new config
                    if transition["left_or_right"] == "L":

                        new_left = left[:-1] if left else "_"
                        new_right = current_symbol + right

                    elif transition["left_or_right"] == "R":

                        new_left = left + current_symbol
                        new_right = right[1:] if right else "_"

                    else:
                        new_left = left
                        new_right = right

                    new_state = transition["next_state"]
                    new_config = [new_left, new_state, new_right]

                    #adds to next level of tree 
                    next_level.append((new_config, tuple(config)))
                    configurations_explored += 1 

        #updates the  tree and queue for next level of tree
        tree.append([cfg[0] for cfg in next_level])  
        queue = next_level
        steps += 1 #this calculates the numbers of states to get to correct state

    #if it never reaches an accept, return a reject
    if len(tree) > max_depth:
        print(f"Execution stopped after max depth: {max_depth}")
    else:
        print(f"String rejected in {steps} steps")
        print(f"Depth of rejecting path: {len(tree) - 1}")
        print(f"Total configurations explored: {configurations_explored}")

    return None



def trace_path(accept_config, config_parents):
    path = []
    current_config = tuple(accept_config)

    #bachtrack the path using the  parent relationships
    while current_config is not None:
        path.insert(0, current_config)  
        current_config = config_parents.get(current_config)

    #output the path
    for config in path:
        left, state, right = config
        head_char = right[0] if right else "_"
        right_tail = right[1:] if len(right) > 1 else "_"
        print(f"Left: {left}, Current State: {state}, Current Char: {head_char}, Right: {right_tail}")

    return path


def main():
    input_file_name = input("Enter the .csv file for the NTM input file: ")
   
    NTM_DATA = csvparse(input_file_name)
    if NTM_DATA == None: return

    string_input = input("Enter the string input: ")
    try:
        max_depth = int(input("Enter the maximum depth: "))
    except ValueError:
        print("Error: Maximum depth must be an integer.")
        return

    run_NTM(NTM_DATA, string_input, int(max_depth))

if __name__ == "__main__":
    main()

    