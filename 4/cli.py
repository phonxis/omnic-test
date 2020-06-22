import os
import re
import sys
import argparse
import pathlib
import operator


class InspectDir:

    BLANK_LINE = r'^$'

    # # comment
    SHARP_COMMENT = r'(?:^|\s)#(?:.*?)+'

    # '''comment''' """comment"""
    QUOTE_COMMENT = r'(?:^|\s)[\'|\"]{3}(?:.*?\n)+[\'|\"]{3}'

    # /*comment*/
    STAR_COMMENT = r'(?:^|\s)/\*(?:.*?\n)+\*/'

    # // comment
    SLASH_COMMENT = r'(?:^|\s)//(?:.*?)+'

    # <!-- comment -->
    HTML_COMMENT = r'(?:^|\s)\<\!\-\-(?:.*?)\-\-\>'

    LANGS = {
        '.py': {
            'name': 'Python',
            'oneline_comment_pattern': SHARP_COMMENT,
            'multiline_comment_pattern': QUOTE_COMMENT
        },
        '.c': {
            'name': 'C',
            'oneline_comment_pattern': None,
            'multiline_comment_pattern': STAR_COMMENT,
        },
        '.cpp': {
            'name': 'C',
            'oneline_comment_pattern': SLASH_COMMENT,
            'multiline_comment_pattern': STAR_COMMENT,
        },
        '.css': {
            'name': 'CSS',
            'oneline_comment_pattern': SLASH_COMMENT,
            'multiline_comment_pattern': STAR_COMMENT,
        },
        '.html': {
            'name': 'HTML',
            'oneline_comment_pattern': None,
            'multiline_comment_pattern': HTML_COMMENT,
        },
        '.js': {
            'name': 'JavaScript',
            'oneline_comment_pattern': SLASH_COMMENT,
            'multiline_comment_pattern': STAR_COMMENT,
        },
    }

    def __init__(self, cli_args):
        self.cli_args = cli_args

    def process_directory(self):
        result = {}
        for root, _, filenames in os.walk(self.cli_args.directory):

            for filename in filenames:

                extension = pathlib.Path(filename).suffix  # get extension of file

                if extension in self.LANGS.keys():

                    language = self.LANGS.get(extension)

                    data = self.process_file(root, filename, language)

                    language = data[0]  # Get language name from resulting tuple

                    if language in result.keys():
                        # Sum tuples
                        # (1, 2, 3) + (3, 2, 1) = (4, 4, 4)
                        result[language] = list(map(operator.add, result[language], data[1:]))
                    else:
                        result[language] = list(data[1:])

        self.pretty_print(result)

    def process_file(self, root, filename, language):
        blank = 0
        comments = 0

        file_path = pathlib.Path(
            os.path.abspath(
                os.path.join(root, filename)
            )
        )

        size = file_path.stat().st_size // 1024  # File size in KBs

        with open(str(file_path)) as file_object:
            file_text = file_object.read()

        rows = len(file_text.split('\n'))  # Number of file's rows

        search_pattern = "({pattern1})|({pattern2})|({pattern3})".format(
            pattern1=self.BLANK_LINE,
            pattern2=language.get('oneline_comment_pattern'),
            pattern3=language.get('multiline_comment_pattern')
        )

        matches = re.finditer(search_pattern.strip(), file_text, re.MULTILINE)

        for match in matches:
            # Matching blank lines
            if match.group(1) is not None:
                blank += 1
            # Matching oneline comments
            if match.group(2) is not None:
                comments += 1
            # Matching multiline comments
            if match.group(3) is not None:
                comments += len(match.group(3).split('\n'))

        return (
            language.get('name'),               # type (Python, JS etc.)
            rows - blank - comments,            # Code lines
            comments,                           # Number of comment lines
            blank,                              # Number of blank lines
            1,                                  # Indicate that one file
            size                                # Size in Kbs
        )

    def pretty_print(self, data):
        columns = ["Language", "Code", "Comment", "Blank", "Files", "Size(KB)"]
        row_format = "{:>10}" * len(columns)

        print(row_format.format(*columns))

        for key in data.keys():
            print(row_format.format(
                key,
                *data[key]
            ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process files from directory')
    parser.add_argument('directory', metavar='DIR', type=str, help='directory with files')
    args = parser.parse_args()  # Get arguments from cli
    
    inspecting = InspectDir(args)
    inspecting.process_directory()
