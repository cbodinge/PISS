import openpyxl as xl
from pathlib import Path
from transforms import quant_or_qual, is_datetime, read_scalar
from numpy import mean, std


#######################################################################################################################
# Individual Data Classes #############################################################################################
#######################################################################################################################


class ReportForm:
    """
    Data Class representing the results that an individual client lab produces
    """

    def __init__(self):
        self.name = ''
        self.clia = ''
        self.analyst = ''
        self.received_date = None
        self.report_date = None

        self.key = {}

        self.results = {}

    def read(self, path: Path):
        """
        Reads the Excel report form and fills out the class data
        :param path: Path to the form
        """
        wb = xl.load_workbook(path)
        self._read_lab_info(wb)
        self._read_key(wb)
        self._read_results(wb)

    def _read_lab_info(self, wb: xl.workbook.workbook.Workbook):
        data = list(wb.worksheets[0].values)
        data = [[row[0], row[4]] for row in data if row[0] is not None]

        self.name = data[1][1]
        self.clia = data[2][1]
        self.analyst = data[6][1]
        self.received_date = is_datetime(data[3][1])
        self.report_date = is_datetime(data[5][1])
        pass

    def _read_key(self, wb: xl.workbook.workbook.Workbook):
        data = list(wb.worksheets[1].values)
        self.key = {row[0]: row[1] for row in data[12:] if row[0] is not None}

    def _read_results(self, wb: xl.workbook.workbook.Workbook):
        for ws in wb.worksheets[2:]:
            if ws.title[:3] == 'ISS':
                data = list(ws.values)
                self.results[ws.title] = {row[0]: quant_or_qual(row[2]) for row in data[4:] if self._test_code(row[0])}
        pass

    def _test_code(self, code):
        if type(code) == int:
            return True

        return False

    def get_reported_drugs(self):
        drugs = list(set(i for res in self.results.values() for i in res.keys()))
        drugs.sort()
        return drugs


#######################################################################################################################
# Aggregate Data Classes ##############################################################################################
#######################################################################################################################


class Answer:
    def __init__(self, sample, drug_id, drug_name, exp_conc):
        self.drug_id = drug_id
        self.drug_name = drug_name
        self.sample = sample
        self.exp_conc = exp_conc

        self.mean = 0
        self.std = 0
        self.cv = 0
        self.n = 0
        self.results = {}


class Answers(dict):
    def read(self, path: Path):
        wb = xl.load_workbook(path)
        ms = self._read_master_sets(wb)
        sc = self._read_sample_content(wb)

        for smpl, vals in sc.items():
            self[smpl] = self._get_drugs(ms, smpl, vals[0], vals[1], vals[2])

    def _read_master_sets(self, wb: xl.workbook.workbook.Workbook):
        ws = [w for w in wb.worksheets if w.title == 'Master Sets'][0]
        return [[row[0], row[2], row[1], read_scalar(row[3])]
                for row in list(ws.values)[1:] if row[0] is not None]

    def _read_sample_content(self, wb: xl.workbook.workbook.Workbook):
        ws = [w for w in wb.worksheets if w.title == 'Sample Content'][0]
        return {row[0]: [row[1], row[2], row[3]]
                for row in list(ws.values)[1:] if row[0] is not None}

    def _get_drugs(self, master_set, sample, grp1, grp2, expected):
        d = {row[1]: Answer(sample, row[1], row[2], read_scalar(row[3]) * expected)
             for row in master_set if row[0] == grp1 or row[0] == grp2}

        d['Error'] = {}

        return d

    def add_client_data(self, rf: ReportForm):
        for smpl, vals in rf.results.items():
            for drg, conc in vals.items():
                s = self[smpl]
                if drg in s:
                    ans = s[drg]
                    ans.results[rf.name] = conc
                else:
                    s['Error'][drg] = 'Not Found'

    def set_calcs(self):
        for smpl, sdict in self.items():
            for drg, ans in sdict.items():
                if drg != 'Error':
                    conc = [i for i in ans.results.values() if i > 0]
                    ans.n = len(conc)
                    self._mean(ans, conc)
                    self._std(ans, conc)

    def _mean(self, ans, conc):
        if conc:
            ans.mean = mean(conc)

    def _std(self, ans, conc):
        if len(conc) > 2:
            ans.std = std(conc, ddof=1)
            ans.cv = ans.std / mean(conc)
