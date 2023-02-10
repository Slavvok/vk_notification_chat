from html.parser import HTMLParser


class EmailHTMLParser(HTMLParser):
    def __init__(self):
        super(EmailHTMLParser, self).__init__()
        self.result = ''

    def handle_data(self, data):
        self.result += f'{data}'
