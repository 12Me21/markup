#+NAVIGATION
#+TITLE
Checks if a number is infinity or NaN.
** Syntax
``` sbsyntax
SPHITRC [[id%[, high_id%], ]x#, y#, width#, height#[, mask%?, vx#, vy#]] OUT collision%
```
|=================================|
| Parameter | Description         |
| number#   | The number to check |
|=================================|
|=============================================|
| Output   | Description                      |
| `group%` |
           \ |===============================|
             | Value | Meaning               |
             |     0 | Regular number        |
             |     1 | Infinity or -infinity |
             |     2 | NaN                   |
             |===============================||
|=============================================|
** Examples
``` smilebasic
PRINT CLASSIFY(10) '0 (normal)
PRINT CLASSIFY(EXP(999)) '1 (infinity)
PRINT CLASSIFY(EXP(999)*0) '2 (nan)
```
[[EXP]]
** Version Information
*** 3.1.0
Introduced.
** References
SmileBoom, "Additions/Changes in Ver. 3.1.0 (March 4, 2015)" [[http://smilebasic.com/en/debug/archive/]]
-----
here is a cool list!
+ list item
 + another item, wow!
+ amazing, nice
 + please
  + work
+ aaa


+ now this should be a new list
hi
testing ^superscript^
x^2^