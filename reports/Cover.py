from .template import Page, Paragraph, DataTable
from structures import ReportForm


class Report(Page):
    def __init__(self, client_forms: list[ReportForm]):
        super().__init__(f'PISS Challenge 2023 A: Comparison Report')
        self._y = 110
        self._grading()
        self._participants(client_forms)
        self._sign_off()

    def _grading(self):
        sstr = 'There are three possible paths to grade each result: ' \
               '\n \n The first method uses the standard score which must be within ±3. ' \
               '\n The standard score requires that at least three labs reported quantitative results ' \
               'for a particular drug in a particular sample. ' \
               '\n \n The second method uses the calculated mean to determine the bias from the reported results. ' \
               '\n This method is used when standard score is not applicable. ' \
               '\n The absolute bias should be less than 30%. ' \
               '\n \n The third method grades the result against the spiked concentration. ' \
               '\n The absolute spike bias should be less than 30%. ' \
               '\n \n The results are considered acceptable if any of the three grading guidelines are met. ' \
               'Any analytes that do not meet these guidelines may require further analysis and interpretation ' \
               'from the laboratory director or technical supervisor to be approved.'

        grading = Paragraph(self)
        grading.header = ''
        grading.spec_str = sstr
        grading.y = self._y
        self._y += grading.h + 50

        self.sections.append(grading)

    def _participants(self, forms: list[ReportForm]):
        text = self.get_text()
        text.x = 50
        text.y = self._y
        self._y += 25
        text.font.size += 2
        text.text = 'Participating Labs:'

        self.sections.append(text)

        header = [['Lab Name', 'CLIA ID']]
        data = [[lab.name, lab.clia] for lab in forms]

        table = DataTable(self, header + data)

        table.set_row_height(23)

        weights = [0.25, 0.75]
        table.weighted_col_width(750, weights)

        for col in table.cols.values():
            col.align_text(col.align_left)

        table.set_sizes()
        table.y = self._y
        self._y += table.h + 50

        self.sections.append(table)

    def _sign_off(self):
        sstr = 'I have reviewed the interlaboratory comparison study. ' \
               'Results are comparable to other accredited laboratories using laboratory developed ' \
               'tests and pass internal acceptability criteria. ' \
               'At least 5 samples were evaluated as part of this comparison study. ' \
               'Samples represent blanks as well as low, medium and high concentrations. \n \n \n \n ' \
               '\n \n Laboratory Director: __________________________________     Date: ________________________ ' \
               '\n \n ' \
               '\n \n Technical Supervisor: _________________________________     Date: ________________________'

        approval = Paragraph(self)
        approval.header = ''
        approval.spec_str = sstr
        approval.y = self._y

        self.sections.append(approval)
