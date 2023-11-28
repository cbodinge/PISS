from structures import Answers, ReportForm
from pathlib import Path
from reports import By_Drug, Cover
from cairosvg import svg2pdf
from io import BytesIO
from PyPDF2 import PdfWriter


def process(svg: str):
    svg = svg.replace('&', '&amp;')
    buff = svg.encode('utf-8')
    buff = svg2pdf(bytestring=buff)

    return buff


def get_all_results():
    forms = []
    for p in Path('(Report Forms)').iterdir():
        rf = ReportForm()
        rf.read(p)
        forms.append(rf)

    return forms


def get_answers(report_forms: list[ReportForm]):
    ans = Answers()
    ans.read(Path('Info - 2023a.xlsx'))

    for rf in report_forms:
        ans.add_client_data(rf)

    ans.set_calcs()

    return ans


def make_pdfs(page):
    svg = page.construct()
    pdf = process(svg)
    return BytesIO(pdf)


def main():
    forms = get_all_results()
    ans = get_answers(forms)

    ppt = forms[4]
    key = ppt.key
    drugs = ppt.get_reported_drugs()

    pages = [Cover(forms)] + [By_Drug(ppt, ans, drug) for drug in drugs]
    outline = [''] + [key[drug] for drug in drugs]
    pdfs = [make_pdfs(page) for page in pages]

    with open('PISS Challenge 2023a (PPT Comparison).pdf', 'wb') as file:
        w = PdfWriter(file)
        for i, pdf in enumerate(pdfs):
            w.append(pdf, outline_item=outline[i])
        w.write(file)


main()
