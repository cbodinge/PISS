from .template import Page
from PySVG import Table, Path
from structures import ReportForm, Answers


class Report(Page):
    def __init__(self, client_form: ReportForm, answers: Answers, drug: int):
        super().__init__(f'{client_form.key[drug]}: Result Summary')
        self.matrix = self._init_data(answers, drug, client_form)
        self.spiked = self._init_spiked(answers, drug)
        self._y = 110
        self.spacing = 50

        self.aggregate_table()
        self.result_table()
        self.comment_table()
        pass

    def _init_data(self, answers: Answers, drug: int, client_form: ReportForm):
        matrix = {s: ['---', '---', '---', '---'] for s in answers.keys()}

        for smpl, results in client_form.results.items():
            if drug in results:
                conc = results[drug]
                matrix[smpl][0] = f'{round(conc * 10) / 10:.1f}' if conc != -1 else 'Detected'
                try:
                    ans = answers[smpl][drug]
                    if conc > 0 and ans.mean > 0:
                        matrix[smpl][1] = f'{100 * (conc - ans.mean) / ans.mean:.1f}%'

                    if conc > 0 and ans.std > 0:
                        matrix[smpl][2] = f'{(conc - ans.mean) / ans.std:.1f}'

                    if conc > 0 and ans.exp_conc > 0:
                        matrix[smpl][3] = f'{100 * (conc - ans.exp_conc) / ans.exp_conc:.1f}%'

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
        matrix = [[s.sample,
                   f'{s.n:.0f}',
                   f'{s.exp_conc}',
                   f'{s.mean:.1f}',
                   f'{s.std:.1f}' if s.std > 0 else '---'] for s in spiked]

        return matrix

    def aggregate_table(self):
        # Header ######################################################################################################
        t = self.text()
        t.x = 50
        t.y = self._y
        t.size += 2
        t.text = 'Aggregate Info:'

        self.addChild(t)
        self._y += 15

        # Table #######################################################################################################
        header = ['Sample', 'N', 'Spike', 'Mean', 'Standard Deviation']
        table = Table(self.text(), [header] + self.spiked, w=750)
        table.set_row_height(20)

        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        table.weighted_col_width(750, weights)

        for row in table.r_rng:
            table.boxes[row, 0].alignment = table.boxes[row, 0].left
            table.boxes[row, 1].alignment = table.boxes[row, 1].center
            table.boxes[row, 2].alignment = table.boxes[row, 2].right
            table.boxes[row, 3].alignment = table.boxes[row, 3].right
            table.boxes[row, 4].alignment = table.boxes[row, 4].right

        table.x = 50
        table.y = self._y
        table.set()

        self.addChild(table.root)
        self._y += table.h + self.spacing

    def result_table(self):
        # Header ######################################################################################################
        t = self.text()
        t.x = 50
        t.y = self._y
        t.size += 2
        t.text = 'Reported Results:'

        self.addChild(t)
        self._y += 15

        # Table #######################################################################################################
        header = ['Sample', 'Reported Value', 'Bias', 'Standard Score', 'Spike Bias']
        table = Table(self.text(), [header] + self.matrix, w=750)
        table.set_row_height(16)

        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        table.weighted_col_width(750, weights)

        for row in table.r_rng:
            table.boxes[row, 0].alignment = table.boxes[row, 0].left
            table.boxes[row, 1].alignment = table.boxes[row, 1].center
            table.boxes[row, 2].alignment = table.boxes[row, 2].right
            table.boxes[row, 3].alignment = table.boxes[row, 3].right
            table.boxes[row, 4].alignment = table.boxes[row, 4].right

        table.x = 50
        table.y = self._y
        table.set()

        self.addChild(table.root)
        self._y += table.h + self.spacing

    def comment_table(self):
        t = self.text()
        t.x = 50
        t.y = self._y
        t.size += 2
        t.text = 'Notes:'
        t.baseline = 'text-top'

        self.addChild(t)
        self._y += 3

        path = Path(stroke=(45, 45, 45), stroke_width=1, stroke_opacity=1)

        for _ in range(5):
            p = path.copy()
            p.points = [('M', 50, self._y), ('L', 800, self._y)]
            self.addChild(p)
            self._y += 25
