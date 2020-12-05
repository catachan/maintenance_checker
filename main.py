from genie.testbed import load
from genie.utils.diff import Diff
import sys
import pickle

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

if __name__ == "__main__":
    
    std_ref = sys.stdout

    checks = ['static_routing','interface']
    int_state = {}
    after_state = {}
    testbed = load('sandbox.yaml')


 
    int_state = check_device(testbed)

    sys.stdout = std_ref

    selection = input("\nPress Enter to continue or y if you want to dump it to a file...")
    if selection == 'y':
        with open('data.txt', 'wb') as outfile:
            pickle.dump(int_state, outfile)
        print("Dumped to file ....")
    else:
        after_state = check_device(testbed)

        print("\n****************************************************")
        print("DELTAS:")
        print("****************************************************")
        get_diff(int_state,after_state,testbed,checks)





