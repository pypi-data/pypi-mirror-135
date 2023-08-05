from .comment import CommentParser
from .constant import Constant


class Detector(Constant):

    @staticmethod
    def get_top_comments(lines):
        comment_parser = CommentParser()
        comments_lines = comment_parser.pick_up_comment(lines)
        comments = comment_parser.parse(comments_lines)

        return comments

    def get_type(self, line):
        if self.is_syntax_line(line):
            return 'syntax'
        if self.is_package_line(line):
            return 'package'
        if self.is_option_line(line):
            return 'option'
        if self.is_import_line(line):
            return 'import'
        if self.is_message_object(line):
            return 'message'
        if self.is_enum_object(line):
            return 'enum'
        if self.is_service_object(line):
            return 'service'
        if self.is_extend_object(line):
            return 'extend'
        if self.is_message_element(line):
            return 'message_element'
        # if self.is_extend_element(line):
        #     return 'extend_element'
        if self.is_enum_element(line):
            return 'enum_element'
        if self.is_service_element(line):
            return 'service_element'
        if self.is_oneof_object(line):
            return 'oneof'

        return 'unknown'

    @staticmethod
    def is_object_type(proto_type):
        return proto_type in ['message', 'enum', 'service', 'oneof']

    @staticmethod
    def is_syntax_line(line):
        return line.replace(' ', '').startswith('syntax=')

    @staticmethod
    def is_package_line(line):
        return line.strip().startswith('package ')

    @staticmethod
    def is_option_line(line):
        return line.strip().startswith('option ')

    @staticmethod
    def is_import_line(line):
        return line.strip().startswith('import ')

    def check_object(self, line, flag):
        if line.count(flag) == 0:
            return False

        if line.count(self.DOUBLE_SLASH) > 0 and line.index(flag) > line.index(self.DOUBLE_SLASH):
            return False

        if line.count(self.SLASH_STAR) > 0 and line.index(flag) > line.index(self.SLASH_STAR):
            return False

        return True

    def is_object_start(self, line):
        return self.check_object(line, self.LEFT_BRACE)

    def is_object_end(self, line):
        return self.check_object(line, self.RIGHT_BRACE)

    def is_message_object(self, line):
        return line.strip().startswith('message ') and line.strip().count(self.LEFT_BRACE)

    def is_extend_object(self, line):
        return line.strip().startswith('extend ') and line.strip().count(self.LEFT_BRACE)

    def is_oneof_object(self, line):
        return line.strip().startswith('oneof ') and line.strip().count(self.LEFT_BRACE)

    def is_message_element(self, line):
        if not self.is_element_line(line):
            return False

        if self.is_map_element(line):
            return True

        parts = line.strip().split(self.EQUAL_SIGN)
        parts = [e for e in parts[0].strip().split(' ')]
        parts = list(filter(None, parts))

        if parts[0] == 'rpc':  # service element
            return False

        return len(parts) >= 2

    def is_element_line(self, line):
        if line.count(self.SEMICOLON) == 0:
            return False

        if line.count(self.DOUBLE_SLASH) > 0 and line.index(self.SEMICOLON) > line.index(
                self.DOUBLE_SLASH):
            return False

        if line.count(self.SLASH_STAR) > 0 and line.index(self.SEMICOLON) > line.index(
                self.SLASH_STAR):
            return False

        if self.is_service_element(line):
            return True

        if self.is_map_element(line):
            return True

        return line.strip().count(self.SEMICOLON) > 0 and line.strip().count(self.EQUAL_SIGN) > 0

    @staticmethod
    def is_service_element(line):
        # the service element looks like:
        # rpc SeatAvailability (SeatAvailabilityRequest) returns (SeatAvailabilityResponse);
        line = line.strip()
        return line.startswith('rpc ')

    @staticmethod
    def is_map_element(line):
        # the map element looks like:
        # map<string, Project> projects = 3;
        line = line.strip().replace(' ', '')
        return line.startswith('map<')

    def is_enum_object(self, line):
        return line.strip().startswith('enum ') and line.strip().count(self.LEFT_BRACE)

    def is_enum_element(self, line):
        if not self.is_element_line(line):
            return False

        parts = line.strip().split(self.EQUAL_SIGN)
        parts = [e for e in parts[0].strip().split(' ')]
        parts = list(filter(None, parts))

        return len(parts) == 1

    def is_service_object(self, line):
        return line.strip().startswith('service ') and line.strip().count(self.LEFT_BRACE)
