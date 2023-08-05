# proto-formatter
Protocol Buffers file formatter.

## Install
```shell
pip install proto-formatter
```
## Usage
Format all proto files under current folder and sub-folders with default configs
```shell
proto_formatter format
```
Help message
```shell
****************************************************************************************************
*                         Format protobuf file(s) from a specific target.                          *
*                                           MIT License                                            *
****************************************************************************************************
usage:
  proto_formatter <command> [options]

commands:
  format                       format protobuf files
  view                         view file

general options:
  -h                           show this help message and exit
  --help                       show this help message and exit
  --files                      target protobuf files need to be formatted.
  --folder                     target directory, default is current directory, all protobuf files
                               under it including all subdirectories will be formatted.
  --indents                    the number of indented spaces, default is 4
  --top-comment                format all comments as top comments(above the target line), default
                               is False
  --align-by-equal-sign        align the code by equal sign: True or False, default is True
  --flatten                    flatten nested objects, default is False
  --comment-max-length         the max length of comment line, default is 999999.
  --file                       target protobuf file, only used for command 'view'
```
It also provides a method ``format_str`` to format a protobuf string.
```python
from proto_formatter import format_str

proto_str = """
    /*
    Person balabala
*/
    message Person {
    // comment of name a
required string name = 1; // comment of name b
/* 
comment of id a
// comment of id b
         */
        required int32 id = 2;// comment of id c
       optional string email = 3;// comment of email
}
"""
formatted_proto_str = format_str(proto_str)
print(formatted_proto_str)
```
The formatted_proto_str is:
```protobuf
/*
**    Person balabala
*/
message Person {
  /*
  **    comment of name a
  */
  required string name = 1;   // comment of name b
  /*
  **    comment of id a
  **    comment of id b
  */
  required int32 id = 2;      // comment of id c
  optional string email = 3;  // comment of email
}
```