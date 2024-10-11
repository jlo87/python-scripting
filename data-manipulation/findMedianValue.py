#The list of digits. 
nums = [1, 2, 3, 4] 
 
#Sort the list from smallest to largest. 
nums.sort() 
 
#Find the median. 
length = len(nums) 
if (length % 2 == 0): 
    median = (nums[(length)//2] + nums[(length)//2-1]) / 2 
else: 
    median = nums[(length-1)//2] 
 
#Display the result. 
print(median) 


# Using statistics module
import statistics 
 
data = [1, 3, 3, 6, 7, 8, 9] 
median = statistics.median(data) 
print("Median:", median) 


# Using NumPy
import numpy as np 
 
data = [1, 3, 3, 6, 7, 8, 9] 
median = np.median(data) 
print("Median:", median) 


# Using pandas
import pandas as pd 
 
data = [1, 3, 3, 6, 7, 8, 9] 
median = pd.Series(data).median() 
print("Median:", median) 