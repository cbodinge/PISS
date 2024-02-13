from .template import Page, piss, Paragraphs
from PySVG import Table

from structures import ReportForm


class Report(Page):
    def __init__(self, client_forms: list[ReportForm]):
        super().__init__(f'PISS Challenge {piss}: Comparison Report')
        self._y = 110
        self.spacing = 50

        self._grading()
        self._participants(client_forms)
        self._sign_off()

    def _grading(self):
        p = Paragraphs(18)
        p.y = self._y

        p.addParagraph('There are three possible paths to grade each result:')
        p.addParagraph('')
        p.addParagraph('The first method uses the standard score which must be within ±3.')
        p.addParagraph('The standard score requires that at least three labs reported quantitative results '
                       'for a particular drug in a particular sample.')
        p.addParagraph('')
        p.addParagraph('The second method uses the calculated mean to determine the bias from the reported results.')
        p.addParagraph('This method is used when standard score is not applicable. '
                       'The absolute bias should within ±30%.')
        p.addParagraph('The third method grades the result against the spiked concentration.')
        p.addParagraph('The absolute spike bias should within ±30%.')
        p.addParagraph('')
        p.addParagraph('The results are considered acceptable if any of the three grading guidelines are met. '
                       'Any analytes that do not meet these guidelines may require further analysis and '
                       'interpretation from the laboratory director or technical supervisor to be approved.')

        self.addChild(p)
        p.set()

        self._y += p.h + self.spacing

    def _participants(self, forms: list[ReportForm]):
        # Header ######################################################################################################
        t = self.text()
        t.x = 50
        t.y = self._y
        t.size += 2
        t.text = 'Participating Labs:'
        self.addChild(t)

        self._y += 25

        # Table #######################################################################################################
        header = [['Lab Name', 'CLIA ID']]
        data = [[lab.name, lab.clia] for lab in forms]

        table = Table(self.text(), header + data, w=750)
        table.set_row_height(23)

        weights = [0.25, 0.75]
        table.weighted_col_width(750, weights)

        for row in table.r_rng:
            table.boxes[row, 0].alignment = table.boxes[row, 0].left
            table.boxes[row, 1].alignment = table.boxes[row, 1].right

        table.x = 50
        table.y = self._y
        table.set()

        self.addChild(table.root)
        self._y += table.h + self.spacing

    def _sign_off(self):
        p = Paragraphs(18)
        p.y = self._y

        p.addParagraph('I have reviewed the interlaboratory comparison study. '
                       'Results are comparable to other accredited laboratories using laboratory developed tests and '
                       'pass internal acceptability criteria. '
                       'At least 5 samples were evaluated as part of this comparison study. '
                       'Samples represent blanks as well as low, medium, and high concentrations. ')
        p.addParagraph('')
        p.addParagraph('')
        p.addParagraph('Laboratory Director: __________________________________     Date: ________________________ ')
        p.addParagraph('')
        p.addParagraph('')
        p.addParagraph('Technical Supervisor: _________________________________     Date: ________________________')

        self.addChild(p)
        p.set()
