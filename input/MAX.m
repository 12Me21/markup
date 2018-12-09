#+NAVIGATION
#+TITLE
Finds the largest number in a list of numbers or an array
** Syntax
``` sbsyntax
MAX number_1, number_2 [, ...] OUT maximum
MAX array[] OUT maximum
```
|=|
|Parameter|Description|
|`number_1`, `number_2`, ...|List of numbers to find the maximum of. Must have at least 2 items|
|`array[]`|Number array to find the maximum of. Must have at least 1 item|
|Output|Description|
|`maximum`|The maximum of the list/array. Will always be a float, unless you passed an integer array or 2 integers. If the maximum value occurs multiple times in the list, MAX returns the first occurrence.|
|=|
** Examples
|===========|
|Code|Output|
|
``` smilebasic
PRINT MAX(7,4,8)
```
|
``` sbconsole
8
```
||
``` smilebasic
DIM A[3]
A[0]=7
A[1]=4
A[2]=8
PRINT MAX(A)
```
|
``` sbconsole
8
```
||=|
** Possible Errors
|=|| Error | Cause |
| `Type mismatch` |
+ The list of numbers has fewer than 2 items
+ There are non-number values in the list
+ A string array was used
|
| `Illegal function call` |
+ 0 arguments were passed
+ The number of outputs was not 1
+ An array with a length of 0 was used
||=|
** Version Information
*** 3.3.2
No longer allows arrays with 0 elements
** References
SmileBoom "Bug Fixes in Ver. 3.3.2 (August 10, 2016)" [[http://smilebasic.com/en/debug/archive/]]
-----
#+NAVIGATION