import streamlit as st
import plotly.graph_objects as go

from program_logic import calculate_program, fi_kg, fi_pct
from pdf_generator import generate_pdf
from styles import CSS

st.set_page_config(page_title="Smolov Jr. — Leuanveto", layout="wide")
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


MONO_BLUE_SCALE = [
    [0.0, "#E6F1FB"],
    [0.2, "#B5D4F4"],
    [0.4, "#85B7EB"],
    [0.6, "#378ADD"],
    [0.8, "#185FA5"],
    [1.0, "#0C447C"],
]


def get_text_color(weight: float, min_w: float, max_w: float) -> str:
    norm = (weight - min_w) / (max_w - min_w) if max_w != min_w else 0.5
    return "#042C53" if norm < 0.3 else "white"


def create_heatmap(program):
    weeks_1_3 = program[:3]

    z_raw, text_raw = [], []
    for t_idx in range(4):
        row_z, row_text = [], []
        for w in weeks_1_3:
            s = w["sessions"][t_idx]
            row_z.append(s["weight"])
            row_text.append(fi_kg(s["weight"]))
        z_raw.append(row_z)
        text_raw.append(row_text)

    z_rev    = list(reversed(z_raw))
    text_rev = list(reversed(text_raw))
    y_labels = ["Treeni 4", "Treeni 3", "Treeni 2", "Treeni 1"]

    all_w = [w for row in z_rev for w in row]
    min_w, max_w = min(all_w), max(all_w)

    annotations = []
    for i, (row_z, row_t) in enumerate(zip(z_rev, text_rev)):
        for j, (val, txt) in enumerate(zip(row_z, row_t)):
            annotations.append(dict(
                x=j, y=i, text=txt, showarrow=False,
                font=dict(size=13, color=get_text_color(val, min_w, max_w), family="Inter"),
            ))

    fig = go.Figure(data=go.Heatmap(
        z=z_rev,
        x=["Viikko 1", "Viikko 2", "Viikko 3"],
        y=y_labels,
        colorscale=MONO_BLUE_SCALE,
        showscale=False,
        xgap=3,
        ygap=3,
        hovertemplate="<b>%{y}, %{x}</b><br>Paino: %{text}<extra></extra>",
        text=text_rev,
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=240,
        margin=dict(l=60, r=10, t=10, b=10),
        font=dict(family="Inter", size=12, color="#1A1F36"),
        xaxis=dict(side="top", showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, tickfont=dict(size=12)),
        annotations=annotations,
    )
    return fig


def _row_html(s: dict) -> str:
    stype = s["type"]
    if stype == "rest":
        return (
            '<div class="treeni-row-special" style="background:var(--int-deload);">'
            '<div class="treeni-bar" style="background:var(--bar-deload);"></div>'
            '<div class="label-center">— Lepo —</div>'
            '</div>'
        )
    if stype == "test":
        return (
            '<div class="treeni-row-special" style="background:var(--int-test);">'
            '<div class="treeni-bar" style="background:var(--bar-test);"></div>'
            '<div class="label-center">Maksimitesti</div>'
            '</div>'
        )
    tier = s["intensity_tier"]
    return (
        f'<div class="treeni-row" style="background:var(--int-{tier});">'
        f'<div class="treeni-bar" style="background:var(--bar-{tier});"></div>'
        f'<div class="treeni-label">T{s["treeni"]}</div>'
        f'<div class="treeni-volume">{s["sets"]} × {s["reps"]}</div>'
        f'<div class="treeni-pct">{fi_pct(s["pct"])}</div>'
        f'<div class="treeni-weight">+{fi_kg(s["weight"])}</div>'
        '</div>'
    )


def render_week_card(week: dict):
    wn = week["week_number"]
    type_label = "Kuormitus" if week["week_type"] == "kuormitus" else "Deload + testi"
    rows = "".join(_row_html(s) for s in week["sessions"])
    html = (
        f'<div class="week-card">'
        f'<div class="week-card-header">'
        f'<div class="week-card-title">Viikko {wn}</div>'
        f'<div class="week-card-type">{type_label}</div>'
        f'</div>'
        f'{rows}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


PULLUP_SVG = (
    '<svg width="48" height="76" viewBox="0 0 54 82" xmlns="http://www.w3.org/2000/svg">'
    # Bar
    '<rect x="2" y="5" width="50" height="3" rx="1.5" fill="#0A2540"/>'
    # Head — clearly above the shoulders
    '<circle cx="27" cy="18" r="7" fill="#0A2540"/>'
    # Neck + torso as one continuous line
    '<line x1="27" y1="25" x2="27" y2="62" stroke="#0A2540" stroke-width="3" stroke-linecap="round"/>'
    # Shoulder cross-bar (makes arm attachment point obvious)
    '<line x1="18" y1="34" x2="36" y2="34" stroke="#0A2540" stroke-width="2.5" stroke-linecap="round"/>'
    # Left arm: bar → elbow (flared out) → shoulder
    '<polyline points="14,6.5 8,21 18,34" fill="none" stroke="#0A2540" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'
    # Right arm: bar → elbow → shoulder
    '<polyline points="40,6.5 46,21 36,34" fill="none" stroke="#0A2540" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>'
    # Left leg
    '<line x1="27" y1="62" x2="18" y2="78" stroke="#0A2540" stroke-width="2.5" stroke-linecap="round"/>'
    # Right leg
    '<line x1="27" y1="62" x2="36" y2="78" stroke="#0A2540" stroke-width="2.5" stroke-linecap="round"/>'
    '</svg>'
)

# ── Header row (placeholder for PDF button filled after compute) ─────────────
hdr_left, hdr_right = st.columns([5, 1])
with hdr_left:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:18px;">'
        '<div class="app-header-content">'
        '<h1>Smolov jr. — Leuanveto</h1>'
        '<p class="subtitle">4 viikon maksimivoimaohjelma</p>'
        '</div>'
        f'{PULLUP_SVG}'
        '</div>',
        unsafe_allow_html=True,
    )
with hdr_right:
    pdf_btn_slot = st.empty()

st.markdown(
    '<hr style="border:none;border-top:1px solid var(--border);margin:0.75rem 0 1.5rem;">',
    unsafe_allow_html=True,
)

# ── Top row: settings card (left) + heatmap (right) ─────────────────────────
top_left, top_right = st.columns([1, 3])

with top_left:
    max_added = st.number_input(
        "Lisäpaino-maksimi (kg)",
        min_value=5.0, max_value=150.0, value=30.0, step=0.5,
    )
    weekly_increase = st.number_input(
        "Viikkonosto (%-yksikköä)",
        min_value=1.0, max_value=15.0, value=5.0, step=0.5,
    )

# ── Compute (inputs are now defined above) ───────────────────────────────────
program   = calculate_program(max_added, weekly_increase)
settings  = {"max_added": max_added, "weekly_increase": weekly_increase}
pdf_bytes = generate_pdf(program, settings)
filename  = f"Smolov_Jr_Leuanveto_{max_added:g}kg.pdf"

# ── Fill PDF button placeholder ───────────────────────────────────────────────
with pdf_btn_slot:
    st.download_button(
        label="Lataa PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
    )

# ── Heatmap ───────────────────────────────────────────────────────────────────
with top_right:
    fig = create_heatmap(program)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False, "staticPlot": True})

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Week grid 2×2 ───────────────────────────────────────────────────────────
row1_l, row1_r = st.columns(2, gap="small")
with row1_l:
    render_week_card(program[0])
with row1_r:
    render_week_card(program[1])

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

row2_l, row2_r = st.columns(2, gap="small")
with row2_l:
    render_week_card(program[2])
with row2_r:
    render_week_card(program[3])
