import importlib.util as iu
import os
import sys

#this method only works from python 3.5 and above
def module_from_file(module_name, file_path):
    spec=iu.spec_from_file_location(module_name, file_path)
    module=iu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

filePath=os.path.abspath('../Phase1/lex.py')
directory=os.path.dirname(filePath)
#lex = module_from_file('lex',filePath) #FIRST Method (comment out this line to test the SECOND Method)

#Second Method
#IMPORTANT: Add __init__.py (empty) file to the directory where your importing file exists.
#append to search the parent directory obtained below last. Use sys.path.insert(0,<parent_dir_path>) to search for the path first.
#Comment out the line below to test the FIRST Method
sys.path.append(os.path.split(directory)[0]) #os.path.split(directory) output: ('/Users/david/Documents/CS304_Compiler_Design/Assignments/Project', 'Phase1')

'''
os.path.split(<path>)
Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that.
The tail part will never contain a slash; if path ends in a slash, tail will be empty.
If there is no slash in path, head will be empty. If path is empty, both head and tail are empty.
Trailing slashes are stripped from head unless it is the root (one or more slashes only).
'''

from Phase1 import lex

if __name__ == '__main__':
    print(f"--- Running getNextToken from {sys.argv[0]} ---")
    token=lex.getNextToken()
    token.printTokenInfo()
