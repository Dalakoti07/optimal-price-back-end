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

'''
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
args = parser.parse_args()
print("keyword searched :"+args.item)
'''
import asyncio
# https://stackoverflow.com/questions/44182014/python-lib-beautiful-soup-using-aiohttp
'''
async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
'''

'''
async def my_task():
    pass

def main():
    loop = asyncio.new_event_loop()
    coroutine1 = my_task()
    coroutine2 = my_task()
    task1 = loop.create_task(coroutine1)
    task2 = loop.create_task(coroutine2)
    loop.run_until_complete(asyncio.wait([task1, task2]))
    print('task1 result:', task1.result())
    print('task2 result:', task2.result())
    loop.close()

main()
'''




# from difflib import SequenceMatcher

'''
class Item:
    def __init__(self,name,tag):
        self.name=name
        self.tag=tag
    def __repr__(self):
        return "name: {} ".format(self.name)

list1=[Item("one","health"),Item("two","beauty")]
print(list1)

for i, o in enumerate(list1):
    if o.name == 'one' or o.name=='two':
        del list1[i]
        break
print(list1)
'''

'''
async def saveToDB():
    print('saving to db')
    await asyncio.sleep(2)
    print('saved to db !!!')

async def getTheResponse():
    await saveToDB()
    print("retuning value ")
    return 'value'

loop = asyncio.get_event_loop()
asyncio.ensure_future(getTheResponse())
# asyncio.ensure_future(saveToDB())
loop.run_forever()
'''
'''
async def async_foo():
    print("async_foo started")
    await asyncio.sleep(5)
    print("async_foo done")

async def main():
    asyncio.ensure_future(async_foo())  # fire and forget async_foo()
    print('Do some actions 1')
    await asyncio.sleep(5)
    print('Do some actions 2')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
'''

uniqueName={}
newList=[]
list1=['saurabh','saurabh','nitin','amit','aakash','ajay','nitin','saurabh','nikhil','nitin']
for l in list1:
    if l in uniqueName.keys():
        uniqueName[l]+=1
        newList.append(l+" ({})".format(uniqueName[l]))
    else:
        uniqueName[l]=1
        newList.append(l)

print(newList)