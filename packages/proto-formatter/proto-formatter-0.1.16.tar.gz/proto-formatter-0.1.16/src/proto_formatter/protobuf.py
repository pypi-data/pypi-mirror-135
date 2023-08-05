from copy import deepcopy
from .proto_structures import EnumElement
from .proto_structures import ExtendElement
from .proto_structures import Extend
from .proto_structures import Import
from .proto_structures import Message
from .proto_structures import MessageElement
from .proto_structures import Option
from .proto_structures import Position
from .proto_structures import ProtoEnum
from .proto_structures import Service
from .proto_structures import ServiceElement
from .proto_structures import Oneof
from .util import to_lines


class Protobuf():
    SPACES_BETWEEN_VALUE_COMMENT = 2
    SPACES_BEFORE_AFTER_EQUAL_SIGN = 1
    SPACES_BETWEEN_NUMBER_ANNOTATION = 1
    ONE_SPACE = ' '
    TOP_COMMENT_INDENTS = ' ' * 4

    def __init__(self):
        self.syntax = None
        self.package = None
        self.options = []
        self.imports = []
        self.objects = []

        self.indents_unit = 2
        self.align_by_equal_sign = None
        self.top_comment = False
        self.flatten = False
        self.comment_max_length = None

    def to_string(self, indents=2, align_by_equal_sign=None, top_comment=False, flatten=False, comment_max_length=None):
        if flatten:
            self.flatten_objects()

        self.indents_unit = indents
        self.align_by_equal_sign = align_by_equal_sign
        self.top_comment = top_comment
        self.flatten = flatten
        self.comment_max_length = comment_max_length

        syntax_string = self.syntax_string()
        package_string = self.package_string()
        option_string = self.options_string()
        imports_string = self.imports_string()

        all_lines = []
        for object in self.objects:
            lines = []
            self.format_object_without_comment(object, lines, indents=0)
            max_length = self.get_max_length(lines)
            extra = self.get_max_lengthes(lines)
            new_lines = []
            self.format_object(object, new_lines, 0, extra)
            all_lines.append('\n'.join(new_lines))

        object_string = '\n\n'.join(all_lines)
        contents = [syntax_string, package_string, option_string, imports_string, object_string]
        contents = list(filter(None, contents))
        content = '\n\n'.join(contents)
        content = content + '\n'

        return content

    def flatten_objects(self):
        new_objects = []

        for obj in self.objects:
            new_obj = deepcopy(obj)
            new_obj.elements = []
            for element in obj.elements:
                if isinstance(element, (Message, ProtoEnum, Service)):
                    self.flatten_object(element, new_objects)
                else:
                    new_obj.elements.append(element)

            new_objects.append(new_obj)

        self.objects = new_objects

    def flatten_object(self, obj, new_objects: list):
        new_obj = deepcopy(obj)
        new_obj.elements = []

        for element in obj.elements:
            if isinstance(element, (Message, ProtoEnum, Service)):
                self.flatten_object(element, new_objects)
            else:
                new_obj.elements.append(element)

        new_objects.append(new_obj)

    def get_max_length(self, lines):
        max = 0
        for line in lines:
            if max < len(line):
                max = len(line)

        return max

    def get_max_lengthes(self, lines):
        max_equal_sign_index = 0
        max_length_of_number = 0
        max_length_of_object_line = 0
        max_length_of_service_element_line = 0
        s1 = ''
        s2 = ''
        for line in lines:
            if '=' in line:
                equa_sign_index = line.index('=')
                if max_equal_sign_index < equa_sign_index:
                    max_equal_sign_index = equa_sign_index
                    s1 = line[:equa_sign_index]

                semicolon_index = line.index(';')
                number_str = line[equa_sign_index + 1:semicolon_index].strip()
                number_length = len(number_str)
                if max_length_of_number < number_length:
                    max_length_of_number = number_length
                    s2 = number_str
            elif line.strip().startswith('rpc'):
                if max_length_of_service_element_line < len(line):
                    max_length_of_service_element_line = len(line)
            else:
                if max_length_of_object_line < len(line):
                    max_length_of_object_line = len(line)

        max_length_sample = f'{s1.rstrip()}{self.ONE_SPACE * self.SPACES_BEFORE_AFTER_EQUAL_SIGN}={self.ONE_SPACE * self.SPACES_BEFORE_AFTER_EQUAL_SIGN}{s2};'
        max_length = max(len(max_length_sample), max_length_of_service_element_line, max_length_of_object_line)

        return {
            'max_length': max_length,
            'max_equal_sign_index': max_equal_sign_index,
            'max_length_of_number': max_length_of_number,
            'max_length_of_object_line': max_length_of_object_line
        }

    def syntax_string(self):
        if not self.syntax:
            return ''

        line = f'syntax = "{self.syntax.value}";'

        return self.make_string(line, 0, self.syntax.comments, self.SPACES_BETWEEN_VALUE_COMMENT)

    def package_string(self):
        if not self.package:
            return ''

        line = f'package {self.package.value};'

        return self.make_string(line, 0, self.package.comments, self.SPACES_BETWEEN_VALUE_COMMENT)

    def options_string(self):
        if not self.options:
            return ''

        max_length = self.max_length_of_option()

        string_list = []
        for option in self.options:
            string = self.option_string(option, max_length)
            string_list.append(string)

        return '\n'.join(string_list)

    def max_length_of_option(self):
        max_length = 0
        for option in self.options:
            if option.value == 'true' or option.value == 'false':
                line = f'option {option.name} = {option.value};'
            else:
                line = f'option {option.name} = "{option.value}";'

            if max_length < len(line):
                max_length = len(line)

        return max_length

    def option_string(self, option: Option, max_length):
        if option.value == 'true' or option.value == 'false':
            line = f'option {option.name} = {option.value};'
        else:
            line = f'option {option.name} = "{option.value}";'

        space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT

        return self.make_string(line, 0, option.comments, space_between_number_comment)

    def imports_string(self):
        if not self.imports:
            return ''

        max_length = self.max_length_of_import()

        string_list = []
        for obj in self.imports:
            string = self.import_string(obj, max_length)
            string_list.append(string)

        return '\n'.join(string_list)

    def max_length_of_import(self):
        max_length = 0
        for obj in self.imports:
            line = f'import "{obj.value}";'

            if max_length < len(line):
                max_length = len(line)

        return max_length

    def import_string(self, obj: Import, max_length):
        line = f'import "{obj.value}";'
        space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT

        return self.make_string(line, 0, obj.comments, space_between_number_comment)

    @staticmethod
    def get_object_keyword(obj):
        if isinstance(obj, Message):
            return 'message'
        if isinstance(obj, ProtoEnum):
            return 'enum'
        if isinstance(obj, Service):
            return 'service'
        if isinstance(obj, Extend):
            return 'extend'
        if isinstance(obj, Oneof):
            return 'oneof'

    def create_object_header(self, obj, indents, no_comment, max_length):
        obj_keyword = self.get_object_keyword(obj)
        line = f'{obj_keyword} {obj.name} ' + "{"

        space_between_number_comment = 2
        if max_length:
            space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def get_object_element_class(self, obj):
        classes = {
            'message': MessageElement,
            'enum': EnumElement,
            'service': ServiceElement,
            'extend': MessageElement,
            'oneof': MessageElement
        }
        return classes[self.get_object_keyword(obj)]

    def get_make_object_element_string_method(self, obj):
        methods = {
            'message': self.message_element_string,
            'enum': self.enum_element_string,
            'service': self.service_element_string,
            'extend': self.extend_element_string,
            'oneof': self.message_element_string
        }
        return methods[self.get_object_keyword(obj)]

    def format_object(self, obj, string_list, indents, extra):
        max_length = extra['max_length']
        max_equal_sign_index = extra['max_equal_sign_index']
        max_length_of_number = extra['max_length_of_number']
        max_length_of_object_line = extra['max_length_of_object_line']

        message_header = self.create_object_header(obj, indents, False, max_length - indents)
        string_list.append(message_header)
        element_class = self.get_object_element_class(obj)
        element_str_method = self.get_make_object_element_string_method(obj)

        for element in obj.elements:
            if isinstance(element, element_class):
                line = element_str_method(
                    element,
                    indents + self.indents_unit,
                    True,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BETWEEN_VALUE_COMMENT
                )

                if self.align_by_equal_sign:
                    line_without_number = line.split('=')[0].rstrip()
                    space_between_name_equal_sign = max_equal_sign_index - len(line_without_number)

                    if hasattr(element, 'number'):
                        space_between_number_comment = max_length - max_equal_sign_index - len('=') - len(';') - len(
                            element.number) - len(
                            element.annotation) - self.SPACES_BEFORE_AFTER_EQUAL_SIGN - self.SPACES_BETWEEN_NUMBER_ANNOTATION + self.SPACES_BETWEEN_VALUE_COMMENT

                        if element.annotation == '':
                            # the space between number and rules is tripped, so shouldn't count it
                            space_between_number_comment = space_between_number_comment + self.SPACES_BETWEEN_NUMBER_ANNOTATION

                    elif line.strip().startswith('rpc'):
                        space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT
                    else:
                        space_between_number_comment = max_length - len(
                            line) - self.SPACES_BEFORE_AFTER_EQUAL_SIGN + self.SPACES_BETWEEN_VALUE_COMMENT

                    string = element_str_method(
                        element,
                        indents + self.indents_unit,
                        False,
                        space_between_name_equal_sign,
                        self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        space_between_number_comment
                    )
                else:
                    space_between_number_comment = max_length - len(line) + self.SPACES_BETWEEN_VALUE_COMMENT
                    string = element_str_method(
                        element,
                        indents + self.indents_unit,
                        False,
                        self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                        space_between_number_comment
                    )

                string_list.append(string)
            else:
                self.format_object(element, string_list, indents + self.indents_unit, extra)

        message_rear = self.make_string('}', indents, [], self.SPACES_BETWEEN_VALUE_COMMENT)
        string_list.append(message_rear)

    def format_object_without_comment(self, obj, string_list, indents):
        message_header = self.create_object_header(obj, no_comment=True, indents=indents, max_length=None)
        string_list.append(message_header)
        element_class = self.get_object_element_class(obj)
        element_str_method = self.get_make_object_element_string_method(obj)

        for element in obj.elements:
            if isinstance(element, element_class):
                string = element_str_method(
                    element,
                    indents + self.indents_unit,
                    True,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BEFORE_AFTER_EQUAL_SIGN,
                    self.SPACES_BETWEEN_VALUE_COMMENT
                )
                string_list.append(string)
            else:
                self.format_object_without_comment(element, string_list, indents=indents + self.indents_unit)

        message_rear = self.make_indented_line('}', indents=indents)
        string_list.append(message_rear)

    def message_element_string(
            self,
            obj: MessageElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        line = f'{obj.label} {obj.type} {obj.name}{self.ONE_SPACE * space_between_name_equal_sign}={self.ONE_SPACE * space_between_equal_sign_number}{obj.number}{self.ONE_SPACE * self.SPACES_BETWEEN_NUMBER_ANNOTATION}{obj.annotation}'
        line = line.strip()  # remove prefix space when obj.label is empty string or rules is empty.
        line = f'{line};'

        if no_comment:
            return self.make_indented_line(line, indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def extend_element_string(
            self,
            obj: ExtendElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        # using the message element making string
        return self.message_element_string(obj,
                                           indents,
                                           no_comment,
                                           space_between_name_equal_sign,
                                           space_between_equal_sign_number,
                                           space_between_number_comment)

    def enum_element_string(
            self,
            obj: EnumElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        line = f'{obj.name}{self.ONE_SPACE * space_between_name_equal_sign}={self.ONE_SPACE * space_between_equal_sign_number}{obj.number}{self.ONE_SPACE * self.SPACES_BETWEEN_NUMBER_ANNOTATION}{obj.annotation}'
        line = line.strip()  # remove prefix space when rules is empty.
        line = f'{line};'

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def service_element_string(
            self,
            obj: ServiceElement,
            indents,
            no_comment,
            space_between_name_equal_sign,
            space_between_equal_sign_number,
            space_between_number_comment
    ):
        # rpc SeatAvailability (SeatAvailabilityRequest) returns (SeatAvailabilityResponse);
        line = f'{obj.label} {obj.name} ({obj.request}) returns ({obj.response});'

        if no_comment:
            return self.make_indented_line(line, indents=indents)
        else:
            return self.make_string(line, indents, obj.comments, space_between_number_comment)

    def make_string(self, value_line, indents, comments, space_between_number_comment):
        top_comment_lines = []
        right_comment = ''
        if self.top_comment:
            for comment in comments:
                if comment.position == Position.TOP:
                    text_lines = [l.strip() for l in comment.text.split('\n')]

                    new_text_lines = []
                    if self.comment_max_length is not None:
                        for l in text_lines:
                            new_text_lines.extend(to_lines(l, self.comment_max_length))
                        text_lines = new_text_lines

                    top_comment_lines.extend(text_lines)
                if comment.position == Position.Right:
                    line = comment.text
                    text_lines = [line]

                    new_text_lines = []
                    if self.comment_max_length is not None:
                        for l in text_lines:
                            new_text_lines.extend(to_lines(l, self.comment_max_length))

                    if self.comment_max_length is not None:
                        top_comment_lines.extend(new_text_lines)
                    else:
                        top_comment_lines.extend(text_lines)

                    right_comment = ''
        else:
            for comment in comments:
                if comment.position == Position.TOP:
                    text_lines = [l.strip() for l in comment.text.split('\n')]

                    new_text_lines = []
                    if self.comment_max_length is not None:
                        for l in text_lines:
                            new_text_lines.extend(to_lines(l, self.comment_max_length))
                        text_lines = new_text_lines

                    top_comment_lines.extend(text_lines)
                if comment.position == Position.Right:
                    right_comment = comment.text

        indented_top_comment_lines = []
        if top_comment_lines:
            for comment_line in top_comment_lines:
                indented_top_comment_lines.append(f'**{self.TOP_COMMENT_INDENTS}{comment_line}')
            indented_top_comment_lines.insert(0, '/*')
            indented_top_comment_lines.append('*/')

        lines = indented_top_comment_lines
        if right_comment:
            line = f'{value_line}{self.ONE_SPACE * space_between_number_comment}// {right_comment}'
            lines.append(line)
        else:
            lines.append(value_line)

        indented_lines = [f'{self.ONE_SPACE * indents}{line}' for line in lines]
        string = '\n'.join(indented_lines)
        return string

    def make_indented_line(self, line, indents=0):
        return f'{self.ONE_SPACE * indents}{line}'
