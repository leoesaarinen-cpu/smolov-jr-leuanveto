from fpdf import FPDF
from datetime import date
from typing import List, Dict
from program_logic import fi_kg, fi_pct


TIER_FILL = {
    "low":    (238, 242, 255),
    "mid":    (219, 234, 254),
    "high":   (191, 219, 254),
    "deload": (236, 253, 245),
    "test":   (254, 243, 199),
}

PRIMARY  = (10, 37, 64)
MUTED    = (107, 114, 128)
TEXT     = (26, 31, 54)
WHITE    = (255, 255, 255)
BORDER   = (229, 231, 235)


def _set_color(pdf: FPDF, rgb: tuple, fill: bool = False):
    if fill:
        pdf.set_fill_color(*rgb)
    else:
        pdf.set_text_color(*rgb)


def generate_pdf(program: List[Dict], settings: Dict) -> bytes:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    page_w = 210 - 36  # usable width

    # ── Header ────────────────────────────────────────────────────
    _set_color(pdf, PRIMARY)
    pdf.set_font('Helvetica', 'B', 22)
    pdf.cell(0, 10, 'SMOLOV JR. - LEUANVETO', ln=True)

    _set_color(pdf, MUTED)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, '4 viikon maksimivoimaohjelma lisapainolla', ln=True)

    pdf.ln(3)
    _set_color(pdf, BORDER, fill=True)
    pdf.set_draw_color(*BORDER)
    pdf.set_line_width(0.3)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(5)

    # ── Settings block ────────────────────────────────────────────
    _set_color(pdf, MUTED)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 5, 'ASETUKSET', ln=True)
    pdf.ln(1)

    _set_color(pdf, TEXT)
    pdf.set_font('Helvetica', '', 10)
    madd = settings.get('max_added', 0)
    winc = settings.get('weekly_increase', 0)
    today = date.today().strftime('%d.%m.%Y')

    col = page_w / 3
    pdf.cell(col, 6, f"Lisapaino-maksimi: {fi_kg(madd)}")
    pdf.cell(col, 6, f"Viikkonosto: {winc:g} %-yks.")
    pdf.cell(col, 6, f"Paivamaara: {today}", ln=True)

    pdf.ln(4)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(6)

    # ── Weeks ─────────────────────────────────────────────────────
    for week in program:
        wn   = week['week_number']
        wt   = week['week_type'].upper()
        label = f"VIIKKO {wn} - {wt}"

        _set_color(pdf, PRIMARY)
        pdf.set_font('Helvetica', 'B', 13)
        pdf.cell(0, 7, label, ln=True)
        pdf.ln(2)

        col_widths = [32, 22, 22, 22, page_w - 98]

        for s in week['sessions']:
            tier = s.get('intensity_tier', 'low')
            fill_rgb = TIER_FILL.get(tier, TIER_FILL['low'])

            _set_color(pdf, fill_rgb, fill=True)
            row_h = 8

            if s['type'] == 'rest':
                pdf.set_fill_color(*TIER_FILL['deload'])
                _set_color(pdf, MUTED)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(col_widths[0], row_h, f"TREENI {s['treeni']}", fill=True)
                _set_color(pdf, MUTED)
                pdf.set_font('Helvetica', '', 10)
                pdf.cell(page_w - col_widths[0], row_h, 'LEPO / AKTIIVINEN PALAUTUMINEN', fill=True, ln=True)
            elif s['type'] == 'test':
                pdf.set_fill_color(*TIER_FILL['test'])
                _set_color(pdf, MUTED)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(col_widths[0], row_h, f"TREENI {s['treeni']}", fill=True)
                _set_color(pdf, TEXT)
                pdf.set_font('Helvetica', 'B', 10)
                pdf.cell(page_w - col_widths[0], row_h, 'MAKSIMITESTI', fill=True, ln=True)
            else:
                _set_color(pdf, MUTED)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(col_widths[0], row_h, f"TREENI {s['treeni']}", fill=True)

                _set_color(pdf, TEXT)
                pdf.set_font('Helvetica', '', 10)
                sets_reps = f"{s['sets']} x {s['reps']}"
                pdf.cell(col_widths[1], row_h, sets_reps, fill=True)

                pdf.set_font('Helvetica', '', 10)
                pdf.cell(col_widths[2], row_h, fi_pct(s['pct']), fill=True)

                pdf.set_font('Helvetica', 'B', 10)
                _set_color(pdf, PRIMARY)
                pdf.cell(page_w - col_widths[0] - col_widths[1] - col_widths[2],
                         row_h, fi_kg(s['weight']), fill=True, align='R', ln=True)

            pdf.ln(1)

        pdf.ln(6)

    # ── Footer ────────────────────────────────────────────────────
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(3)
    _set_color(pdf, MUTED)
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(0, 5, f"Tuotettu Smolov Jr. -sovelluksella, {today}", ln=True)

    return bytes(pdf.output())
