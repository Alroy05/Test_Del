/* Styles from the view-logs.html design, scoped to this page (.pg-logs) */
.pg-logs { --bg: #FFFFFF; --surface: #FFFFFF; --surface-2: #F9FAFD; --surface-hover: #F3F5FB; --border: #E6E9F2; --border-strong: #D5DAE7; --text: #0F1B3D; --text-muted: #5B6785; --text-faint: #8A94AD; --brand: #1E3A8A; --brand-soft: #E8EEFF; --focus: #3B6CF6; --shadow: 0 1px 2px rgba(15, 27, 61, 0.04), 0 8px 24px -16px rgba(15, 27, 61, 0.18); --scrim: rgba(15, 27, 61, 0.35); --intake-fg: #B45309; --intake-bg: #FEF3E2; --assess-fg: #1D4ED8; --assess-bg: #E7EEFF; --monitor-fg: #047857; --monitor-bg: #E2F6EE; --warn-fg: #B45309; --warn-bg: #FEF3E2; --pink-fg: #BE185D; --pink-bg: #FCE7F1; --done: #10B981; --active: #3B6CF6; }
[data-theme="dark"] .pg-logs { --bg: #0F172B; --surface: #121831; --surface-2: #0F1529; --surface-hover: #182040; --border: #232B45; --border-strong: #2F3958; --text: #E6EAF5; --text-muted: #A3AEC8; --text-faint: #6F7A96; --brand: #7DA2FF; --brand-soft: #1B2547; --focus: #7DA2FF; --shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 8px 24px -16px rgba(0, 0, 0, 0.7); --scrim: rgba(0, 0, 0, 0.55); --intake-fg: #FBBF24; --intake-bg: #33260E; --assess-fg: #8DB0FF; --assess-bg: #18264D; --monitor-fg: #4ADE9F; --monitor-bg: #0F2F25; --warn-fg: #FBBF24; --warn-bg: #33260E; --pink-fg: #F472B6; --pink-bg: #3A1530; --done: #34D399; --active: #7DA2FF; }
.pg-logs * { -webkit-tap-highlight-color: transparent; }
.pg-logs { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); transition: background-color 0.25s ease, color 0.25s ease; }
.pg-logs.no-scroll { overflow: hidden; }
.pg-logs h1,
.pg-logs h2,
.pg-logs .display { font-family: 'Plus Jakarta Sans', sans-serif; }
.pg-logs .mono { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 12px; }
.pg-logs .muted { color: var(--text-muted); }
.pg-logs .faint { color: var(--text-faint); }
.pg-logs :focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; border-radius: 8px; }
.pg-logs .surface { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); }
.pg-logs { --bar: #0B2A7A; --bar-h: 52px; --rail-w: 64px; }
[data-theme="dark"] .pg-logs { --bar: #0A1636; }
.pg-logs .appbar { position: fixed; top: 0; left: var(--rail-w); right: 0; z-index: 25; height: var(--bar-h); display: flex; align-items: center; padding: 0 16px 0 20px; background: var(--bar); color: #fff; border-bottom: 1px solid rgba(255,255,255,0.08); transition: left 0.22s ease; }
.pg-logs .app-name { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 600; letter-spacing: 0.01em; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.pg-logs .rail-brand { height: var(--bar-h); flex: none; margin: 0 -9px 14px; padding: 0 9px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
.pg-logs .logo { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-style: italic; font-size: 15px; letter-spacing: 0.02em; color: #fff; transition: font-size 0.22s ease; }
.pg-logs.rail-expanded .logo { font-size: 20px; }
.pg-logs .bar-btn { width: 34px; height: 34px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: #fff; font-size: 14px; opacity: 0.9; }
.pg-logs .bar-btn:hover { background: rgba(255,255,255,0.12); opacity: 1; }
.pg-logs #roleBtn[aria-expanded="true"] { background: rgba(255,255,255,0.18); opacity: 1; }
.pg-logs .role-menu { position: absolute; top: calc(100% + 8px); right: 0; z-index: 30; min-width: 240px; padding: 6px; background: var(--surface); color: var(--text); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 18px 40px -16px rgba(15, 27, 61, 0.45); }
.pg-logs .role-head { padding: 6px 10px 8px; font-size: 10.5px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-faint); }
.pg-logs .role-opt { width: 100%; display: flex; align-items: center; gap: 10px; padding: 6px 10px 6px 6px; border-radius: 8px; font-size: 13px; text-align: left; }
.pg-logs .role-opt:hover,
.pg-logs .role-opt:focus-visible { background: var(--surface-hover); }
.pg-logs .role-opt > i:first-child { width: 28px; height: 28px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--rc); background: color-mix(in srgb, var(--rc) 13%, transparent); }
.pg-logs .role-opt.on { background: color-mix(in srgb, var(--rc) 10%, transparent); font-weight: 600; color: var(--rc); }
.pg-logs .role-opt.on > i:first-child { background: var(--rc); color: #fff; }
[data-theme="dark"] .pg-logs .role-opt.on > i:first-child { color: #0B1020; }
.pg-logs .role-check { margin-left: auto; font-size: 11px; color: var(--rc); }
.pg-logs .notif-dot { position: absolute; top: 7px; right: 8px; width: 7px; height: 7px; border-radius: 999px; background: #EF4444; box-shadow: 0 0 0 2px var(--bar); }
.pg-logs.rail-expanded { --rail-w: 232px; }
.pg-logs .rail { position: fixed; top: 0; bottom: 0; left: 0; z-index: 26; width: var(--rail-w); display: flex; flex-direction: column; gap: 6px; padding: 0 9px 14px; background: var(--bar); border-right: 1px solid rgba(255,255,255,0.08); transition: width 0.22s ease; }
.pg-logs .rail-section { padding: 2px 10px 6px; font-size: 10px; font-weight: 700; letter-spacing: 0.12em; color: rgba(255,255,255,0.4); }
.pg-logs:not(.rail-expanded) .rail-section { display: none; }
.pg-logs .rail-btn { position: relative; height: 42px; padding: 0 8px; border-radius: 10px; display: flex; align-items: center; gap: 12px; color: rgba(255,255,255,0.72); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-logs:not(.rail-expanded) .rail-btn { justify-content: center; padding: 0; }
.pg-logs .rail-btn i { width: 30px; height: 30px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; background: rgba(255,255,255,0.07); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-logs .rail-btn:hover { color: #fff; background: rgba(255,255,255,0.06); }
.pg-logs .rail-btn:hover i { background: rgba(255,255,255,0.14); }
.pg-logs .rail-btn.active { color: #fff; background: linear-gradient(90deg, rgba(96,165,250,0.22), rgba(96,165,250,0.04)); }
.pg-logs .rail-btn.active i { background: linear-gradient(135deg, #3B82F6, #60A5FA); color: #fff; box-shadow: 0 6px 14px -6px rgba(59,130,246,0.8); }
.pg-logs .rail-btn.active::before { content: ''; position: absolute; left: -9px; top: 9px; bottom: 9px; width: 3px; border-radius: 0 3px 3px 0; background: #60A5FA; }
.pg-logs .rail-label { font-size: 13px; font-weight: 500; white-space: nowrap; }
.pg-logs .rail-btn.active .rail-label { font-weight: 600; }
.pg-logs:not(.rail-expanded) .rail-label { position: absolute; left: calc(100% + 12px); top: 50%; transform: translate(-4px, -50%); padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; background: var(--text); color: var(--bg); box-shadow: 0 8px 20px -8px rgba(0,0,0,0.4); opacity: 0; pointer-events: none; transition: opacity 0.15s ease, transform 0.15s ease; }
.pg-logs:not(.rail-expanded) .rail-btn:hover .rail-label,
.pg-logs:not(.rail-expanded) .rail-btn:focus-visible .rail-label { opacity: 1; transform: translate(0, -50%); }
.pg-logs .rail-toggle { margin-top: auto; height: 32px; padding: 0 10px; border-radius: 9px; display: flex; align-items: center; gap: 12px; font-size: 12px; color: rgba(255,255,255,0.6); }
.pg-logs .rail-toggle:hover { color: #fff; background: rgba(255,255,255,0.1); }
.pg-logs .rail-toggle i { width: 14px; text-align: center; transition: transform 0.22s ease; }
.pg-logs.rail-expanded .rail-toggle i { transform: rotate(180deg); }
.pg-logs:not(.rail-expanded) .rail-toggle .rail-label { display: none; }
.pg-logs .shell { margin-left: var(--rail-w); padding: calc(var(--bar-h) + 10px) 12px 24px; min-height: 100vh; transition: margin-left 0.22s ease; }
.pg-logs .crumbbar { position: relative; overflow: hidden; display: flex; align-items: center; gap: 12px; height: 44px; padding: 0 14px 0 16px; margin-bottom: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 6px 18px -14px rgba(15, 27, 61, 0.35); }
.pg-logs .crumb-back { width: 28px; height: 28px; border-radius: 999px; flex: none; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--brand); background: var(--brand-soft); transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease; }
.pg-logs .crumb-back:hover { background: var(--brand); color: #fff; transform: translateX(-1px); }
[data-theme="dark"] .pg-logs .crumb-back:hover { color: #0B1020; }
.pg-logs .crumb-sep-v { width: 1px; height: 18px; background: var(--border); }
.pg-logs .crumb-link { display: inline-flex; align-items: center; gap: 6px; padding: 4px 8px; margin: 0 -4px; border-radius: 8px; color: var(--text-muted); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-logs .crumb-link i { font-size: 11px; }
.pg-logs .crumb-link:hover { background: var(--surface-hover); color: var(--text); }
.pg-logs .crumb-chev { font-size: 8px; color: var(--text-faint); opacity: 0.7; }
.pg-logs .crumb-current { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 999px; font-size: 12.5px; font-weight: 700; color: var(--brand); background: linear-gradient(90deg, color-mix(in srgb, #3B6CF6 12%, transparent), color-mix(in srgb, #8B5CF6 12%, transparent)); border: 1px solid color-mix(in srgb, #8B5CF6 22%, transparent); }
.pg-logs .crumb-current i { font-size: 11px; }
.pg-logs .ico { width: 17px; height: 17px; flex: none; display: inline-block; vertical-align: middle; }
.pg-logs .theme-toggle .ico-sun { display: none; }
[data-theme="dark"] .pg-logs .theme-toggle .ico-sun { display: inline-block; }
[data-theme="dark"] .pg-logs .theme-toggle .ico-moon { display: none; }
.pg-logs .toast { position: fixed; left: 50%; bottom: 24px; transform: translate(-50%, 20px); opacity: 0; z-index: 50; background: var(--text); color: var(--bg); padding: 10px 16px; border-radius: 10px; font-size: 13px; font-weight: 500; transition: opacity 0.2s ease, transform 0.2s ease; pointer-events: none; }
.pg-logs .toast.show { opacity: 1; transform: translate(-50%, 0); }
.pg-logs .vi-actions { margin-left: auto; display: flex; gap: 8px; }
.pg-logs .vbtn { display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 10px; font-size: 13px; font-weight: 600; border: 1px solid var(--border); background: var(--surface); color: var(--text); transition: background-color 0.15s ease, filter 0.15s ease; }
.pg-logs .vbtn:hover { background: var(--surface-hover); }
.pg-logs .vbtn.primary { background: var(--brand); border-color: var(--brand); color: #fff; }
.pg-logs .vbtn.primary:hover { filter: brightness(1.1); }
[data-theme="dark"] .pg-logs .vbtn.primary { color: #0B1020; }
.pg-logs .vi-summary { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-bottom: 12px; padding: 16px 20px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; }
@media (max-width: 760px) {
  .pg-logs .vi-summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
.pg-logs .sum-label { font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-faint); }
.pg-logs .sum-val { margin-top: 6px; font-size: 14px; font-weight: 600; }
.pg-logs .pill { display: inline-flex; align-items: center; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; white-space: nowrap; }
.pg-logs .avatar { width: 26px; height: 26px; border-radius: 999px; flex: none; display: inline-flex; align-items: center; justify-content: center; font-size: 10.5px; font-weight: 700; }
.pg-logs .pill-assess { color: var(--assess-fg); background: var(--assess-bg); }
.pg-logs .pill-host { color: var(--monitor-fg); background: var(--monitor-bg); }
.pg-logs .vi-jump { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.pg-logs .jump-chip { padding: 5px 12px; border-radius: 999px; font-size: 12.5px; font-weight: 500; color: var(--text-muted); background: var(--surface); border: 1px solid var(--border); transition: color 0.15s ease, border-color 0.15s ease; }
.pg-logs .jump-chip:hover { color: var(--brand); border-color: color-mix(in srgb, var(--brand) 40%, var(--border)); }
.pg-logs .sec { margin-bottom: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; scroll-margin-top: calc(var(--bar-h) + 16px); }
.pg-logs .sec-head { display: flex; align-items: center; gap: 10px; padding: 12px 16px 12px 18px; }
.pg-logs .sec:not(.collapsed) .sec-head { border-bottom: 1px solid var(--border); }
.pg-logs .sec-icon { width: 28px; height: 28px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--brand); background: var(--brand-soft); }
.pg-logs .sec-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 700; color: var(--brand); }
.pg-logs .sec-tools { margin-left: auto; display: flex; align-items: center; gap: 8px; }
.pg-logs .st-dd { position: relative; }
.pg-logs .st-dd { --st: #2563EB; }
.pg-logs .st-dd[data-state="done"] { --st: #059669; }
.pg-logs .st-dd[data-state="todo"] { --st: #6B7280; }
[data-theme="dark"] .pg-logs .st-dd { --st: #7DA2FF; }
[data-theme="dark"] .pg-logs .st-dd[data-state="done"] { --st: #34D399; }
[data-theme="dark"] .pg-logs .st-dd[data-state="todo"] { --st: #9CA3AF; }
.pg-logs .st-btn { display: inline-flex; align-items: center; gap: 7px; padding: 5px 10px 5px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; color: var(--st); background: color-mix(in srgb, var(--st) 10%, var(--surface)); border: 1px solid color-mix(in srgb, var(--st) 28%, transparent); transition: box-shadow 0.15s ease; }
.pg-logs .st-btn:hover,
.pg-logs .st-btn[aria-expanded="true"] { box-shadow: 0 0 0 3px color-mix(in srgb, var(--st) 14%, transparent); }
.pg-logs .st-btn .chev-s { font-size: 9px; opacity: 0.75; transition: transform 0.2s ease; }
.pg-logs .st-btn[aria-expanded="true"] .chev-s { transform: rotate(180deg); }
.pg-logs .st-dot { width: 7px; height: 7px; border-radius: 999px; background: currentColor; flex: none; }
.pg-logs .st-menu { position: absolute; top: calc(100% + 6px); right: 0; z-index: 15; min-width: 170px; padding: 5px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; box-shadow: 0 16px 34px -14px rgba(15, 27, 61, 0.4); }
.pg-logs .st-opt { width: 100%; display: flex; align-items: center; gap: 9px; padding: 7px 9px; border-radius: 7px; font-size: 13px; text-align: left; color: var(--text); }
.pg-logs .st-opt:hover,
.pg-logs .st-opt:focus-visible { background: var(--surface-hover); outline: none; }
.pg-logs .st-opt .st-dot { color: var(--opt); }
.pg-logs .st-opt[aria-selected="true"] { font-weight: 600; }
.pg-logs .st-opt .fa-check { margin-left: auto; font-size: 11px; color: var(--brand); }
.pg-logs .sec-toggle { width: 28px; height: 28px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 11px; }
.pg-logs .sec-toggle:hover { background: var(--surface-hover); color: var(--text); }
.pg-logs .sec-toggle i { transition: transform 0.2s ease; }
.pg-logs .sec.collapsed .sec-toggle i { transform: rotate(180deg); }
.pg-logs .sec.collapsed .sec-body { display: none; }
.pg-logs .sec-body { padding: 18px; }
.pg-logs .fields { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px 28px; }
.pg-logs .f-label { display: flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 600; color: var(--text-muted); }
.pg-logs .f-label .info { font-size: 11px; color: var(--brand); cursor: help; }
.pg-logs .f-val { margin-top: 5px; font-size: 13.5px; font-weight: 500; display: flex; align-items: center; gap: 6px; word-break: break-word; }
.pg-logs .f-val ul { list-style: disc; padding-left: 18px; }
.pg-logs .f-val .stack { display: flex; flex-direction: column; gap: 3px; }
.pg-logs .edit-btn { width: 24px; height: 24px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; color: var(--text-faint); font-size: 11px; }
.pg-logs .edit-btn:hover { background: var(--surface-hover); color: var(--brand); }
.pg-logs .tabs { display: flex; flex-wrap: wrap; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.pg-logs .tab { flex: 1 1 0; min-width: max-content; text-align: center; padding: 10px 14px; font-size: 13px; font-weight: 600; color: var(--text-muted); border-bottom: 2px solid transparent; margin-bottom: -1px; }
.pg-logs .tab:hover { color: var(--text); }
.pg-logs .tab[aria-selected="true"] { color: var(--brand); border-bottom-color: var(--brand); }
.pg-logs .tab-panel[hidden] { display: none; }
.pg-logs .dtable { width: 100%; border: 1px solid var(--border); border-radius: 10px; border-collapse: separate; border-spacing: 0; overflow: hidden; }
.pg-logs .dtable th { background: #F1F3F6; color: #1E3A8A; font-size: 11.5px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; text-align: left; padding: 10px 14px; }
[data-theme="dark"] .pg-logs .dtable th { background: #1C2235; color: #D6E4FF; }
.pg-logs .dtable td { font-size: 13px; padding: 11px 14px; border-top: 1px solid var(--border); }
.pg-logs .dtable .empty { text-align: center; color: var(--text-faint); padding: 18px; }
.pg-logs .qa { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.pg-logs .qa-row { display: grid; grid-template-columns: minmax(0, 1fr) minmax(160px, 38%); gap: 16px; padding: 11px 16px; font-size: 13px; }
.pg-logs .qa-row + .qa-row { border-top: 1px solid var(--border); }
.pg-logs .qa-q { font-weight: 500; }
.pg-logs .qa-a { word-break: break-word; }
.pg-logs .qa-row.sub { background: var(--surface-2); padding-left: 28px; box-shadow: inset 3px 0 0 var(--brand-soft); }
.pg-logs .qa-row.sub .qa-q { color: var(--text-muted); }
.pg-logs .yes { color: var(--monitor-fg); font-weight: 600; }
.pg-logs .no { color: #DC2626; font-weight: 600; }
.pg-logs .file-link { display: inline-flex; align-items: flex-start; gap: 6px; color: var(--brand); word-break: break-all; }
.pg-logs .file-link:hover { text-decoration: underline; }
.pg-logs .file-link i { margin-top: 3px; font-size: 11px; }
.pg-logs .placeholder { padding: 18px; text-align: center; font-size: 13px; color: var(--text-faint); border: 1px dashed var(--border-strong); border-radius: 10px; }
.pg-logs .tools { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; }
.pg-logs .tool { padding: 14px; border-radius: 12px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-logs .tool-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.pg-logs .tool-ico { width: 32px; height: 32px; flex: none; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; color: var(--brand); background: var(--brand-soft); }
.pg-logs .tool-name { font-size: 13.5px; font-weight: 700; }
.pg-logs .tool-sub { font-size: 11.5px; color: var(--text-faint); }
.pg-logs .kv { display: flex; justify-content: space-between; gap: 12px; padding: 6px 0; font-size: 13px; }
.pg-logs .kv + .kv { border-top: 1px dashed var(--border); }
.pg-logs .kv span,
.pg-logs .kv-label { color: var(--text-muted); }
.pg-logs .kv span { white-space: nowrap; }
.pg-logs .kv b { font-weight: 600; text-align: right; word-break: break-word; }
.pg-logs .kv b.na { color: var(--text-faint); font-weight: 500; }
.pg-logs .kv-label { margin: 8px 0 6px; font-size: 12px; font-weight: 600; }
.pg-logs .chips { display: flex; flex-wrap: wrap; gap: 6px; }
.pg-logs .chip { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px; font-size: 12.5px; background: var(--surface); border: 1px solid var(--border); }
.pg-logs .chip b { font-weight: 700; color: var(--brand); }
.pg-logs .chip i { font-size: 10.5px; color: var(--text-faint); }
.pg-logs .env-toggle { display: inline-flex; gap: 2px; margin-bottom: 14px; padding: 3px; border-radius: 999px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-logs .env-toggle button { padding: 4px 16px; border-radius: 999px; font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; color: var(--text-faint); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-logs .env-toggle button:hover { color: var(--text); }
.pg-logs .env-toggle .env-qa[aria-pressed="true"] { color: #2F5F8A; background: #DCE8F4; }
.pg-logs .env-toggle .env-prod[aria-pressed="true"] { color: #4338CA; background: #DAD8F8; }
[data-theme="dark"] .pg-logs .env-toggle .env-qa[aria-pressed="true"] { color: #9CC3E6; background: #1B2A3B; }
[data-theme="dark"] .pg-logs .env-toggle .env-prod[aria-pressed="true"] { color: #C7C4F5; background: #27245A; }
.pg-logs .vi-foot { padding: 18px 0 4px; text-align: center; font-size: 12px; color: var(--text-faint); }
.pg-logs .to-top { position: fixed; right: 22px; bottom: 22px; z-index: 20; width: 42px; height: 42px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; background: var(--brand); color: #fff; box-shadow: 0 10px 24px -10px rgba(15, 27, 61, 0.6); opacity: 0; pointer-events: none; transition: opacity 0.2s ease; }
.pg-logs .to-top.show { opacity: 1; pointer-events: auto; }
[data-theme="dark"] .pg-logs .to-top { color: #0B1020; }
.pg-logs { --grad: linear-gradient(90deg, #3B6CF6 0%, #8B5CF6 50%, #EC4899 100%); --wash: linear-gradient(100deg, #EEF3FF 0%, #F4EFFF 55%, #FDF0F7 100%); --glow: rgba(139, 92, 246, 0.28); }
[data-theme="dark"] .pg-logs { --grad: linear-gradient(90deg, #6B93FF 0%, #A78BFA 50%, #F472B6 100%); --wash: linear-gradient(100deg, #141D3F 0%, #1B1840 55%, #251633 100%); --glow: rgba(167, 139, 250, 0.3); }
.pg-logs .vi-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px; padding: 8px 12px; margin-bottom: 12px; border-radius: 16px; background: var(--wash); border: 1px solid var(--border); }
.pg-logs .title-block { display: flex; align-items: center; gap: 12px; flex: none; }
.pg-logs .title-accent { width: 4px; height: 30px; flex: none; border-radius: 999px; background: linear-gradient(180deg, #1E3A8A, #60A5FA); }
.pg-logs .vi-head h1 { font-size: 18px; font-weight: 800; letter-spacing: -0.01em; line-height: 1.2; white-space: nowrap; }
.pg-logs .vi-head .sub { font-size: 12px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pg-logs .vi-names { order: 2; flex: 1 1 0; display: flex; gap: 10px; min-width: 0; padding-left: 16px; border-left: 1px solid var(--border); }
.pg-logs .vi-name { display: flex; align-items: center; gap: 10px; flex: 0 1 auto; min-width: 0; padding: 6px 14px 6px 6px; border-radius: 12px; background: color-mix(in srgb, var(--surface) 75%, transparent); border: 1px solid color-mix(in srgb, var(--border) 80%, transparent); }
.pg-logs .vi-name-ico { width: 30px; height: 30px; flex: none; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; color: var(--ic); background: color-mix(in srgb, var(--ic) 12%, var(--surface)); }
[data-theme="dark"] .pg-logs .vi-name-ico { filter: brightness(1.5); }
.pg-logs .vi-name-txt { display: flex; flex-direction: column; min-width: 0; line-height: 1.25; }
.pg-logs .vi-name-txt span { font-size: 11px; font-weight: 500; color: var(--text-muted); }
.pg-logs .vi-name-txt b { font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pg-logs .vi-meta { order: 3; flex: 0 1 auto; min-width: 0; overflow-x: auto; scrollbar-width: none; display: grid; grid-template-columns: auto auto; align-items: center; gap: 6px 20px; padding-left: 16px; border-left: 1px solid var(--border); }
.pg-logs .meta-item { display: flex; align-items: center; gap: 7px; white-space: nowrap; }
.pg-logs .meta-item > span:first-child { font-size: 11.5px; font-weight: 500; color: var(--text-muted); }
.pg-logs .meta-item > span:first-child::after { content: ':'; }
.pg-logs .meta-item > b { font-size: 13px; font-weight: 600; }
.pg-logs .meta-item .pill { padding: 1px 9px; font-size: 11.5px; }
.pg-logs .vi-actions { order: 4; margin-left: auto; display: flex; gap: 8px; position: relative; }
.pg-logs .vi-actions > button.with-label { width: auto; gap: 7px; padding: 0 12px 0 10px; font-size: 13px; font-weight: 600; white-space: nowrap; }
.pg-logs .vi-actions > button[aria-expanded="true"] { background: var(--brand-soft); border-color: var(--brand); }
.pg-logs .vi-actions > button { width: 34px; height: 34px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; background: var(--surface); color: var(--brand); border: 1px solid var(--border); box-shadow: 0 4px 12px -8px rgba(15, 27, 61, 0.3); }
.pg-logs .vi-actions > button i,
.pg-logs .vi-actions > button .ico { transition: transform 0.15s ease; }
.pg-logs .vi-actions > button:hover i,
.pg-logs .vi-actions > button:hover .ico { transform: scale(1.2); }
.pg-logs .vi-actions .tool-download { color: #DC2626; }
[data-theme="dark"] .pg-logs .vi-actions .tool-download { color: #F87171; }
@media (max-width: 1000px) {
  .pg-logs .vi-names { order: 4; flex-basis: 100%; padding-left: 0; border-left: 0; }
  .pg-logs .vi-name { flex: 1; }
  .pg-logs .vi-meta { order: 5; flex-basis: 100%; padding-left: 0; border-left: 0; }
}
.pg-logs .pill-intake { color: var(--intake-fg); background: var(--intake-bg); }
.pg-logs .rf-hero { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px 28px; margin: 2px 0 14px; padding: 18px 22px 18px 24px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; box-shadow: inset 4px 0 0 var(--brand), 0 6px 18px -16px rgba(15, 27, 61, 0.35); }
.pg-logs .rf-title { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 17px; font-weight: 800; color: var(--brand); }
.pg-logs .rf-value { margin-top: 5px; font-size: 14px; font-weight: 600; }
.pg-logs .rf-right { text-align: right; }
.pg-logs .rf-right .rf-title { justify-content: flex-end; }
.pg-logs .pill-saas { color: #0E7490; background: color-mix(in srgb, #06B6D4 14%, var(--surface)); }
.pg-logs .pill-saasplus { color: #7C3AED; background: color-mix(in srgb, #8B5CF6 14%, var(--surface)); }
[data-theme="dark"] .pg-logs .pill-saas { color: #22D3EE; }
[data-theme="dark"] .pg-logs .pill-saasplus { color: #A78BFA; }
.pg-logs .nt-bar { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.pg-logs .nt-card { margin-bottom: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; }
.pg-logs .nt-form { padding: 20px 22px 0; }
.pg-logs .nt-form[hidden] { display: none; }
.pg-logs .nt-form-title { display: flex; align-items: center; gap: 10px; padding-bottom: 14px; margin-bottom: 18px; border-bottom: 1px solid var(--border); font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 700; color: var(--brand); }
.pg-logs .nt-row { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 8px 24px; margin-bottom: 18px; }
@media (max-width: 760px) {
  .pg-logs .nt-row { grid-template-columns: minmax(0, 1fr); }
}
.pg-logs .nt-label { padding-top: 10px; font-size: 13px; font-weight: 600; color: var(--text-muted); }
.pg-logs .nt-label .req { color: #DC2626; }
.pg-logs .inp { width: 100%; height: 40px; padding: 0 12px; border-radius: 9px; font-size: 13px; color: var(--text); background: var(--surface-2); border: 1px solid var(--border); transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease; }
.pg-logs textarea.inp { height: auto; min-height: 110px; padding: 10px 12px; resize: vertical; line-height: 1.5; }
.pg-logs select.inp { appearance: none; padding-right: 34px; cursor: pointer; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; }
.pg-logs .inp::placeholder { color: var(--text-faint); }
.pg-logs .inp:hover { border-color: var(--border-strong); }
.pg-logs .inp:focus { outline: none; background-color: var(--surface); border-color: var(--brand); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 16%, transparent); }
.pg-logs .inp.invalid { border-color: #DC2626; box-shadow: 0 0 0 3px color-mix(in srgb, #DC2626 14%, transparent); }
[data-theme="dark"] .pg-logs .inp { color-scheme: dark; }
.pg-logs .hint { margin-top: 7px; font-size: 12px; font-weight: 600; line-height: 1.6; color: var(--brand); }
.pg-logs .err { margin-top: 6px; font-size: 12px; font-weight: 600; color: #DC2626; }
.pg-logs .err[hidden] { display: none; }
.pg-logs .char-count { float: right; font-weight: 500; color: var(--text-faint); }
.pg-logs .drop { display: flex; align-items: center; gap: 14px; padding: 14px 16px; border-radius: 11px; cursor: pointer; border: 1.5px dashed color-mix(in srgb, var(--brand) 45%, var(--border)); background: color-mix(in srgb, var(--brand) 4%, var(--surface)); transition: background-color 0.15s ease, border-color 0.15s ease; }
.pg-logs .drop:hover,
.pg-logs .drop.over { border-color: var(--brand); background: color-mix(in srgb, var(--brand) 9%, var(--surface)); }
.pg-logs .drop-ico { width: 38px; height: 38px; flex: none; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; font-size: 15px; color: var(--brand); background: var(--brand-soft); }
.pg-logs .drop-text { font-size: 13px; color: var(--text-muted); }
.pg-logs .drop-text b { color: var(--brand); font-weight: 700; }
.pg-logs .drop-count { margin-left: auto; font-size: 12px; font-weight: 600; color: var(--text-faint); white-space: nowrap; }
.pg-logs .files { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.pg-logs .file-chip { display: inline-flex; align-items: center; gap: 8px; max-width: 100%; padding: 5px 6px 5px 10px; border-radius: 9px; font-size: 12.5px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-logs .file-chip i.ft { color: var(--brand); }
.pg-logs .file-chip .fn { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 260px; font-weight: 500; }
.pg-logs .file-chip .fs { color: var(--text-faint); font-size: 11.5px; }
.pg-logs .file-chip button { width: 22px; height: 22px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; color: var(--text-faint); }
.pg-logs .file-chip button:hover { color: #DC2626; background: color-mix(in srgb, #EF4444 12%, var(--surface)); }
.pg-logs .nt-actions { display: flex; justify-content: flex-end; gap: 10px; padding: 14px 0 18px; margin-top: 4px; border-top: 1px solid var(--border); }
.pg-logs .vbtn:disabled { opacity: 0.5; cursor: not-allowed; }
.pg-logs .nl-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; padding: 14px 18px; border-bottom: 1px solid var(--border); }
.pg-logs .nl-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 700; color: var(--brand); }
.pg-logs .nl-count { padding: 2px 9px; border-radius: 999px; font-size: 11.5px; font-weight: 700; color: var(--brand); background: var(--brand-soft); }
.pg-logs .nl-filter { margin-left: auto; display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; color: var(--text-muted); }
.pg-logs .nl-filter .inp { width: 200px; height: 36px; }
.pg-logs .nl-body { padding: 16px 18px; min-height: 280px; }
.pg-logs .nl-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; min-height: 250px; font-size: 14.5px; color: var(--text-faint); }
.pg-logs .nl-empty i { font-size: 40px; opacity: 0.55; }
.pg-logs .notes { display: flex; flex-direction: column; gap: 12px; }
.pg-logs .note-item { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 12px; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--border); background: color-mix(in srgb, var(--surface-2) 50%, var(--surface)); animation: noteIn 0.25s ease; }
@keyframes noteIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
.pg-logs .note-av { width: 34px; height: 34px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; font-size: 11.5px; font-weight: 700; color: #fff; background: var(--rc); }
.pg-logs .note-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; font-size: 12.5px; color: var(--text-muted); }
.pg-logs .note-meta b { color: var(--text); font-weight: 700; font-size: 13px; }
.pg-logs .note-type { padding: 2px 8px; border-radius: 6px; font-size: 10.5px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--brand); background: var(--brand-soft); }
.pg-logs .note-time { margin-left: auto; font-size: 12px; color: var(--text-faint); }
.pg-logs .note-text { margin-top: 6px; font-size: 13.5px; line-height: 1.55; white-space: pre-wrap; word-break: break-word; }
.pg-logs .note-files { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.pg-logs .note-files a { display: inline-flex; align-items: center; gap: 6px; padding: 3px 9px; border-radius: 7px; font-size: 12px; color: var(--brand); background: var(--surface); border: 1px solid var(--border); }
.pg-logs .note-files a:hover { border-color: var(--brand); }
.pg-logs { --th-bg: linear-gradient(180deg, #F5F8FF 0%, #EAF0FC 100%); --th-fg: #1E3A8A; --th-line: #D5DFF3; }
[data-theme="dark"] .pg-logs { --th-bg: linear-gradient(180deg, #1C2646 0%, #172039 100%); --th-fg: #C9D7FF; --th-line: #2B3760; }
.pg-logs .lg-tools { margin-left: auto; display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.pg-logs .lg-bar { display: flex; align-items: center; height: 38px; border-radius: 999px; border: 1.5px solid transparent; background: linear-gradient(var(--surface), var(--surface)) padding-box, var(--grad) border-box; box-shadow: 0 8px 22px -14px var(--glow); transition: box-shadow 0.2s ease; }
.pg-logs .lg-bar:focus-within { box-shadow: 0 0 0 4px color-mix(in srgb, #8B5CF6 16%, transparent), 0 10px 28px -12px var(--glow); }
.pg-logs .lg-search { display: flex; align-items: center; gap: 9px; padding: 0 12px 0 14px; }
.pg-logs .lg-search > i { font-size: 13px; background: var(--grad); -webkit-background-clip: text; background-clip: text; color: transparent; }
.pg-logs .lg-search input { width: 220px; height: 34px; font-size: 13px; background: transparent; outline: none; color: var(--text); }
.pg-logs .lg-search input::placeholder { color: var(--text-faint); }
.pg-logs .lg-div { width: 1px; height: 20px; background: var(--border); }
.pg-logs .lg-bar .csel-btn.lg-type { width: 170px; height: 34px; padding: 0 14px 0 12px; border: 0; border-radius: 0 999px 999px 0; background: transparent; box-shadow: none !important; font-size: 13px; font-weight: 600; color: var(--text); }
.pg-logs .lg-bar .csel-btn.lg-type::before { content: '\f0b0'; font-family: 'Font Awesome 6 Free'; font-weight: 900; font-size: 11px; color: var(--brand); }
.pg-logs .lg-bar .csel-btn.lg-type:hover { background: var(--surface-hover); }
@media (max-width: 640px) {
  .pg-logs .lg-search input { width: 140px; }
  .pg-logs .lg-bar .csel-btn.lg-type { width: 140px; }
}
.pg-logs .lg-wrap { height: 560px; overflow: auto; }
.pg-logs .ltable { width: 100%; min-width: 1080px; table-layout: fixed; border-collapse: separate; border-spacing: 0; font-size: 13px; }
.pg-logs .ltable thead th { position: sticky; top: 0; z-index: 2; text-align: left; padding: 11px 14px; color: var(--th-fg); background: var(--th-bg); font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12.5px; font-weight: 600; border-bottom: 1px solid var(--th-line); white-space: nowrap; }
.pg-logs .ltable th.sortable { cursor: pointer; user-select: none; }
.pg-logs .ltable th.sortable i { margin-left: 5px; font-size: 10px; opacity: 0.8; }
.pg-logs .ltable td { padding: 12px 14px; vertical-align: top; border-bottom: 1px solid var(--border); word-break: break-word; line-height: 1.5; }
.pg-logs .ltable tbody tr:hover td { background: var(--surface-hover); }
.pg-logs .lg-date { font-size: 12.5px; color: var(--text-muted); white-space: nowrap; }
.pg-logs .lg-date b { display: block; font-weight: 600; color: var(--text); }
.pg-logs .lg-who { font-weight: 600; word-break: normal; }
.pg-logs .lg-old { color: var(--text-muted); }
.pg-logs .lg-none { color: var(--text-faint); }
.pg-logs .lg-arrow { color: var(--text-faint); font-size: 10px; margin: 0 4px; }
.pg-logs .lg-type-pill { display: inline-flex; align-items: center; gap: 6px; padding: 3px 9px; border-radius: 999px; font-size: 11.5px; font-weight: 600; white-space: nowrap; color: var(--tc); background: color-mix(in srgb, var(--tc) 11%, var(--surface)); }
.pg-logs .lg-type-pill i { font-size: 10px; }
.pg-logs .lg-role { font-size: 12.5px; color: var(--text-muted); }
.pg-logs .lg-mail b { font-weight: 600; color: var(--text-muted); }
.pg-logs .lg-mail .addr { color: var(--brand); }
.pg-logs .lg-more { max-height: 92px; overflow-y: auto; padding-right: 6px; scrollbar-width: thin; }
.pg-logs .lg-links { display: flex; gap: 14px; margin-top: 6px; }
.pg-logs .lg-links button { white-space: nowrap; display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 600; color: var(--brand); }
.pg-logs .lg-links button:hover { text-decoration: underline; }
.pg-logs .lg-foot { display: flex; justify-content: space-between; padding: 10px 18px; font-size: 12px; color: var(--text-faint); border-top: 1px solid var(--border); }
.pg-logs .csel { position: relative; }
.pg-logs .csel-btn { display: flex; align-items: center; gap: 9px; width: 100%; text-align: left; cursor: pointer; }
.pg-logs .csel-btn .csel-val { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pg-logs .csel-btn .chev { font-size: 10px; color: var(--text-faint); transition: transform 0.2s ease; }
.pg-logs .csel-btn[aria-expanded="true"] { border-color: var(--brand); background: var(--surface); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 16%, transparent); }
.pg-logs .csel-btn[aria-expanded="true"] .chev { transform: rotate(180deg); }
.pg-logs .csel-dot { width: 8px; height: 8px; flex: none; border-radius: 999px; background: var(--oc); box-shadow: 0 0 0 3px color-mix(in srgb, var(--oc) 18%, transparent); }
.pg-logs .csel-menu { position: fixed; z-index: 60; padding: 5px; max-height: 280px; overflow-y: auto; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 18px 40px -16px rgba(15, 27, 61, 0.45); animation: cselIn 0.14s ease; }
@keyframes cselIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
.pg-logs .csel-opt { width: 100%; display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 8px; font-size: 13px; text-align: left; color: var(--text); }
.pg-logs .csel-opt:hover,
.pg-logs .csel-opt.active { background: var(--surface-hover); }
.pg-logs .csel-opt[aria-selected="true"] { font-weight: 600; color: var(--brand); background: var(--brand-soft); }
.pg-logs .csel-opt small { display: block; font-size: 11.5px; font-weight: 400; color: var(--text-faint); }
.pg-logs .csel-opt .fa-check { margin-left: auto; font-size: 11px; }
.pg-logs .csel-opt { font-weight: 500; }
.pg-logs .ui-tip { position: fixed; z-index: 70; max-width: 260px; padding: 6px 10px; border-radius: 8px; font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 500; line-height: 1.35; text-align: center; color: #fff; background: #0F1B3D; box-shadow: 0 10px 24px -10px rgba(0, 0, 0, 0.45); pointer-events: none; opacity: 0; transform: translateY(3px); transition: opacity 0.12s ease, transform 0.12s ease; }
.pg-logs .ui-tip.below { transform: translateY(-3px); }
.pg-logs .ui-tip.show { opacity: 1; transform: none; }
.pg-logs .ui-tip::after { content: ''; position: absolute; left: calc(var(--ax, 50%) - 4px); bottom: -4px; width: 8px; height: 8px; background: inherit; transform: rotate(45deg); }
.pg-logs .ui-tip.below::after { bottom: auto; top: -4px; }
[data-theme="dark"] .pg-logs .ui-tip { color: #0F1B3D; background: #E6EAF5; }
.pg-logs .vi-head > .vi-names:first-child { padding-left: 0; border-left: 0; }
