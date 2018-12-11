** Links
|====|
|Input|Output|
|`[[www.example.com]]`|[[www.example.com]]|
|`[[http://kland.smilebasicsource.com/i/ezmls.jpeg]]`|[[http://kland.smilebasicsource.com/i/ezmls.jpeg]]|
|`[[PRINT]]`|[[PRINT]] (Link to documentation page)|
|`[[www.example.com][text]]`|[[www.example.com][text]]|
|=|

Images are inserted if the url ends in `.png`, `.jpeg`, `.jpg`, `.bmp`, or `.gif` (not case sensitive)
For image urls that don't end in the file extension, you can use `#.png` (or something) at the end of the url to trick the parser without affecting the url
If the "url" is the name of a page, a link to that page is inserted, with the text being the page's title

** Lists
...

** Tables
`|===||` - Start table (any number of `=` are allowed) (whitespace is allowed between `||`)
`|` - Next cell
`||` - Next row (whitespace is allowed between `||`) Only works if the right number of cells have been used in the current row.
`||===|` - End table (any number of `=` are allowed) (whitespace is allowed between `||`)
Typical usage:
```
|=================|
|header 1|header 2|
| 12345  | abcdef |
|=================|
```
|=================|
|header 1|header 2|
| 12345  | abcdef |
|=================|

** Styling
|===========================|
|    Input    |   Output    |
|  `*bold*`   |   *bold*    |
| `/italic/`  |  /italic/   |
|`_underline_`| _underline_ |
| ` ``code``` |   `code`    |
|===========================|
In inline code, ` ``` can be inserted as ` `````.
If you need ` ``` as the first character in a code block, put a space before it.
` `` ````...``` -> ` ``...`

** Headings
Must be at the start of a line
|================|
| Input | Output |
| `* Heading 1` |
* Heading 1
|| `** Heading 2` |
** Heading 2
|| `----` |
-----
|
|================|

** Escaping
Any character can be escaped with `\` (outside of code blocks, the url part of a link, and a few other specific situations.)
This will insert that character directly into the output without it being parsed
`\\` -> \\
`\``` -> \`

** Comments
`# comment` (must begin at the start of a line)

** Commands
`#+NAVIGATION` - insert navigation links
`#+TITLE` - insert page title
`#+PAGES` - insert a list of links to pages in the category (only allowed on category pages)

** Code block
` ``​```` language
contents
````​``
`
|=|
|Language|Description|
|`smilebasic`|SmileBASIC
``` smilebasic
READ VAR("A")[0]
```
|
|`sbconsole`|SmileBASIC DIRECT mode
``` sbconsole
SmileBASIC for Nintendo 3DS ver 3.5.2
(C)2011-2017 SmileBoom Co.Ltd.
8318972 bytes free

OK
```
|
|`sbsyntax`|SmileBASIC function syntax
``` sbsyntax
COLOR text_color% [, background_color%]
```
|
|(none)|No highlighting
```
unhighlighted code
```
|
|=|