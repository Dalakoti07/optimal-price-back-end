import time

'''
def nextSquare():
    i = 1
    time.sleep(1)
    # An Infinite loop to generate squares  
    while True:
        time.sleep(1)
        yield i*i                 
        i += 1  # Next execution resumes  
                # from this point      
  
# Driver code to test above generator  
# function
i=0 
for num in nextSquare():    
    i+=1
    if i==20:
        break
    print(num)

string="i am white "
print(string.split('(')[0])

'''

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
args = parser.parse_args()
print("keyword searched :"+args.item)