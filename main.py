from genie.testbed import load
from genie.utils.diff import Diff
import sys
import pickle
import os

def check_device(testbed):

    state = {}

    for device in testbed.devices:
        try:
            print("\n****************************************************")
            print("* Connecting to device " + device + "...")
            print("****************************************************")
            sys.stdout = open('/dev/null', 'w')
            testbed.devices[device].connect()

            for check in checks:
                sys.stdout = std_ref
                print("Checking module " + check + "....")
                sys.stdout = open('/dev/null', 'w')
                state[check] = testbed.devices['csr1000v'].learn(check)

        except:
            print("Something went wrong. Please check device ip")

    return state

def get_diff(int_state,after_state,testbed,checks):

    sys.stdout = std_ref
    for device in testbed.devices:
        for module in checks:
            print("Module " + module + " delta")
            diff = Diff(int_state[module], after_state[module])
            diff.findDiff()

            for i in diff.diffs:
                print(str(i))

def func_get_arguments():
    ###########################################
    # function to get command line arguments
    ###########################################

    i=0
    # define dict to hold options / command line switches
    options={}
    options['import'] = False
    
    #parse through arguments and fill citionary with value pairs
    for argument in sys.argv:
        i=i+1
        if argument == "-i":
            options['import'] = sys.argv[i]

    return options

if __name__ == "__main__":
    
    std_ref = sys.stdout

    checks = ['static_routing']
    int_state = {}
    after_state = {}
    testbed = load('sandbox.yaml')

    #get command line arguments
    options={}
    options = func_get_arguments()

    if options['import'] ==  False:
        int_state = check_device(testbed)
        sys.stdout = std_ref
        selection = input("\nPress Enter to continue or \'d\' if you want to dump it to a file...")
        if selection == 'd':
            filename = input("Please enter export filename:")
            with open(filename, 'wb') as outfile:
                pickle.dump(int_state, outfile)
        print("Dumped to file "  + os.getcwd() + "/" + filename)
        exit()
    else:
        with open(options['import'],'rb') as importfile:
            int_state = pickle.load(importfile)

    print("\n****************************************************")
    print("* Beginning after check :")
    print("****************************************************\n")



    after_state = check_device(testbed)

    print("\n****************************************************")
    print("DELTAS:")
    print("****************************************************")
    get_diff(int_state,after_state,testbed,checks)

