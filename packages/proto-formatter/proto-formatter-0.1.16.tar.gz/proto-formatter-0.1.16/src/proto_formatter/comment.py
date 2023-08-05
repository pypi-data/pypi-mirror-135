from .proto_structures import Comment
from .constant import Constant
from .proto_structures import Position
from .util import remove_prefix, remove_suffix


class CommentParser(Constant):
    def __init__(self):
        self.end_line = 0

        self.multiple_comment_start_symbol_stack = []
        self.multiple_comment_end_symbol_stack = []

    def pick_up_comment(self, lines):
        comment_lines = []
        while lines:
            line = lines.pop(0).strip()
            # comment case: /* I'am a comment */
            if self._start_with_multiple_line_comment(line) and self._end_with_multiple_line_comment(line):
                comment_lines.append(line)
                continue

            if self._start_with_multiple_line_comment(line):
                self.multiple_comment_start_symbol_stack.append(self.SLASH_STAR)
                comment_lines.append(line)
                continue

            if self.is_comment(line):
                comment_lines.append(line)

            if self._end_with_multiple_line_comment(line):
                self.multiple_comment_end_symbol_stack.append(self.STAR_SLASH)
                continue

            if line and not self.is_comment(line):
                lines.insert(0, line)  # add back
                break

        return comment_lines

    @staticmethod
    def is_not_new_line(variable):
        return variable != '\n'

    def parse(self, comment_lines):
        comment_lines = self.remove_prefix_symble(comment_lines)

        comment_lines = list(filter(None, comment_lines))
        comment_lines = list(filter(self.is_not_new_line, comment_lines))

        return comment_lines

    def remove_prefix_symble(self, comment_lines):
        processed_lines = []
        for line in comment_lines:
            if line.strip().startswith(self.DOUBLE_SLASH):
                # remove the single comment symble if have, E.g. // I'am a comment
                processed_lines.append(line.strip()[2:].strip())
            elif self._start_with_multiple_line_comment(line) or self._end_with_multiple_line_comment(line):
                # remove the multiple comment symble if have, E.g. /* I'am a comment */
                processed_lines.append(line.strip().replace(self.SLASH_STAR, "").replace(self.STAR_SLASH, ''))
            elif (line.strip().startswith(self.STAR) or line.strip().startswith(
                    self.STAR * 2)) and not self._end_with_multiple_line_comment(line):
                # remove the multiple comment symble if have, E.g. * I'am a comment in multiple line comment
                # Example:
                # /*
                # **    Device information, including user agent, device proto_type and ip address.
                # */
                #
                processed_lines.append(line.strip().replace(self.STAR, ""))
            else:
                processed_lines.append(line.strip())

        return processed_lines

    def _start_with_single_line_comment(self, line):
        return line.strip().startswith(self.DOUBLE_SLASH)

    def _start_with_multiple_line_comment(self, line):
        return line.strip().startswith(self.SLASH_STAR)

    def _end_with_multiple_line_comment(self, line):
        return line.strip().endswith(self.STAR_SLASH)

    def _is_multiple_comment(self):
        if len(self.multiple_comment_start_symbol_stack) == 0:
            return False

        return len(self.multiple_comment_start_symbol_stack) > len(self.multiple_comment_end_symbol_stack)

    def is_comment(self, line):
        if self._is_multiple_comment():
            return True

        if self._start_with_single_line_comment(line):
            return True

        return False

    @staticmethod
    def parse_single_line_comment(line):
        comment = None
        if line.count(CommentParser.DOUBLE_SLASH) > 0:
            start_index = line.index(CommentParser.DOUBLE_SLASH)
            comment_str = line[start_index:].lstrip(CommentParser.DOUBLE_SLASH).strip()
            comment = Comment(comment_str, Position.Right)
        return comment

    @staticmethod
    def create_top_comments(comments):
        result = []
        while comments:
            comment_lines = comments.pop(0)
            text = ''.join(comment_lines)
            text = text.strip()
            text = remove_prefix(text, CommentParser.DOUBLE_SLASH)
            text = remove_prefix(text, CommentParser.SLASH_STAR)
            text = remove_suffix(text, CommentParser.STAR_SLASH)
            text = text.strip()
            result.append(Comment(text, Position.TOP))
        return result

    @staticmethod
    def create_comment(line, top_comment_list):
        comments = CommentParser.create_top_comments(top_comment_list)
        right_comment = CommentParser.parse_single_line_comment(line)
        if right_comment is not None:
            comments.append(right_comment)
        return comments
