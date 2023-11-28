import PySVG
from PySVG.Text import Table


class Page(PySVG.SVG):
    def __init__(self, title, subtitle=''):
        super().__init__(850, 1100)

        self.background = PySVG.Draw.Rect()
        self.background.fill = (255, 255, 255)
        self.background.fill_opacity = 1

        self.title = self.get_title()
        self.title.text = title

        self.subtitle = self.get_subtitle()
        self.subtitle.text = subtitle
        if subtitle == '':
            self.subtitle.active = False

        self.specification = ''

        self.sections = []

        self.y_margin = 50
        self.title_h = 65

    def get_text(self):
        text = PySVG.Text()
        text.fill = (0, 0, 0)
        text.fill_opacity = 1
        text.font = PySVG.Font('IBM Plex Mono', 11, '500')
        text.baseline = 'central'

        return text

    def get_title(self):
        text = PySVG.Text()
        text.fill = text.fill = (0, 0, 0)
        text.fill_opacity = 1
        text.font = PySVG.Font('IBM Plex Mono', 20, '700')
        text.baseline = 'hanging'
        text.anchor = 'start'

        text.x = 50
        text.y = 50

        return text

    def get_subtitle(self):
        text = self.get_title()
        text.font.size -= 6

        text.y = 75

        return text

    def justify(self):
        page_height = 1100 - 2 * self.y_margin - self.title_h
        if len(self.sections) > 1:
            total_section_height = sum([section.h for section in self.sections])
            dy = (page_height - total_section_height) / (len(self.sections) - 1)
        else:
            dy = 50

        y = self.y_margin + self.title_h
        for section in self.sections:
            section.y = y
            y += section.h + dy

    def construct(self):
        self.add_child(self.background)
        self.add_child(self.title)
        self.add_child(self.subtitle)

        for section in self.sections:
            self.add_child(section)

        return super().construct()


class Paragraph(PySVG.Paragraph):
    def __init__(self, parent: Page):
        super().__init__(0, 0)
        self.text = parent.get_text()
        self._spec_str = ''
        self._spec_tuple = ()
        self.x, self.y, self.w, self.h = 50, 600, 750, 500

        self.linewidth = 18
        self.indention = 1
        self.header = ''

        self.background = PySVG.Draw.Rect(0, 0, self.w, self.h)
        # self.background.fill = (155, 223, 245)
        # self.background.fill_opacity = 1

    @property
    def spec_str(self):
        return self._spec_str

    @spec_str.setter
    def spec_str(self, spec_str: str):
        self._spec_str = spec_str
        try:
            self.text.text = self.header + spec_str % self.spec_tuple
        except (TypeError, ValueError):
            self.text.text = self.header + spec_str

        self.makefit()

    @property
    def spec_tuple(self):
        return self._spec_tuple

    @spec_tuple.setter
    def spec_tuple(self, spec_tuple: tuple):
        self._spec_tuple = spec_tuple
        try:
            self.text.text = self.header + self.spec_str % self.spec_tuple
        except TypeError:
            self.text.text = self.header + self.spec_str

        self.makefit()

    def construct(self):
        self.text.text = self.text.text

        b = self.background
        b.x, b.y, b.w, b.h = 0, 0, self.w, self.h
        self.add_child(b)

        return super().construct()


class DataTable(Table):
    def __init__(self, parent: Page, data: list[list] = None):
        super().__init__(parent.get_text())

        if data:
            for i in range(len(data)):
                for j in range(len(data[0])):
                    self.add_box(i, j, data[i][j])

        self.x = 50
        self.y = 200
        self.size = (750, 500)
        self._switch = True

    @property
    def w(self):
        return self.size[0]

    @w.setter
    def w(self, width):
        self.size = (width, self.size[1])

    @property
    def h(self):
        return self.size[1]

    @h.setter
    def h(self, height):
        self.size = (self.size[0], height)

    def construct(self):
        if self._switch:
            container = PySVG.Section(self.x, self.y)
            container.add_child(self)
            self._switch = False
            return container.construct()

        return super().construct()
