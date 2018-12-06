#+INCLUDE test.m
* CLASSIFY
Checks if a number is infinity or NaN.
** Syntax
```
CLASSIFY number# OUT group%
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
** Version Information
*** 3.1.0
Introduced.
** References
SmileBoom, "Additions/Changes in Ver. 3.1.0 (March 4, 2015)" [[http://smilebasic.com/en/debug/archive/]]
-----