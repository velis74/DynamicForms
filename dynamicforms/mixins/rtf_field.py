from html.parser import HTMLParser
from re import sub


class RTFFieldMixin(object):

    def to_representation(self, instance, row_data=None):
        if not self.parent.is_filter:
            self.style.update({'base_template': 'rtf_field.html'})
        if self.is_rendering_to_list and not self.parent.is_filter:
            parser = RTFFieldHTMLParser()
            parser.feed(instance)
            instance = parser.to_string()

        return super().to_representation(instance, row_data)


class RTFFieldHTMLParser(HTMLParser):
    text = []
    max_lines = 3
    max_line_length = 40
    curr_line = 1

    def __init__(self):
        self.text = []
        super(RTFFieldHTMLParser, self).__init__()

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0 and self.curr_line <= self.max_lines:
            text = sub('[ \t\r\n]+', ' ', text)[0:self.max_line_length - 3]
            if len(text) >= self.max_line_length - 3:
                text += '...'
            if self.curr_line < self.max_lines:
                text += '<br/>'
            self.text.append(text)
        self.curr_line += 1

    def to_string(self):
        return ''.join(self.text).strip()
