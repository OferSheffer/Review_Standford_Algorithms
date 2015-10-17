'''
Created on Oct 14, 2015
@author: Ofer

Question 1
Download the text file here. (Right click and save link as) 
http://spark-public.s3.amazonaws.com/algo1/programming_prob/IntegerArray.txt

This file contains all of the 100,000 integers between 1 and 100,000 (inclusive)
 in some order, with no integer repeated. Your task is to compute the number of 
 inversions in the file given, where the ith row of the file indicates the ith 
 entry of an array. Because of the large size of this array, you should 
 implement the fast divide-and-conquer algorithm covered in the video lectures.
'''

'''
Educational Notes:
 Concatenating immutable sequences always results in a new object. This means
 that building up a sequence by repeated concatenation will have a quadratic
 runtime cost in the total sequence length - e.g. like the question about
 repeated merge-sorts on k sequences of length n. To get a linear runtime 
 cost see:  https://docs.python.org/3/library/stdtypes.html
 
Python TimeComplexity: 
 https://wiki.python.org/moin/TimeComplexity

 list - insert is a terrible idea. O(n)
 set item - good idea. O(1)
'''

#TODO: if debug import unittest
import unittest
import sys


def Merge_and_CountSplitInv(A,start_index,len_1st,len_2nd):
    """
    Merges two similar length pre-sorted sub-slices of array A while counting
    inversions.
    
    Input: 
    array A, start_index (location of first sub-slice)
    len_1st,len_2nd (subslice_lengths).
    Output: inversions (values where i<j, but A[i]>A[j])
    Side Effect: two consecutive A subsections are sorted.
    """
    inversions=0
    temp_array=[]
    index_1st=start_index
    index_2nd=start_index+len_1st

    #while both indices are in range
    while ((index_1st < start_index+len_1st) and
          (index_2nd < start_index+len_1st+len_2nd)):
        
        #place smaller value in temp_array, increase inversions 
        if A[index_1st]<=A[index_2nd]:
            temp_array.append(A[index_1st])
            index_1st += 1
        else:
            temp_array.append(A[index_2nd])
            index_2nd += 1
            inversions+=(start_index+len_1st-index_1st)
    
    #one index is out of range:
    if index_2nd == start_index+len_1st+len_2nd: # 2nd index complete
        #add leftover 1st half values to temp_array
        #before destroying them by the write process.
        temp_array.extend(A[index_1st:start_index+len_1st])
    else: # 1st index complete
        pass #no need to write over leftovers in 2nd sub-array
         
    #write temp_array over A[start_index:start_index+len(temp_array)]
    write_index=start_index
    for value in temp_array:
        A[write_index]=value
        write_index +=1
    
    return inversions
    
        
def Sort_and_Count(A, n, start_index=0):
    """
    Input: array A, length n, start_index(default=0)
    Output: inversions (values where i<j, but A[i]>A[j])
    Side Effect: A is sorted.
    """
    if n==1:
        return 0    # base case, array of length 1
    else:
        # Input: 1st and 2nd halves of current sub-array
        len_1st=n//2
        len_2nd=n//2+n%2
        x=Sort_and_Count(A, len_1st, start_index)           
        y=Sort_and_Count(A, len_2nd, start_index+len_1st)
        # merge the (newly sorted) half-sized sub-arrays
        z=Merge_and_CountSplitInv(A,start_index,len_1st,len_2nd)
    return x+y+z

class TestSort_and_Count(unittest.TestCase):
    """
    Basic test class
    """

    def test_Sort_and_Count(self):
        A=[1]
        res1 = Sort_and_Count(A,len(A))  # single element
        self.assertEqual(res1, 0)
        B=[1,3,5,2,4,6]
        res2 = Sort_and_Count(B,len(B))  # even length
        self.assertEqual(res2, 3)
        C=[1,3,5,2,4,6,3]
        res3 = Sort_and_Count(C,len(C))  # odd length, duplicate value
        self.assertEqual(res3, 6)


def main(file_name):
    #TODO: take values from file and run sort_and_count
    with open(file_name) as fh:
#         if _debug:
#             fh.readline()  # get rid of first answer line from debug file
        A = [map(int, [line.strip() for line in fh])]
        print(Sort_and_Count(A,len(A)))
    
    
if __name__ == '__main__':
    
    #TODO: working with argv to accept file input
    if len(sys.argv) > 2:
        sys.exit("Usage: inv_count <file_name> (leave empty for testing)")
    if len(sys.argv) == 1:
        print("No filename input, testing...")
        unittest.main()
    # else: argv == 2
    main(sys.argv[1])
    
    
    