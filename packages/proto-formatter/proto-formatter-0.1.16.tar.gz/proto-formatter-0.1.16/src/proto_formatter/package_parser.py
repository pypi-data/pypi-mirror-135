from .comment import CommentParser
from .proto_structures import Package
from .protobuf import Protobuf


class PackageParser():

    @classmethod
    def parse_and_add(cls, proto_obj: Protobuf, line, top_comment_list):
        if proto_obj.package is not None:
            raise Exception('multiple package detected!')

        proto_obj.package = cls.parse_package(line, top_comment_list)

    @classmethod
    def parse_package(cls, line, top_comment_list):
        value = cls._get_package_value(line)
        comments = CommentParser.create_comment(line, top_comment_list)
        package = Package(value, comments)
        return package

    @classmethod
    def _get_package_value(cls, line):
        line = line.strip()
        lindex = len('package ')
        rindex = line.index(';')
        value = line[lindex:rindex].strip()
        return value
