TODO List
---------

## Formatting the output

* Quoted and non-quoted entries are supported. 
* Double-quote is the quoting character. 
* Entries with whitespace must be quoted. 
* Double-quote and backslash characters inside quoted entry must be escaped with a backslash. 
* Escaping is not supported in non-quoted entries. 
* Linefeed escape sequences (\n) are supported in quoted strings. 
* Linefeed escape sequences are trimmed from the end of an entry. 


## Send using timestamps?
Each line of the input file must contain 4 whitespace delimited entries: <hostname> <key> <timestamp> <value>. 
Timestamp should be specified in Unix timestamp format.
