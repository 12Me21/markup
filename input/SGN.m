#+NAVIGATION
#+TITLE
Returns the sign of a number (-1, 0, or 1).
** Syntax
``` sbsyntax
SGN number# OUT sign%
```
|=|
| parameter | description |
| number#   | The number to get the sign of |
|=|
|=|
| output | description |
| sign%  | The sign of number# (-1, 0, or 1) |
|=|
|=|
| numbers   | sign |
| positive  | 1    |
| negative  | -1   |
| 0         | 0    |
| -0        | 0    |
| infinity  | 1    |
| -infinity | -1   |
| NaN       | 1    |
|=|
** Examples
``` smilebasic
PRINT SGN(10) '1
PRINT SGN(-EXP(999)) '-1
```
-----
#+NAVIGATION
