CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    color-scheme: light;
    --bg:         #F8F9FB;
    --surface:    #FFFFFF;
    --primary:    #0A2540;
    --accent:     #047857;
    --text:       #1A1F36;
    --text-muted: #6B7280;
    --border:     #E5E7EB;

    --int-low:    #EEF2FF;
    --int-mid:    #DBEAFE;
    --int-high:   #BFDBFE;
    --int-deload: #ECFDF5;
    --int-test:   #FEF3C7;

    --bar-low:    #6366F1;
    --bar-mid:    #3B82F6;
    --bar-high:   #1D4ED8;
    --bar-deload: #047857;
    --bar-test:   #D97706;
}

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

.stApp { background-color: var(--bg); }

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1180px;
}

/* ── App header ──────────────────────────────────────────── */
.app-header-content h1 {
    font-size: 28px;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: -0.02em;
    margin: 0 0 4px 0;
    line-height: 1.2;
}
.app-header-content .subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin: 0;
}

/* ── Settings ────────────────────────────────────────────── */
.settings-stack {
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.settings-label {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 2px;
}
.settings-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--primary);
    font-variant-numeric: tabular-nums;
}

/* ── Week card ───────────────────────────────────────────── */
.week-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 1px 3px rgba(10, 37, 64, 0.04);
    margin-bottom: 0;
}
.week-card-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
}
.week-card-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--primary);
}
.week-card-type {
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Treeni rows (compact) ───────────────────────────────── */
.treeni-row {
    display: grid;
    grid-template-columns: 4px 36px 1fr auto auto;
    gap: 12px;
    align-items: center;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 4px;
    font-variant-numeric: tabular-nums;
}
.treeni-row:last-child { margin-bottom: 0; }

.treeni-bar {
    height: 100%;
    min-height: 24px;
    border-radius: 2px;
    align-self: stretch;
}
.treeni-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.treeni-volume {
    font-size: 13px;
    color: var(--text);
    font-variant-numeric: tabular-nums;
}
.treeni-pct {
    background: var(--primary);
    color: white;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}
.treeni-weight {
    font-size: 15px;
    font-weight: 700;
    color: var(--primary);
    font-variant-numeric: tabular-nums;
    text-align: right;
    min-width: 72px;
    white-space: nowrap;
}

/* ── Special rows ────────────────────────────────────────── */
.treeni-row-special {
    display: grid;
    grid-template-columns: 4px 1fr;
    gap: 12px;
    align-items: center;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 4px;
    min-height: 40px;
}
.treeni-row-special:last-child { margin-bottom: 0; }
.treeni-row-special .label-center {
    text-align: center;
    font-size: 13px;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.04em;
}

/* ── Force light-theme text regardless of OS dark mode ───── */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
label {
    color: var(--text) !important;
}

/* ── Number input styling ────────────────────────────────── */
[data-testid="stNumberInput"] input {
    font-size: 16px;
    font-weight: 500;
    color: var(--primary) !important;
    background-color: #FFFFFF !important;
}

[data-testid="stNumberInput"] {
    background-color: transparent !important;
}

/* ── Download button ─────────────────────────────────────── */
[data-testid="stDownloadButton"] button {
    background: var(--surface) !important;
    color: var(--primary) !important;
    border: 1px solid var(--border) !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    width: 100%;
}
[data-testid="stDownloadButton"] button:hover {
    background: var(--primary) !important;
    color: white !important;
}
"""
