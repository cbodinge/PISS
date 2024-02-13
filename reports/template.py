from PySVG import Document, TextBox, Text, Font, Paragraph, G

piss = '2023 B'

_family = 'IBM Plex Mono'
font400 = Font(_family, '400')
font500 = Font(_family, '500')
font600 = Font(_family, '600')
font700 = Font(_family, '700')


class Page(Document):
    def __init__(self, title: str):
        super().__init__(w=850, h=1100)

        self.title = self._title(title)

        self.specification = ''

        self.y_margin = 50
        self.title_h = 65

    def _title(self, title: str):
        t = Text(font700, text=title, fill=(50, 60, 70), fill_opacity=1, size=18)
        tb = TextBox(t, (0, 0), x=50, y=50, w=750, h=1000)
        tb.fill = (0, 222, 50)
        tb.fill_opacity = 0.25
        tb.set()
        tb.background.active = False

        self.addChild(tb.root)
        return tb

    def text(self):
        return Text(font500, fill=(25, 30, 35), fill_opacity=1, baseline='central', anchor='start', size=11)


class Paragraphs(G):
    def __init__(self, linewidth: float, string: str = '', **kwargs):
        super().__init__(**kwargs)
        self.text = Text(font500, text=string, fill=(25, 30, 35), fill_opacity=1,
                         baseline='central', anchor='start', size=11)

        self.lw = linewidth

        self._p = []

        self.h = 0

    def addParagraph(self, string: str):
        t = self.text.copy()
        t.text = string
        p = Paragraph(t, 750, 0, 50, 50)
        p.linewidth = self.lw
        self._p.append(p)
        self.add_child(p.root)

    def set(self):
        y = 0
        for p in self._p:
            if p.text.text == '':
                y += self.lw
                p.root.active = False
            else:
                p.set()
                p.y = y
                y += p.h

        self.h = y
