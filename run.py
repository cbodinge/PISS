from structures import Answers, ReportForm
from pathlib import Path
from reports import Cover, By_Drug
from reports.template import piss

import subprocess


def process(client: str):
    w = 850 * 25.4 / 96
    h = 1100 * 25.4 / 96

    cover = Path("__temp__\\cover.svg").absolute()

    cpath = Path(f'__temp__\\{client}')
    paths = ['"' + str(p.absolute()) + '"' for p in cpath.iterdir()]
    paths.sort(key=lambda x: x.lower())
    paths = ' '.join([f'"{cover}"'] + paths)

    destination = f'"{Path().cwd()}\\(Results)\\PISS Challenge {piss} ({client}).pdf"'

    cmd = f'wkhtmltopdf --disable-smart-shrinking -B 0 -L 0 -R 0 -T 0 --page-height {h} --page-width {w}  --dpi 200 ' \
          f'{paths} {destination}'
    subprocess.call(cmd)


def get_all_results():
    forms = []
    for p in Path('(Report Forms)').iterdir():
        rf = ReportForm()
        rf.read(p)
        forms.append(rf)

    return forms


def get_answers(report_forms: list[ReportForm]):
    ans = Answers()
    ans.read(Path('Info.xlsx'))

    for rf in report_forms:
        ans.add_client_data(rf)

    ans.set_calcs()

    return ans


def save(page, client: str, name: str):
    svg = page.construct()
    svg = svg.replace('&', '&amp;')
    buff = svg.encode('utf-8')

    p = Path(f'__temp__\\{client}')
    if not p.exists():
        p.mkdir()

    with open(f'{str(p)}\\{name}.svg', 'wb') as file:
        file.write(buff)


def build(form, ans):
    drugs = form.get_reported_drugs()
    _ = [save(By_Drug(form, ans, drug), form.name, form.key[drug]) for i, drug in enumerate(drugs)]

    # with open(f'(Results)\\PISS Challenge 2023b ({form.name}).pdf', 'wb') as file:
    #     w = PdfWriter(file)
    #     for i, pdf in enumerate(pdfs):
    #         w.append(pdf, outline_item=outline[i])
    #     w.write(file)


def clear(path: Path):
    if path.is_file():
        path.unlink()
    else:
        for p in path.iterdir():
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                for pp in p.iterdir():
                    clear(pp)
                p.rmdir()


def main():
    forms = get_all_results()
    ans = get_answers(forms)

    svg = Cover(forms).construct()
    svg = svg.replace('&', '&amp;')
    buff = svg.encode('utf-8')

    p = Path(f'__temp__\\cover.svg')

    with open(str(p.absolute()), 'wb') as file:
        file.write(buff)

    for form in forms:
        build(form, ans)
        process(form.name)

    clear(Path('__temp__'))


main()
