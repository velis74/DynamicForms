from html.parser import HTMLParser


class RTFFieldMixin(object):
    def __init__(self, *args, show_as_plain_text=False, plain_text_lines=3, plain_text_line_length=40, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse = show_as_plain_text or False
        self.max_lines = plain_text_lines
        self.max_line_length = plain_text_line_length
        self.parser = RTFFieldHTMLParser(max_lines=self.max_lines, max_line_length=self.max_line_length)

    def to_representation(self, instance, row_data=None):
        if not self.parent.is_filter:
            self.style.update({"base_template": "rtf_field.html"})
        if self.is_rendering_to_list and not self.parent.is_filter and self.parse:
            self.parser.feed(instance)
            instance = self.parser.to_string()
            self.parser.reset()

        return super().to_representation(instance, row_data)


class RTFFieldHTMLParser(HTMLParser):
    def __init__(self, max_lines, max_line_length):
        self.text = []
        self.curr_line_count = 1
        self.curr_line = ""
        self.max_lines = max_lines
        self.max_line_length = max_line_length
        super(RTFFieldHTMLParser, self).__init__()

    def handle_data(self, data):
        text = data.strip()
        if self.curr_line_count <= self.max_lines:
            if len(text) > 0:
                self.curr_line += " " + text
                line = self.curr_line[0 : self.max_line_length - 3]
                if len(self.curr_line) >= self.max_line_length - 3:
                    line += "..."
                line += "<br>"
                self.text.append(line)
                self.curr_line = ""
                self.curr_line_count += 1

    def reset(self):
        self.text = []
        self.curr_line_count = 1
        self.curr_line = ""
        super(RTFFieldHTMLParser, self).reset()

    def to_string(self):
        return "".join(self.text).strip()
