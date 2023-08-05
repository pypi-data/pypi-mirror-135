import os
import ntpath

from .parser import ProtoParser


def format_file(fp, indents=2, top_comment=False, align_by_equal_sign=False, flatten=False, comment_max_length=None,
                new_fp=None):
    """
    Format protobuf file, override the original file if no new file path(new_fp) specified
    or write the formatted result to a new file.
    :param fp: unformatted protobuf file path.
    :param indents: indents number.
    :param top_comment: convert the single line comment at the left of code as a top comment or not. Default: not
    :param align_by_equal_sign: if align the code by equal sign or not.
    Example of align:
        ENUM_TYPE_UNSPECIFIED = 0;  // ENUM_TYPE_UNSPECIFIED
        ENUM_TYPE_CARRY_A     = 1;  // ENUM_TYPE_CARRY_A
        ENUM_TYPE_B           = 2;  // ENUM_TYPE_B
    :param flatten: if flatten nested object or not.
    Example of flatten:
      Original file:
         message Outer {
           int32 outerq = 1;
           message MiddleAA {
             message Inner {
               int64 ival = 1;
               bool  booly = 2;
             }
             bool  booly_aa = 1;
           }
         }

      Formatted file:
         message Inner {
             int64 ival = 1;
             bool booly = 2;
         }

         message MiddleAA {
             bool booly_aa = 1;
         }

         message Outer {
             int32 outerq = 1;
         }
    :param comment_max_length: the max length of comment line, defalut is no limitation.
    :param new_fp: the file path of new formatted protobuf file. Rewrite the original file if it is not specified.
    :return: file content size.
    """
    proto_parser = ProtoParser()
    protobuf_obj = proto_parser.load(fp=fp)
    content = protobuf_obj.to_string(
        indents=indents,
        top_comment=top_comment,
        align_by_equal_sign=align_by_equal_sign,
        flatten=flatten,
        comment_max_length=comment_max_length
    )

    if new_fp:
        fp = new_fp
        if not os.path.exists(new_fp):
            path, tail = ntpath.split(new_fp)
            if not os.path.exists(path):
                os.makedirs(path)

    with open(fp, 'w') as f:
        return f.write(content)


def format_str(proto_str, indents=2, top_comment=False, align_by_equal_sign=False, flatten=False,
               comment_max_length=None):
    """
    Format a protobuf string, return the formatted string.
    :param proto_str: protobuf string need to be formatted.
    :param indents: indents number.
    :param top_comment: convert the single line comment at the left of code as a top comment or not. Default: not
    :param align_by_equal_sign: if align the code by equal sign or not.
    Example of align:
        ENUM_TYPE_UNSPECIFIED = 0;  // ENUM_TYPE_UNSPECIFIED
        ENUM_TYPE_CARRY_A     = 1;  // ENUM_TYPE_CARRY_A
        ENUM_TYPE_B           = 2;  // ENUM_TYPE_B
    :param flatten: if flatten nested object or not.
    Example of flatten:
      Original file:
         message Outer {
           int32 outerq = 1;
           message MiddleAA {
             message Inner {
               int64 ival = 1;
               bool  booly = 2;
             }
             bool  booly_aa = 1;
           }
         }

      Formatted file:
         message Inner {
             int64 ival = 1;
             bool booly = 2;
         }

         message MiddleAA {
             bool booly_aa = 1;
         }

         message Outer {
             int32 outerq = 1;
         }
    :param comment_max_length: the max length of comment line, defalut is no limitation.
    :return: formatted string.
    """
    proto_parser = ProtoParser()
    protobuf_obj = proto_parser.loads(proto_str=proto_str.strip())
    content = protobuf_obj.to_string(
        indents=indents,
        top_comment=top_comment,
        align_by_equal_sign=align_by_equal_sign,
        flatten=flatten,
        comment_max_length=comment_max_length
    )

    return content
