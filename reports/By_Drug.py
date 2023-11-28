from .template import Page, DataTable
from structures import ReportForm, Answers


class Report(Page):
    def __init__(self, client_form: ReportForm, answers: Answers, drug: int):
        super().__init__(f'{client_form.key[drug]}: Result Summary')
        self.matrix = self._init_data(answers, drug, client_form)
        self.spiked = self._init_spiked(answers, drug)
        self._y = 110
        self.aggregate_table()
        self.result_table()
        self.comment_table()
        pass

    def _init_data(self, answers: Answers, drug: int, client_form: ReportForm):
        matrix = {s: ['---', '---', '---', '---'] for s in answers.keys()}

        for smpl, results in client_form.results.items():
            if drug in results:
                conc = results[drug]
                matrix[smpl][0] = f'{conc:.1f}' if conc != -1 else 'Detected'
                try:
                    ans = answers[smpl][drug]
                    if conc > 0 and ans.mean > 0:
                        matrix[smpl][1] = f'{100 * (ans.mean - conc) / ans.mean:.1f}%'

                    if conc > 0 and ans.std > 0:
                        matrix[smpl][2] = f'{(ans.mean - conc) / ans.std:.1f}'

                    if conc > 0 and ans.exp_conc > 0:
                        matrix[smpl][3] = f'{100 * (ans.exp_conc - conc) / ans.exp_conc:.1f}%'

                except KeyError:
                    pass

            else:
                matrix[smpl][0] = 'Not Detected'

        matrix = [[smpl] + vals for smpl, vals in matrix.items()]
        matrix.sort()

        return matrix

    def _init_spiked(self, answers: Answers, drug):
        spiked = [results[drug] for results in answers.values() if drug in results]
        spiked.sort(key=lambda x: x.sample)
        matrix = [[s.sample, f'{s.n:.0f}', f'{s.mean:.1f}', f'{s.std:.1f}' if s.std > 0 else '---'] for s in spiked]

        return matrix

    def aggregate_table(self):
        text = self.get_text()
        text.x = 50
        text.y = self._y
        self._y += 15
        text.font.size += 2
        text.text = 'Aggregate Info:'

        self.sections.append(text)

        header = ['Sample', 'N', 'Mean', 'Standard Deviation']
        table = DataTable(self, [header] + self.spiked)

        table.set_row_height(20)

        weights = [0.25, 0.25, 0.25, 0.25]
        table.weighted_col_width(750, weights)

        for col in table.cols.values():
            col.align_text(col.align_center)

        table.set_sizes()
        table.y = self._y
        self._y += table.h + 40

        self.sections.append(table)

    def result_table(self):
        text = self.get_text()
        text.x = 50
        text.y = self._y
        self._y += 15
        text.font.size += 2
        text.text = 'Reported Results:'

        self.sections.append(text)

        header = ['Sample', 'Reported Value', 'Bias', 'Standard Score', 'Spike Bias']
        table = DataTable(self, [header] + self.matrix)

        table.set_row_height(16)

        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        table.weighted_col_width(750, weights)

        for col in table.cols.values():
            col.align_text(col.align_center)

        table.set_sizes()
        table.y = self._y
        self._y += table.h + 50

        self.sections.append(table)

    def comment_table(self):
        text = self.get_text()
        text.x = 50
        text.y = self._y
        self._y += 15
        text.font.size += 2
        text.text = 'Notes:'

        self.sections.append(text)

        table = DataTable(self, [[''] for _ in range(8)])

        table.set_row_height(25)
        weights = [1]
        table.weighted_col_width(750, weights)

        i = -1
        for row in table.rows.values():
            i *= -1
            if i == 1:
                row.h = 1
                row.fill = (0, 0, 0)
                row.fill_opacity = 1

        table.set_sizes()
        table.y = self._y

        self.sections.append(table)
