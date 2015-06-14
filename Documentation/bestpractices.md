#The Prime Directive
Do not work from an original file. Always work from a copy of the original file.

#The Other Prime Directive
The structure of the data is what turns gibberish into information. Protect the 
structure of the information and verify that it is intact after any change.

#The final Prime Directive
When automating anything it becomes easy to accidentally drop data that does not
meet your expectations. Ensure that you have not done this by either very careful
use of these tools or by reverting the final needed output back to the original file
and diffing the files.


# Other stuff

If you are not 100% sure that every line in a file will meet your formatting 
expectations (Basically anytime you are dealing with files from an unknown
origin ) and it is very large, use the file splitter tool to take off the first
X number of lines and test on those before testing on the large file.  This will
allow you to attempt to find any likely issues before waiting the time it takes
to process the whole file. 

