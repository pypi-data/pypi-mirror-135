# Copyright 2018 Tile, Inc.  All Rights Reserved.
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from mistletoe import block_token
from mistletoe.base_renderer import BaseRenderer


def escape_url(raw):
    """
    Escape urls to prevent code injection craziness. (Hopefully.)
    """
    from urllib.parse import quote
    return quote(raw, safe='/#:')


class MarkdownRenderer(BaseRenderer):
    """Render Markdown... back into Markdown!
    """

    def __init__(self, *extras):
        self.listTokens = []
        super(MarkdownRenderer, self).__init__(*extras)

    def render_document(self, document):
        return ''.join([self.render(token) for token in document.children])

    def render_inner(self, token):
        if isinstance(token, block_token.List):
            if token.start:
                self.listTokens.append('1.')
            else:
                self.listTokens.append('-')

        # Render child tokens
        rendered_tokens = [self.render(child) for child in token.children]

        if isinstance(token, block_token.List):
            del (self.listTokens[-1])

        return ''.join(rendered_tokens)

    def render_strong(self, token):
        return f'__{self.render_inner(token)}__'

    def render_emphasis(self, token):
        return f'*{self.render_inner(token)}*'

    def render_inline_code(self, token):
        return f'`{self.render_inner(token)}`'

    def render_strikethrough(self, token):
        return f'~~{self.render_inner(token)}~~'

    def render_image(self, token):
        alt_text = self.render_inner(token)
        if token.title:
            return f'![{alt_text}]({token.src} "{token.title}")'
        else:
            return f'![{alt_text}]({token.src})'

    def render_link(self, token):
        target = escape_url(token.target)
        return f'[{self.render_inner(token)}]({target})'

    def render_auto_link(self, token):
        return escape_url(self.render_inner(token))

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    def render_heading(self, token):
        return f"\n\n{'#' * token.level} {self.render_inner(token)}\n"

    def render_quote(self, token):
        return f'> {self.render_inner(token)}\n'

    def render_paragraph(self, token):
        return f'{self.render_inner(token)}\n'

    def render_block_code(self, token):
        return f'```{token.language}\n{self.render_inner(token)}```\n'

    def render_list(self, token):
        return self.render_inner(token)

    def render_list_item(self, token):
        prefix = ''.join(self.listTokens)
        return f'{prefix} {self.render_inner(token)}\n'

    def render_table(self, token):
        if hasattr(token, 'header'):
            header = token.children[0]
            header_inner_rendered = self.render_table_row(header, True)
        else:
            header_inner_rendered = ''
        body_inner_rendered = self.render_inner(token)
        return f'{header_inner_rendered}{body_inner_rendered}\n'

    def render_table_row(self, token, is_header=False):
        inner_rendered = ''.join([
            self.render_table_cell(child, is_header) for child in token.children
        ])
        if is_header:
            return f'{inner_rendered}||\n'
        else:
            return f'{inner_rendered}|\n'

    def render_table_cell(self, token, is_header=False):
        if is_header:
            return f'||{self.render_inner(token)}'
        else:
            return f'|{self.render_inner(token)}'

    def render_raw_text(self, token):
        return token.content

    @staticmethod
    def render_thematic_break(token):
        return '---\n'

    @staticmethod
    def render_line_break(token):
        return '\n'
