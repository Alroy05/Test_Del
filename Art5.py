/* Styles from the new-request.html design, scoped to this page (.pg-request-add) */
.pg-request-add { --bg: #FFFFFF; --surface: #FFFFFF; --surface-2: #F9FAFD; --surface-hover: #F3F5FB; --border: #E6E9F2; --border-strong: #D5DAE7; --text: #0F1B3D; --text-muted: #5B6785; --text-faint: #8A94AD; --brand: #1E3A8A; --brand-soft: #E8EEFF; --focus: #3B6CF6; --shadow: 0 1px 2px rgba(15, 27, 61, 0.04), 0 8px 24px -16px rgba(15, 27, 61, 0.18); --scrim: rgba(15, 27, 61, 0.35); --intake-fg: #B45309; --intake-bg: #FEF3E2; --assess-fg: #1D4ED8; --assess-bg: #E7EEFF; --monitor-fg: #047857; --monitor-bg: #E2F6EE; --warn-fg: #B45309; --warn-bg: #FEF3E2; --pink-fg: #BE185D; --pink-bg: #FCE7F1; --done: #10B981; --active: #3B6CF6; }
[data-theme="dark"] .pg-request-add { --bg: #0F172B; --surface: #121831; --surface-2: #0F1529; --surface-hover: #182040; --border: #232B45; --border-strong: #2F3958; --text: #E6EAF5; --text-muted: #A3AEC8; --text-faint: #6F7A96; --brand: #7DA2FF; --brand-soft: #1B2547; --focus: #7DA2FF; --shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 8px 24px -16px rgba(0, 0, 0, 0.7); --scrim: rgba(0, 0, 0, 0.55); --intake-fg: #FBBF24; --intake-bg: #33260E; --assess-fg: #8DB0FF; --assess-bg: #18264D; --monitor-fg: #4ADE9F; --monitor-bg: #0F2F25; --warn-fg: #FBBF24; --warn-bg: #33260E; --pink-fg: #F472B6; --pink-bg: #3A1530; --done: #34D399; --active: #7DA2FF; }
.pg-request-add * { -webkit-tap-highlight-color: transparent; }
.pg-request-add { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); transition: background-color 0.25s ease, color 0.25s ease; }
.pg-request-add.no-scroll { overflow: hidden; }
.pg-request-add h1,
.pg-request-add h2,
.pg-request-add .display { font-family: 'Plus Jakarta Sans', sans-serif; }
.pg-request-add .mono { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 12px; }
.pg-request-add .muted { color: var(--text-muted); }
.pg-request-add .faint { color: var(--text-faint); }
.pg-request-add :focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; border-radius: 8px; }
.pg-request-add .surface { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); }
.pg-request-add { --bar: #0B2A7A; --bar-h: 52px; --rail-w: 64px; }
[data-theme="dark"] .pg-request-add { --bar: #0A1636; }
.pg-request-add .appbar { position: fixed; top: 0; left: var(--rail-w); right: 0; z-index: 25; height: var(--bar-h); display: flex; align-items: center; padding: 0 16px 0 20px; background: var(--bar); color: #fff; border-bottom: 1px solid rgba(255,255,255,0.08); transition: left 0.22s ease; }
.pg-request-add .app-name { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 600; letter-spacing: 0.01em; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.pg-request-add .rail-brand { height: var(--bar-h); flex: none; margin: 0 -9px 14px; padding: 0 9px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid rgba(255,255,255,0.08); }
.pg-request-add .logo { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-style: italic; font-size: 15px; letter-spacing: 0.02em; color: #fff; transition: font-size 0.22s ease; }
.pg-request-add.rail-expanded .logo { font-size: 20px; }
.pg-request-add .bar-btn { width: 34px; height: 34px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: #fff; font-size: 14px; opacity: 0.9; }
.pg-request-add .bar-btn:hover { background: rgba(255,255,255,0.12); opacity: 1; }
.pg-request-add #roleBtn[aria-expanded="true"] { background: rgba(255,255,255,0.18); opacity: 1; }
.pg-request-add .role-menu { position: absolute; top: calc(100% + 8px); right: 0; z-index: 30; min-width: 240px; padding: 6px; background: var(--surface); color: var(--text); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 18px 40px -16px rgba(15, 27, 61, 0.45); }
.pg-request-add .role-head { padding: 6px 10px 8px; font-size: 10.5px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-faint); }
.pg-request-add .role-opt { width: 100%; display: flex; align-items: center; gap: 10px; padding: 6px 10px 6px 6px; border-radius: 8px; font-size: 13px; text-align: left; }
.pg-request-add .role-opt:hover,
.pg-request-add .role-opt:focus-visible { background: var(--surface-hover); }
.pg-request-add .role-opt > i:first-child { width: 28px; height: 28px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--rc); background: color-mix(in srgb, var(--rc) 13%, transparent); }
.pg-request-add .role-opt.on { background: color-mix(in srgb, var(--rc) 10%, transparent); font-weight: 600; color: var(--rc); }
.pg-request-add .role-opt.on > i:first-child { background: var(--rc); color: #fff; }
[data-theme="dark"] .pg-request-add .role-opt.on > i:first-child { color: #0B1020; }
.pg-request-add .role-check { margin-left: auto; font-size: 11px; color: var(--rc); }
.pg-request-add .notif-dot { position: absolute; top: 7px; right: 8px; width: 7px; height: 7px; border-radius: 999px; background: #EF4444; box-shadow: 0 0 0 2px var(--bar); }
.pg-request-add.rail-expanded { --rail-w: 232px; }
.pg-request-add .rail { position: fixed; top: 0; bottom: 0; left: 0; z-index: 26; width: var(--rail-w); display: flex; flex-direction: column; gap: 6px; padding: 0 9px 14px; background: var(--bar); border-right: 1px solid rgba(255,255,255,0.08); transition: width 0.22s ease; }
.pg-request-add .rail-section { padding: 2px 10px 6px; font-size: 10px; font-weight: 700; letter-spacing: 0.12em; color: rgba(255,255,255,0.4); }
.pg-request-add:not(.rail-expanded) .rail-section { display: none; }
.pg-request-add .rail-btn { position: relative; height: 42px; padding: 0 8px; border-radius: 10px; display: flex; align-items: center; gap: 12px; color: rgba(255,255,255,0.72); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-request-add:not(.rail-expanded) .rail-btn { justify-content: center; padding: 0; }
.pg-request-add .rail-btn i { width: 30px; height: 30px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; background: rgba(255,255,255,0.07); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-request-add .rail-btn:hover { color: #fff; background: rgba(255,255,255,0.06); }
.pg-request-add .rail-btn:hover i { background: rgba(255,255,255,0.14); }
.pg-request-add .rail-btn.active { color: #fff; background: linear-gradient(90deg, rgba(96,165,250,0.22), rgba(96,165,250,0.04)); }
.pg-request-add .rail-btn.active i { background: linear-gradient(135deg, #3B82F6, #60A5FA); color: #fff; box-shadow: 0 6px 14px -6px rgba(59,130,246,0.8); }
.pg-request-add .rail-btn.active::before { content: ''; position: absolute; left: -9px; top: 9px; bottom: 9px; width: 3px; border-radius: 0 3px 3px 0; background: #60A5FA; }
.pg-request-add .rail-label { font-size: 13px; font-weight: 500; white-space: nowrap; }
.pg-request-add .rail-btn.active .rail-label { font-weight: 600; }
.pg-request-add:not(.rail-expanded) .rail-label { position: absolute; left: calc(100% + 12px); top: 50%; transform: translate(-4px, -50%); padding: 6px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; background: var(--text); color: var(--bg); box-shadow: 0 8px 20px -8px rgba(0,0,0,0.4); opacity: 0; pointer-events: none; transition: opacity 0.15s ease, transform 0.15s ease; }
.pg-request-add:not(.rail-expanded) .rail-btn:hover .rail-label,
.pg-request-add:not(.rail-expanded) .rail-btn:focus-visible .rail-label { opacity: 1; transform: translate(0, -50%); }
.pg-request-add .rail-toggle { margin-top: auto; height: 32px; padding: 0 10px; border-radius: 9px; display: flex; align-items: center; gap: 12px; font-size: 12px; color: rgba(255,255,255,0.6); }
.pg-request-add .rail-toggle:hover { color: #fff; background: rgba(255,255,255,0.1); }
.pg-request-add .rail-toggle i { width: 14px; text-align: center; transition: transform 0.22s ease; }
.pg-request-add.rail-expanded .rail-toggle i { transform: rotate(180deg); }
.pg-request-add:not(.rail-expanded) .rail-toggle .rail-label { display: none; }
.pg-request-add .shell { margin-left: var(--rail-w); padding: calc(var(--bar-h) + 10px) 12px 24px; min-height: 100vh; transition: margin-left 0.22s ease; }
.pg-request-add .crumbbar { position: relative; overflow: hidden; display: flex; align-items: center; gap: 12px; height: 44px; padding: 0 14px 0 16px; margin-bottom: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 6px 18px -14px rgba(15, 27, 61, 0.35); }
.pg-request-add .crumb-back { width: 28px; height: 28px; border-radius: 999px; flex: none; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--brand); background: var(--brand-soft); transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease; }
.pg-request-add .crumb-back:hover { background: var(--brand); color: #fff; transform: translateX(-1px); }
[data-theme="dark"] .pg-request-add .crumb-back:hover { color: #0B1020; }
.pg-request-add .crumb-sep-v { width: 1px; height: 18px; background: var(--border); }
.pg-request-add .crumb-link { display: inline-flex; align-items: center; gap: 6px; padding: 4px 8px; margin: 0 -4px; border-radius: 8px; color: var(--text-muted); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-request-add .crumb-link i { font-size: 11px; }
.pg-request-add .crumb-link:hover { background: var(--surface-hover); color: var(--text); }
.pg-request-add .crumb-chev { font-size: 8px; color: var(--text-faint); opacity: 0.7; }
.pg-request-add .crumb-current { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 999px; font-size: 12.5px; font-weight: 700; color: var(--brand); background: linear-gradient(90deg, color-mix(in srgb, #3B6CF6 12%, transparent), color-mix(in srgb, #8B5CF6 12%, transparent)); border: 1px solid color-mix(in srgb, #8B5CF6 22%, transparent); }
.pg-request-add .crumb-current i { font-size: 11px; }
.pg-request-add .ico { width: 17px; height: 17px; flex: none; display: inline-block; vertical-align: middle; }
.pg-request-add .theme-toggle .ico-sun { display: none; }
[data-theme="dark"] .pg-request-add .theme-toggle .ico-sun { display: inline-block; }
[data-theme="dark"] .pg-request-add .theme-toggle .ico-moon { display: none; }
.pg-request-add .toast { position: fixed; left: 50%; bottom: 24px; transform: translate(-50%, 20px); opacity: 0; z-index: 50; background: var(--text); color: var(--bg); padding: 10px 16px; border-radius: 10px; font-size: 13px; font-weight: 500; transition: opacity 0.2s ease, transform 0.2s ease; pointer-events: none; }
.pg-request-add .toast.show { opacity: 1; transform: translate(-50%, 0); }
.pg-request-add .vi-actions { margin-left: auto; display: flex; gap: 8px; }
.pg-request-add .vbtn { display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 10px; font-size: 13px; font-weight: 600; border: 1px solid var(--border); background: var(--surface); color: var(--text); transition: background-color 0.15s ease, filter 0.15s ease; }
.pg-request-add .vbtn:hover { background: var(--surface-hover); }
.pg-request-add .vbtn.primary { background: var(--brand); border-color: var(--brand); color: #fff; }
.pg-request-add .vbtn.primary:hover { filter: brightness(1.1); }
[data-theme="dark"] .pg-request-add .vbtn.primary { color: #0B1020; }
.pg-request-add .vi-summary { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-bottom: 12px; padding: 16px 20px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; }
@media (max-width: 760px) {
  .pg-request-add .vi-summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
.pg-request-add .sum-label { font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-faint); }
.pg-request-add .sum-val { margin-top: 6px; font-size: 14px; font-weight: 600; }
.pg-request-add .pill { display: inline-flex; align-items: center; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; white-space: nowrap; }
.pg-request-add .avatar { width: 26px; height: 26px; border-radius: 999px; flex: none; display: inline-flex; align-items: center; justify-content: center; font-size: 10.5px; font-weight: 700; }
.pg-request-add .pill-assess { color: var(--assess-fg); background: var(--assess-bg); }
.pg-request-add .pill-host { color: var(--monitor-fg); background: var(--monitor-bg); }
.pg-request-add .vi-jump { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
.pg-request-add .jump-chip { padding: 5px 12px; border-radius: 999px; font-size: 12.5px; font-weight: 500; color: var(--text-muted); background: var(--surface); border: 1px solid var(--border); transition: color 0.15s ease, border-color 0.15s ease; }
.pg-request-add .jump-chip:hover { color: var(--brand); border-color: color-mix(in srgb, var(--brand) 40%, var(--border)); }
.pg-request-add .sec { margin-bottom: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; scroll-margin-top: calc(var(--bar-h) + 16px); }
.pg-request-add .sec-head { display: flex; align-items: center; gap: 10px; padding: 12px 16px 12px 18px; }
.pg-request-add .sec:not(.collapsed) .sec-head { border-bottom: 1px solid var(--border); }
.pg-request-add .sec-icon { width: 28px; height: 28px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--brand); background: var(--brand-soft); }
.pg-request-add .sec-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 700; color: var(--brand); }
.pg-request-add .sec-tools { margin-left: auto; display: flex; align-items: center; gap: 8px; }
.pg-request-add .st-dd { position: relative; }
.pg-request-add .st-dd { --st: #2563EB; }
.pg-request-add .st-dd[data-state="done"] { --st: #059669; }
.pg-request-add .st-dd[data-state="todo"] { --st: #6B7280; }
[data-theme="dark"] .pg-request-add .st-dd { --st: #7DA2FF; }
[data-theme="dark"] .pg-request-add .st-dd[data-state="done"] { --st: #34D399; }
[data-theme="dark"] .pg-request-add .st-dd[data-state="todo"] { --st: #9CA3AF; }
.pg-request-add .st-btn { display: inline-flex; align-items: center; gap: 7px; padding: 5px 10px 5px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; color: var(--st); background: color-mix(in srgb, var(--st) 10%, var(--surface)); border: 1px solid color-mix(in srgb, var(--st) 28%, transparent); transition: box-shadow 0.15s ease; }
.pg-request-add .st-btn:hover,
.pg-request-add .st-btn[aria-expanded="true"] { box-shadow: 0 0 0 3px color-mix(in srgb, var(--st) 14%, transparent); }
.pg-request-add .st-btn .chev-s { font-size: 9px; opacity: 0.75; transition: transform 0.2s ease; }
.pg-request-add .st-btn[aria-expanded="true"] .chev-s { transform: rotate(180deg); }
.pg-request-add .st-dot { width: 7px; height: 7px; border-radius: 999px; background: currentColor; flex: none; }
.pg-request-add .st-menu { position: absolute; top: calc(100% + 6px); right: 0; z-index: 15; min-width: 170px; padding: 5px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; box-shadow: 0 16px 34px -14px rgba(15, 27, 61, 0.4); }
.pg-request-add .st-opt { width: 100%; display: flex; align-items: center; gap: 9px; padding: 7px 9px; border-radius: 7px; font-size: 13px; text-align: left; color: var(--text); }
.pg-request-add .st-opt:hover,
.pg-request-add .st-opt:focus-visible { background: var(--surface-hover); outline: none; }
.pg-request-add .st-opt .st-dot { color: var(--opt); }
.pg-request-add .st-opt[aria-selected="true"] { font-weight: 600; }
.pg-request-add .st-opt .fa-check { margin-left: auto; font-size: 11px; color: var(--brand); }
.pg-request-add .sec-toggle { width: 28px; height: 28px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 11px; }
.pg-request-add .sec-toggle:hover { background: var(--surface-hover); color: var(--text); }
.pg-request-add .sec-toggle i { transition: transform 0.2s ease; }
.pg-request-add .sec.collapsed .sec-toggle i { transform: rotate(180deg); }
.pg-request-add .sec.collapsed .sec-body { display: none; }
.pg-request-add .sec-body { padding: 18px; }
.pg-request-add .fields { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px 28px; }
.pg-request-add .f-label { display: flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 600; color: var(--text-muted); }
.pg-request-add .f-label .info { font-size: 11px; color: var(--brand); cursor: help; }
.pg-request-add .f-val { margin-top: 5px; font-size: 13.5px; font-weight: 500; display: flex; align-items: center; gap: 6px; word-break: break-word; }
.pg-request-add .f-val ul { list-style: disc; padding-left: 18px; }
.pg-request-add .f-val .stack { display: flex; flex-direction: column; gap: 3px; }
.pg-request-add .edit-btn { width: 24px; height: 24px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; color: var(--text-faint); font-size: 11px; }
.pg-request-add .edit-btn:hover { background: var(--surface-hover); color: var(--brand); }
.pg-request-add .tabs { display: flex; flex-wrap: wrap; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.pg-request-add .tab { flex: 1 1 0; min-width: max-content; text-align: center; padding: 10px 14px; font-size: 13px; font-weight: 600; color: var(--text-muted); border-bottom: 2px solid transparent; margin-bottom: -1px; }
.pg-request-add .tab:hover { color: var(--text); }
.pg-request-add .tab[aria-selected="true"] { color: var(--brand); border-bottom-color: var(--brand); }
.pg-request-add .tab-panel[hidden] { display: none; }
.pg-request-add .dtable { width: 100%; border: 1px solid var(--border); border-radius: 10px; border-collapse: separate; border-spacing: 0; overflow: hidden; }
.pg-request-add .dtable th { background: #F1F3F6; color: #1E3A8A; font-size: 11.5px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; text-align: left; padding: 10px 14px; }
[data-theme="dark"] .pg-request-add .dtable th { background: #1C2235; color: #D6E4FF; }
.pg-request-add .dtable td { font-size: 13px; padding: 11px 14px; border-top: 1px solid var(--border); }
.pg-request-add .dtable .empty { text-align: center; color: var(--text-faint); padding: 18px; }
.pg-request-add .qa { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.pg-request-add .qa-row { display: grid; grid-template-columns: minmax(0, 1fr) minmax(160px, 38%); gap: 16px; padding: 11px 16px; font-size: 13px; }
.pg-request-add .qa-row + .qa-row { border-top: 1px solid var(--border); }
.pg-request-add .qa-q { font-weight: 500; }
.pg-request-add .qa-a { word-break: break-word; }
.pg-request-add .qa-row.sub { background: var(--surface-2); padding-left: 28px; box-shadow: inset 3px 0 0 var(--brand-soft); }
.pg-request-add .qa-row.sub .qa-q { color: var(--text-muted); }
.pg-request-add .yes { color: var(--monitor-fg); font-weight: 600; }
.pg-request-add .no { color: #DC2626; font-weight: 600; }
.pg-request-add .file-link { display: inline-flex; align-items: flex-start; gap: 6px; color: var(--brand); word-break: break-all; }
.pg-request-add .file-link:hover { text-decoration: underline; }
.pg-request-add .file-link i { margin-top: 3px; font-size: 11px; }
.pg-request-add .placeholder { padding: 18px; text-align: center; font-size: 13px; color: var(--text-faint); border: 1px dashed var(--border-strong); border-radius: 10px; }
.pg-request-add .tools { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; }
.pg-request-add .tool { padding: 14px; border-radius: 12px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-request-add .tool-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.pg-request-add .tool-ico { width: 32px; height: 32px; flex: none; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; color: var(--brand); background: var(--brand-soft); }
.pg-request-add .tool-name { font-size: 13.5px; font-weight: 700; }
.pg-request-add .tool-sub { font-size: 11.5px; color: var(--text-faint); }
.pg-request-add .kv { display: flex; justify-content: space-between; gap: 12px; padding: 6px 0; font-size: 13px; }
.pg-request-add .kv + .kv { border-top: 1px dashed var(--border); }
.pg-request-add .kv span,
.pg-request-add .kv-label { color: var(--text-muted); }
.pg-request-add .kv span { white-space: nowrap; }
.pg-request-add .kv b { font-weight: 600; text-align: right; word-break: break-word; }
.pg-request-add .kv b.na { color: var(--text-faint); font-weight: 500; }
.pg-request-add .kv-label { margin: 8px 0 6px; font-size: 12px; font-weight: 600; }
.pg-request-add .chips { display: flex; flex-wrap: wrap; gap: 6px; }
.pg-request-add .chip { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px; font-size: 12.5px; background: var(--surface); border: 1px solid var(--border); }
.pg-request-add .chip b { font-weight: 700; color: var(--brand); }
.pg-request-add .chip i { font-size: 10.5px; color: var(--text-faint); }
.pg-request-add .env-toggle { display: inline-flex; gap: 2px; margin-bottom: 14px; padding: 3px; border-radius: 999px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-request-add .env-toggle button { padding: 4px 16px; border-radius: 999px; font-size: 11.5px; font-weight: 700; letter-spacing: 0.08em; color: var(--text-faint); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-request-add .env-toggle button:hover { color: var(--text); }
.pg-request-add .env-toggle .env-qa[aria-pressed="true"] { color: #2F5F8A; background: #DCE8F4; }
.pg-request-add .env-toggle .env-prod[aria-pressed="true"] { color: #4338CA; background: #DAD8F8; }
[data-theme="dark"] .pg-request-add .env-toggle .env-qa[aria-pressed="true"] { color: #9CC3E6; background: #1B2A3B; }
[data-theme="dark"] .pg-request-add .env-toggle .env-prod[aria-pressed="true"] { color: #C7C4F5; background: #27245A; }
.pg-request-add .vi-foot { padding: 18px 0 4px; text-align: center; font-size: 12px; color: var(--text-faint); }
.pg-request-add .to-top { position: fixed; right: 22px; bottom: 22px; z-index: 20; width: 42px; height: 42px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; background: var(--brand); color: #fff; box-shadow: 0 10px 24px -10px rgba(15, 27, 61, 0.6); opacity: 0; pointer-events: none; transition: opacity 0.2s ease; }
.pg-request-add .to-top.show { opacity: 1; pointer-events: auto; }
[data-theme="dark"] .pg-request-add .to-top { color: #0B1020; }
.pg-request-add .select-card { border: 2px solid transparent; transition: all 0.2s ease; }
.pg-request-add .select-card.active { border-color: #3b82f6; background-color: #eff6ff; }
[data-theme="dark"] .pg-request-add .select-card.active { background-color: rgba(37, 99, 235, 0.1); }
.pg-request-add .form-label { font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 6px; }
[data-theme="dark"] .pg-request-add .form-label { color: #94a3b8; }
.pg-request-add .form-input { width: 100%; height: 42px; padding: 0 1rem; border-radius: 0.75rem; border: 1px solid #e2e8f0; background-color: #fff; font-size: 14px; transition: all 0.2s ease; }
[data-theme="dark"] .pg-request-add .form-input { border-color: #334155; background-color: #0f172a; color: #f1f5f9; }
.pg-request-add .form-input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }
.pg-request-add .info-btn { color: #94a3b8; cursor: pointer; transition: color 0.2s; }
.pg-request-add .info-btn:hover { color: #3b82f6; }
.pg-request-add .required-star { color: #ef4444; margin-left: 2px; }
.pg-request-add,
.pg-request-add { width: 100%; max-width: 100%; overflow-x: hidden; }
.pg-request-add .animate-fade-in { animation: fadeIn 0.3s ease-out; }
@keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }
.pg-request-add .ui-tip { position: fixed; z-index: 70; max-width: 260px; padding: 6px 10px; border-radius: 8px; font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 500; line-height: 1.35; text-align: center; color: #fff; background: #0F1B3D; box-shadow: 0 10px 24px -10px rgba(0, 0, 0, 0.45); pointer-events: none; opacity: 0; transform: translateY(3px); transition: opacity 0.12s ease, transform 0.12s ease; }
.pg-request-add .ui-tip.below { transform: translateY(-3px); }
.pg-request-add .ui-tip.show { opacity: 1; transform: none; }
.pg-request-add .ui-tip::after { content: ''; position: absolute; left: calc(var(--ax, 50%) - 4px); bottom: -4px; width: 8px; height: 8px; background: inherit; transform: rotate(45deg); }
.pg-request-add .ui-tip.below::after { bottom: auto; top: -4px; }
[data-theme="dark"] .pg-request-add .ui-tip { color: #0F1B3D; background: #E6EAF5; }
.pg-request-add .dp-field { display: flex !important; align-items: center; gap: 9px; width: 100%; text-align: left; cursor: pointer; }
.pg-request-add .dp-field .dp-val { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pg-request-add .dp-field .dp-val.empty { color: var(--text-faint, #94A3B8); }
.pg-request-add .dp-field > i { font-size: 13px; color: var(--brand, #1D4ED8); opacity: 0.8; }
.pg-request-add .dp-field[aria-expanded="true"] { border-color: var(--brand, #1D4ED8) !important; box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand, #1D4ED8) 16%, transparent); }
.pg-request-add .dp-pop { position: fixed; z-index: 70; width: 300px; padding: 14px; border-radius: 14px; color: var(--text, #0F1B3D); background: var(--surface, #fff); border: 1px solid var(--border, #E4E8F1); box-shadow: 0 22px 48px -18px rgba(15, 27, 61, 0.5); font-family: 'Inter', sans-serif; animation: dpIn 0.14s ease; }
@keyframes dpIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
.pg-request-add .dp-head { display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }
.pg-request-add .dp-title { flex: 1; display: inline-flex; align-items: center; gap: 6px; padding: 5px 8px; border-radius: 8px; font-size: 14.5px; font-weight: 700; color: var(--text, #0F1B3D); }
.pg-request-add .dp-title:hover { background: var(--surface-hover, #F1F4FA); }
.pg-request-add .dp-title i { font-size: 10px; color: var(--text-faint, #94A3B8); }
.pg-request-add .dp-nav { width: 30px; height: 30px; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; color: var(--text-muted, #64748B); border: 1px solid var(--border, #E4E8F1); }
.pg-request-add .dp-nav:hover { color: var(--brand, #1D4ED8); border-color: color-mix(in srgb, var(--brand, #1D4ED8) 40%, transparent); }
.pg-request-add .dp-week,
.pg-request-add .dp-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
.pg-request-add .dp-week span { padding: 4px 0; text-align: center; font-size: 11px; font-weight: 600; color: var(--text-faint, #94A3B8); }
.pg-request-add .dp-day { height: 36px; border-radius: 9px; font-size: 13px; font-weight: 500; color: var(--text, #0F1B3D); position: relative; transition: background-color 0.12s ease; }
.pg-request-add .dp-day:hover { background: var(--surface-hover, #F1F4FA); }
.pg-request-add .dp-day.out { color: var(--text-faint, #94A3B8); opacity: 0.55; }
.pg-request-add .dp-day.today { font-weight: 700; color: var(--brand, #1D4ED8); }
.pg-request-add .dp-day.today::after { content: ''; position: absolute; left: 50%; bottom: 5px; width: 4px; height: 4px; margin-left: -2px; border-radius: 999px; background: currentColor; }
.pg-request-add .dp-day.sel { color: #fff; background: var(--brand, #1D4ED8); font-weight: 700; box-shadow: 0 6px 14px -8px var(--brand, #1D4ED8); }
[data-theme="dark"] .pg-request-add .dp-day.sel { color: #0B1020; }
.pg-request-add .dp-day:focus-visible,
.pg-request-add .dp-cell:focus-visible { outline: 2px solid var(--brand, #1D4ED8); outline-offset: 1px; }
.pg-request-add .dp-cells { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.pg-request-add .dp-cell { height: 40px; border-radius: 10px; font-size: 13px; font-weight: 600; color: var(--text, #0F1B3D); border: 1px solid transparent; }
.pg-request-add .dp-cell:hover { background: var(--surface-hover, #F1F4FA); }
.pg-request-add .dp-cell.cur { color: var(--brand, #1D4ED8); border-color: color-mix(in srgb, var(--brand, #1D4ED8) 35%, transparent); }
.pg-request-add .dp-cell.sel { color: #fff; background: var(--brand, #1D4ED8); }
[data-theme="dark"] .pg-request-add .dp-cell.sel { color: #0B1020; }
.pg-request-add .dp-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border, #E4E8F1); }
.pg-request-add .dp-foot button { padding: 6px 12px; border-radius: 8px; font-size: 12.5px; font-weight: 600; }
.pg-request-add .dp-clear { color: var(--text-muted, #64748B); }
.pg-request-add .dp-clear:hover { color: #DC2626; background: color-mix(in srgb, #EF4444 10%, transparent); }
.pg-request-add .dp-done { color: #fff; background: var(--brand, #1D4ED8); }
[data-theme="dark"] .pg-request-add .dp-done { color: #0B1020; }
.pg-request-add .inp { width: 100%; height: 38px; padding: 0 12px; border-radius: 9px; font-size: 13px; color: var(--text); background: var(--surface-2); border: 1px solid var(--border); transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease; }
.pg-request-add textarea.inp { height: auto; min-height: 96px; padding: 10px 12px; resize: vertical; line-height: 1.5; }
.pg-request-add select.inp { appearance: none; padding-right: 34px; cursor: pointer; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; }
.pg-request-add .inp::placeholder { color: var(--text-faint); }
.pg-request-add .inp:hover { border-color: var(--border-strong); }
.pg-request-add .inp:focus { outline: none; background: var(--surface); border-color: var(--brand); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 16%, transparent); }
[data-theme="dark"] .pg-request-add .inp { color-scheme: dark; }
.pg-request-add .csel { position: relative; }
.pg-request-add .csel-btn { display: flex; align-items: center; gap: 9px; width: 100%; text-align: left; cursor: pointer; }
.pg-request-add .csel-btn .csel-val { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pg-request-add .csel-btn .chev { font-size: 10px; color: var(--text-faint); transition: transform 0.2s ease; }
.pg-request-add .csel-btn[aria-expanded="true"] { border-color: var(--brand); background: var(--surface); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 16%, transparent); }
.pg-request-add .csel-btn[aria-expanded="true"] .chev { transform: rotate(180deg); }
.pg-request-add .csel-dot { width: 8px; height: 8px; flex: none; border-radius: 999px; background: var(--oc); box-shadow: 0 0 0 3px color-mix(in srgb, var(--oc) 18%, transparent); }
.pg-request-add .csel-menu { position: fixed; z-index: 60; padding: 5px; max-height: 280px; overflow-y: auto; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 18px 40px -16px rgba(15, 27, 61, 0.45); animation: cselIn 0.14s ease; }
@keyframes cselIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
.pg-request-add .csel-opt { width: 100%; display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 8px; font-size: 13px; text-align: left; color: var(--text); }
.pg-request-add .csel-opt:hover,
.pg-request-add .csel-opt.active { background: var(--surface-hover); }
.pg-request-add .csel-opt[aria-selected="true"] { font-weight: 600; color: var(--brand); background: var(--brand-soft); }
.pg-request-add .csel-opt small { display: block; font-size: 11.5px; font-weight: 400; color: var(--text-faint); }
.pg-request-add .csel-opt .fa-check { margin-left: auto; font-size: 11px; }
.pg-request-add .ix { margin-bottom: 14px; }
.pg-request-add .ix-tabs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; background: var(--surface); box-shadow: 0 6px 18px -16px rgba(15, 27, 61, 0.35); }
.pg-request-add .ix-tabs button { height: 54px; font-size: 14px; font-weight: 700; color: var(--text-muted); transition: color 0.15s ease, background-color 0.15s ease; }
.pg-request-add .ix-tabs button + button { border-left: 1px solid var(--border); }
.pg-request-add .ix-tabs button:hover { color: var(--text); }
.pg-request-add .ix-tabs button[aria-selected="true"] { color: var(--brand); background: color-mix(in srgb, var(--brand) 4%, var(--surface)); box-shadow: inset 0 -3px 0 var(--brand); }
.pg-request-add .ix-panel[hidden] { display: none; }
.pg-request-add .ix-steps { position: relative; margin-top: 16px; padding-left: 44px; display: flex; flex-direction: column; gap: 18px; }
.pg-request-add .ix-steps::before { content: ''; position: absolute; left: 13px; top: 8px; bottom: 8px; width: 2px; border-radius: 2px; background: var(--border); }
.pg-request-add .ix-step { position: relative; }
.pg-request-add .ix-step::before { content: ''; position: absolute; left: -36px; top: 22px; width: 10px; height: 10px; border-radius: 999px; background: var(--border-strong); box-shadow: 0 0 0 4px var(--bg); transition: background-color 0.2s ease; }
.pg-request-add .ix-step.open::before { background: var(--brand); box-shadow: 0 0 0 4px var(--bg), 0 0 0 6px color-mix(in srgb, var(--brand) 25%, transparent); }
.pg-request-add .ix-step.done::before { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; font-size: 8px; line-height: 14px; text-align: center; color: #fff; width: 14px; height: 14px; left: -38px; top: 20px; background: #059669; }
.pg-request-add .ix-card { border: 1px solid var(--border); border-radius: 12px; background: var(--surface); box-shadow: 0 4px 14px -12px rgba(15, 27, 61, 0.3); overflow: hidden; }
.pg-request-add .ix-head { width: 100%; display: flex; align-items: center; gap: 12px; padding: 13px 18px; text-align: left; transition: background-color 0.15s ease; }
.pg-request-add .ix-head:hover { background: var(--surface-hover); }
.pg-request-add .ix-ico { width: 28px; height: 28px; flex: none; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; color: var(--text-muted); background: var(--surface-2); }
.pg-request-add .ix-title { flex: 1; font-size: 14px; font-weight: 600; color: var(--text); }
.pg-request-add .ix-chev { font-size: 11px; color: var(--text-faint); transition: transform 0.2s ease; }
.pg-request-add .ix-step.open .ix-head { background: color-mix(in srgb, var(--brand) 5%, var(--surface)); border-bottom: 1px solid var(--border); }
.pg-request-add .ix-step.open .ix-ico { color: var(--brand); background: var(--brand-soft); }
.pg-request-add .ix-step.open .ix-title { color: var(--brand); font-weight: 700; }
.pg-request-add .ix-step.open .ix-chev { transform: rotate(180deg); color: var(--brand); }
.pg-request-add .ix-step.done .ix-ico { color: #059669; background: color-mix(in srgb, #10B981 13%, var(--surface)); }
.pg-request-add .ix-body { padding: 20px 24px 18px; }
.pg-request-add .ix-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 48px; }
.pg-request-add .ix-grid .full { grid-column: 1 / -1; }
@media (max-width: 860px) {
  .pg-request-add .ix-grid { grid-template-columns: minmax(0, 1fr); }
  .pg-request-add .ix-steps { padding-left: 32px; }
  .pg-request-add .ix-step::before { left: -25px; }
  .pg-request-add .ix-steps::before { left: 10px; }
}
.pg-request-add .ix-l { display: flex; align-items: center; gap: 5px; margin-bottom: 7px; font-size: 12.5px; font-weight: 600; color: var(--text-muted); line-height: 1.4; }
.pg-request-add .ix-l .req { color: #DC2626; }
.pg-request-add .ix-l .info { font-size: 11px; color: var(--text-faint); cursor: help; }
.pg-request-add .ix-tag { margin-left: auto; padding: 1px 7px; border-radius: 6px; font-size: 10.5px; font-weight: 700; color: #0369A1; background: color-mix(in srgb, #0EA5E9 12%, var(--surface)); border: 1px solid color-mix(in srgb, #0EA5E9 25%, transparent); }
.pg-request-add .ix-hint { margin-top: 5px; font-size: 11.5px; font-style: italic; color: var(--text-faint); }
.pg-request-add .ix-ro { height: 38px; display: flex; align-items: center; font-size: 13px; font-weight: 600; color: var(--text); }
.pg-request-add .ix-f .inp.invalid { border-color: #DC2626; box-shadow: 0 0 0 3px color-mix(in srgb, #DC2626 14%, transparent); }
.pg-request-add .ix-foot { display: flex; justify-content: flex-end; margin-top: 20px; }
.pg-request-add .ix-next { display: inline-flex; align-items: center; gap: 8px; padding: 7px 18px; border-radius: 999px; font-size: 12.5px; font-weight: 700; color: var(--brand); border: 1.5px solid var(--brand); background: var(--surface); transition: background-color 0.15s ease, color 0.15s ease; }
.pg-request-add .ix-next:hover { color: #fff; background: var(--brand); }
.pg-request-add .ix-next i { font-size: 10px; }
.pg-request-add .ix-seg { display: inline-flex; gap: 2px; padding: 3px; border-radius: 10px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-request-add .ix-seg button { min-width: 72px; padding: 6px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 600; color: var(--text-muted); }
.pg-request-add .ix-seg button[aria-pressed="true"] { color: var(--brand); background: var(--surface); box-shadow: 0 1px 3px rgba(15, 27, 61, 0.15); }
.pg-request-add .ix-when[hidden] { display: none; }
.pg-request-add .ix-when { padding: 14px 16px; border-radius: 10px; background: color-mix(in srgb, var(--surface-2) 60%, var(--surface)); border: 1px dashed var(--border); }
.pg-request-add .ix-when .ix-grid { gap: 14px 32px; }
.pg-request-add .ix-files { display: flex; flex-direction: column; gap: 6px; }
.pg-request-add .ix-file { display: flex; align-items: center; gap: 9px; padding: 8px 10px; border-radius: 9px; font-size: 12.5px; background: var(--surface-2); border: 1px solid var(--border); }
.pg-request-add .ix-file i { color: var(--brand); }
.pg-request-add .ix-file span { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500; }
.pg-request-add .ix-file button { font-size: 12px; font-weight: 600; color: var(--brand); }
.pg-request-add .ix-file button:hover { text-decoration: underline; }
.pg-request-add .ix-people { display: flex; flex-direction: column; gap: 10px; }
.pg-request-add .ix-person { display: grid; grid-template-columns: 200px repeat(3, minmax(0, 1fr)); gap: 10px 14px; align-items: center; }
.pg-request-add .ix-person .role { font-size: 13px; font-weight: 600; }
.pg-request-add .ix-person.head span { font-size: 12px; font-weight: 600; color: var(--text-muted); }
@media (max-width: 860px) {
  .pg-request-add .ix-person { grid-template-columns: minmax(0, 1fr); }
  .pg-request-add .ix-person.head { display: none; }
}
.pg-request-add .ix-idbar { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.pg-request-add .ix-idbar .env-toggle { margin: 0 0 0 auto; }
.pg-request-add .ix-tools { display: flex; flex-direction: column; gap: 10px; }
.pg-request-add .ix-tool { border: 1px solid var(--border); border-radius: 12px; background: var(--surface); transition: border-color 0.15s ease, box-shadow 0.15s ease; }
.pg-request-add .ix-tool.on { border-color: color-mix(in srgb, var(--env-c, var(--brand)) 45%, var(--border)); box-shadow: inset 3px 0 0 var(--env-c, var(--brand)); }
.pg-request-add .ix-tool-h { display: flex; align-items: center; gap: 12px; padding: 11px 14px; }
.pg-request-add .ix-tool-h .tool-ico { width: 32px; height: 32px; flex: none; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; color: var(--brand); background: var(--brand-soft); }
.pg-request-add .ix-tool:not(.on) .tool-ico { color: var(--text-faint); background: var(--surface-2); }
.pg-request-add .ix-tool-h b { display: block; font-size: 13.5px; font-weight: 700; }
.pg-request-add .ix-tool-h small { display: block; font-size: 11.5px; color: var(--text-faint); }
.pg-request-add .ix-tool:not(.on) .ix-tool-h b { color: var(--text-muted); }
.pg-request-add .ix-tool-b { padding: 4px 16px 16px 58px; }
.pg-request-add .ix-tool-b .ix-grid { gap: 14px 28px; }
.pg-request-add .sw { position: relative; margin-left: auto; width: 40px; height: 22px; flex: none; border-radius: 999px; background: var(--border-strong); transition: background-color 0.2s ease; }
.pg-request-add .sw::after { content: ''; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: 999px; background: #fff; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25); transition: transform 0.2s ease; }
.pg-request-add .sw[aria-checked="true"] { background: #059669; }
.pg-request-add .sw[aria-checked="true"]::after { transform: translateX(18px); }
.pg-request-add .sw:focus-visible { outline: 2px solid var(--brand); outline-offset: 2px; }
.pg-request-add .ix-chips { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; min-height: 38px; padding: 5px 8px; border-radius: 9px; background: var(--surface-2); border: 1px solid var(--border); cursor: text; }
.pg-request-add .ix-chips:focus-within { border-color: var(--brand); background: var(--surface); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 16%, transparent); }
.pg-request-add .ix-chip { display: inline-flex; align-items: center; gap: 5px; padding: 2px 4px 2px 9px; border-radius: 999px; font-size: 12px; font-weight: 600; color: var(--brand); background: var(--brand-soft); }
.pg-request-add .ix-chip button { width: 18px; height: 18px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; font-size: 9px; }
.pg-request-add .ix-chip button:hover { background: color-mix(in srgb, var(--brand) 18%, transparent); }
.pg-request-add .ix-chips input { flex: 1; min-width: 120px; height: 26px; font-size: 13px; background: transparent; outline: none; color: var(--text); }
.pg-request-add .ix-checks { display: flex; flex-wrap: wrap; gap: 8px; }
.pg-request-add .ix-check { display: inline-flex; align-items: center; gap: 8px; padding: 7px 12px; border-radius: 9px; font-size: 12.5px; font-weight: 500; border: 1px solid var(--border); background: var(--surface-2); cursor: pointer; }
.pg-request-add .ix-check input { accent-color: var(--brand); }
.pg-request-add [data-env-scope] .ix-tool.on { border-color: color-mix(in srgb, var(--env-c) 45%, var(--border)); }
.pg-request-add .ix-seg.invalid { border-color: #DC2626; box-shadow: 0 0 0 3px color-mix(in srgb, #DC2626 14%, transparent); }
.pg-request-add .ix-drop { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 9px; cursor: pointer; font-size: 12.5px; color: var(--text-muted); border: 1.5px dashed color-mix(in srgb, var(--brand) 40%, var(--border)); background: color-mix(in srgb, var(--brand) 3%, var(--surface)); transition: border-color 0.15s ease, background-color 0.15s ease; }
.pg-request-add .ix-drop:hover,
.pg-request-add .ix-drop.over { border-color: var(--brand); background: color-mix(in srgb, var(--brand) 8%, var(--surface)); }
.pg-request-add .ix-drop i { color: var(--brand); }
.pg-request-add .ix-drop b { color: var(--brand); font-weight: 700; }
.pg-request-add .ix-files:not(:empty) { margin-top: 8px; }
.pg-request-add #ixForm .ix-steps::before,
.pg-request-add #ixForm .ix-step::before { --bg: var(--surface); }
.pg-request-add #ixForm .ix-step::before { box-shadow: 0 0 0 4px var(--surface); }
.pg-request-add #ixForm .ix-step.open::before { box-shadow: 0 0 0 4px var(--surface), 0 0 0 6px color-mix(in srgb, var(--brand) 25%, transparent); }
.pg-request-add .st-wrap { margin: 8px 0 24px; }
.pg-request-add .st-card { border: 1px solid var(--border); border-radius: 18px; background: var(--surface); box-shadow: 0 18px 40px -30px rgba(15, 27, 61, 0.45); overflow: hidden; }
.pg-request-add .st-sec { padding: 22px 30px; }
.pg-request-add .st-sec + .st-sec { border-top: 1px solid var(--border); }
.pg-request-add .st-label { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; font-size: 13.5px; font-weight: 700; color: var(--text); }
.pg-request-add .st-label .n { width: 24px; height: 24px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800; color: #fff; background: var(--brand); }
.pg-request-add .st-label .n.off { color: var(--text-faint); background: var(--surface-2); border: 1px solid var(--border); }
[data-theme="dark"] .pg-request-add .st-label .n:not(.off) { color: #0B1020; }
.pg-request-add .st-search { display: flex; align-items: center; gap: 10px; height: 46px; padding: 0 10px 0 16px; border-radius: 999px; border: 1.5px solid transparent; background: linear-gradient(var(--surface), var(--surface)) padding-box, linear-gradient(90deg, #3B6CF6 0%, #8B5CF6 50%, #EC4899 100%) border-box; box-shadow: 0 10px 26px -16px rgba(139, 92, 246, 0.45); }
.pg-request-add .st-search:focus-within { box-shadow: 0 0 0 4px color-mix(in srgb, #8B5CF6 16%, transparent), 0 10px 28px -12px rgba(139, 92, 246, 0.4); }
.pg-request-add .st-search > i { font-size: 15px; color: #8B5CF6; }
.pg-request-add .st-search input { flex: 1; min-width: 0; height: 40px; font-size: 14px; background: transparent; outline: none; color: var(--text); }
.pg-request-add .st-search input::-webkit-search-cancel-button { display: none; }
.pg-request-add .st-search button { width: 28px; height: 28px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; color: var(--text-faint); }
.pg-request-add .st-search button:hover { background: var(--surface-hover); color: var(--text); }
.pg-request-add .st-search { padding-right: 5px; }
.pg-request-add .st-search .st-go { width: auto; height: 36px; gap: 7px; padding: 0 18px; font-size: 13px; font-weight: 700; color: #fff; background: var(--brand); box-shadow: 0 8px 18px -10px rgba(11, 42, 122, 0.8); }
.pg-request-add .st-search .st-go:hover { color: #fff; background: var(--brand); filter: brightness(1.12); }
.pg-request-add .st-search .st-go i { font-size: 12px; color: inherit; }
[data-theme="dark"] .pg-request-add .st-search .st-go { color: #0B1020; }
.pg-request-add .st-meta { display: flex; justify-content: space-between; margin: 14px 2px 8px; font-size: 12px; color: var(--text-faint); }
.pg-request-add .st-list { max-height: 330px; overflow-y: auto; border: 1px solid var(--border); border-radius: 12px; }
.pg-request-add .st-row { display: grid; grid-template-columns: 28px 170px minmax(0, 1fr) minmax(0, 1fr); align-items: center; gap: 14px; width: 100%; padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); transition: background-color 0.15s ease; }
.pg-request-add .st-row:last-child { border-bottom: 0; }
.pg-request-add .st-row:hover { background: var(--surface-hover); }
.pg-request-add .st-row.head { position: sticky; top: 0; z-index: 1; padding-top: 9px; padding-bottom: 9px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12.5px; font-weight: 600; color: var(--th-fg, #1E3A8A); background: var(--th-bg, var(--surface-2)); cursor: default; }
.pg-request-add .st-row.head:hover { background: var(--th-bg, var(--surface-2)); }
.pg-request-add .st-radio { width: 18px; height: 18px; border-radius: 999px; border: 2px solid var(--border-strong); display: inline-flex; align-items: center; justify-content: center; }
.pg-request-add .st-row[aria-checked="true"] { background: color-mix(in srgb, var(--brand) 6%, var(--surface)); box-shadow: inset 3px 0 0 var(--brand); }
.pg-request-add .st-row[aria-checked="true"] .st-radio { border-color: var(--brand); }
.pg-request-add .st-row[aria-checked="true"] .st-radio::after { content: ''; width: 8px; height: 8px; border-radius: 999px; background: var(--brand); }
.pg-request-add .st-apm { font-family: 'JetBrains Mono', monospace; font-size: 12.5px; font-weight: 600; color: var(--brand); }
.pg-request-add .st-row b { font-size: 13px; font-weight: 600; color: var(--text); }
.pg-request-add .st-row small { display: block; font-size: 11.5px; color: var(--text-faint); }
.pg-request-add .st-row mark { background: color-mix(in srgb, #F59E0B 30%, transparent); color: inherit; border-radius: 3px; padding: 0 1px; }
.pg-request-add .st-list[hidden] { display: none; }
.pg-request-add .st-ask { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
@media (max-width: 760px) {
  .pg-request-add .st-ask { grid-template-columns: minmax(0, 1fr); }
}
.pg-request-add .st-ans { position: relative; display: flex; align-items: center; gap: 14px; padding: 16px 44px 16px 16px; border-radius: 14px; text-align: left; border: 1.5px solid var(--border); background: var(--surface); transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease; }
.pg-request-add .st-ans:hover { border-color: color-mix(in srgb, var(--brand) 45%, var(--border)); }
.pg-request-add .st-ans .ti { width: 40px; height: 40px; flex: none; border-radius: 11px; display: inline-flex; align-items: center; justify-content: center; font-size: 15px; color: var(--brand); background: var(--brand-soft); }
.pg-request-add .st-ans b { display: block; font-size: 14px; font-weight: 700; color: var(--text); }
.pg-request-add .st-ans small { display: block; margin-top: 2px; font-size: 12px; color: var(--text-muted); }
.pg-request-add .st-ans .ck { position: absolute; top: 50%; right: 16px; transform: translateY(-50%); font-size: 16px; color: var(--brand); opacity: 0; transition: opacity 0.15s ease; }
.pg-request-add .st-ans[aria-checked="true"] { border-color: var(--brand); background: color-mix(in srgb, var(--brand) 6%, var(--surface)); box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 14%, transparent); }
.pg-request-add .st-ans[aria-checked="true"] .ck { opacity: 1; }
.pg-request-add .st-find { margin-top: 18px; padding-top: 18px; border-top: 1px dashed var(--border); animation: stIn 0.2s ease; }
.pg-request-add .st-find.off { opacity: 0.45; }
.pg-request-add .st-find.off .st-search { box-shadow: none; filter: grayscale(1); }
.pg-request-add .st-find.off * { cursor: not-allowed; }
@keyframes stIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }
.pg-request-add .st-sub-l { margin-bottom: 10px; font-size: 12.5px; font-weight: 600; color: var(--text-muted); }
.pg-request-add .st-empty { padding: 34px 16px; text-align: center; font-size: 13px; color: var(--text-faint); }
.pg-request-add .st-empty i { display: block; margin-bottom: 8px; font-size: 22px; opacity: 0.6; }
@media (max-width: 760px) {
  .pg-request-add .st-row { grid-template-columns: 28px minmax(0, 1fr); }
  .pg-request-add .st-row > :nth-child(n+3) { grid-column: 2; }
  .pg-request-add .st-row.head { display: none; }
}
.pg-request-add .st-types { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
@media (max-width: 760px) {
  .pg-request-add .st-types { grid-template-columns: minmax(0, 1fr); }
}
.pg-request-add .st-type { position: relative; display: flex; flex-direction: column; gap: 6px; padding: 16px; border-radius: 14px; text-align: left; border: 1.5px solid var(--border); background: var(--surface); transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease; }
.pg-request-add .st-type:hover:not(:disabled) { border-color: color-mix(in srgb, var(--tc) 50%, var(--border)); }
.pg-request-add .st-type:disabled { opacity: 0.5; cursor: not-allowed; }
.pg-request-add .st-type .ti { width: 36px; height: 36px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; font-size: 15px; color: var(--tc); background: color-mix(in srgb, var(--tc) 12%, var(--surface)); }
.pg-request-add .st-type b { font-size: 14px; font-weight: 700; color: var(--text); }
.pg-request-add .st-type small { font-size: 12px; line-height: 1.45; color: var(--text-muted); }
.pg-request-add .st-type .ck { position: absolute; top: 14px; right: 14px; font-size: 15px; color: var(--tc); opacity: 0; transition: opacity 0.15s ease; }
.pg-request-add .st-type[aria-checked="true"] { border-color: var(--tc); background: color-mix(in srgb, var(--tc) 6%, var(--surface)); box-shadow: 0 0 0 3px color-mix(in srgb, var(--tc) 14%, transparent); }
.pg-request-add .st-type[aria-checked="true"] .ck { opacity: 1; }
.pg-request-add .st-type.saas { --tc: #0E7490; }
.pg-request-add .st-type.kpmg { --tc: #047857; }
.pg-request-add .st-type.saasplus { --tc: #7C3AED; }
[data-theme="dark"] .pg-request-add .st-type.saas { --tc: #22D3EE; }
[data-theme="dark"] .pg-request-add .st-type.kpmg { --tc: #34D399; }
[data-theme="dark"] .pg-request-add .st-type.saasplus { --tc: #A78BFA; }
.pg-request-add .st-foot { display: flex; justify-content: flex-end; align-items: center; gap: 10px; padding: 16px 30px; border-top: 1px solid var(--border); background: color-mix(in srgb, var(--surface-2) 55%, var(--surface)); }
.pg-request-add .st-foot .sum { flex: 1; min-width: 0; font-size: 12.5px; color: var(--text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pg-request-add .st-foot .sum b { color: var(--text); }
.pg-request-add .st-foot .alt { margin-right: auto; font-size: 12.5px; font-weight: 600; color: var(--brand); }
.pg-request-add .st-foot .alt:hover { text-decoration: underline; }
.pg-request-add .st-btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 11px; font-size: 13px; font-weight: 700; border: 1px solid var(--border); background: var(--surface); color: var(--text); }
.pg-request-add .st-btn:hover { background: var(--surface-hover); }
.pg-request-add .st-btn.primary { color: #fff; background: var(--brand); border-color: var(--brand); box-shadow: 0 10px 22px -12px rgba(11, 42, 122, 0.8); }
.pg-request-add .st-btn.primary:hover:not(:disabled) { filter: brightness(1.1); }
.pg-request-add .st-btn.primary:disabled { opacity: 0.45; cursor: not-allowed; box-shadow: none; }
[data-theme="dark"] .pg-request-add .st-btn.primary { color: #0B1020; }
.pg-request-add .st-chosen { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 22px; margin-bottom: 18px; padding: 12px 16px; border-radius: 12px; border: 1px solid color-mix(in srgb, var(--brand) 25%, var(--border)); background: color-mix(in srgb, var(--brand) 5%, var(--surface)); font-size: 12.5px; color: var(--text-muted); }
.pg-request-add .st-chosen b { color: var(--text); font-weight: 600; }
.pg-request-add .st-chosen .pill { padding: 2px 10px; border-radius: 999px; font-size: 11.5px; font-weight: 700; color: var(--tc); background: color-mix(in srgb, var(--tc) 12%, var(--surface)); }
.pg-request-add .st-chosen button { margin-left: auto; font-size: 12.5px; font-weight: 600; color: var(--brand); }
.pg-request-add .st-chosen button:hover { text-decoration: underline; }
.pg-request-add { --grad: linear-gradient(90deg, #3B6CF6 0%, #8B5CF6 50%, #EC4899 100%); --wash: linear-gradient(100deg, #EEF3FF 0%, #F4EFFF 55%, #FDF0F7 100%); --glow: rgba(139, 92, 246, 0.28); }
[data-theme="dark"] .pg-request-add { --grad: linear-gradient(90deg, #6B93FF 0%, #A78BFA 50%, #F472B6 100%); --wash: linear-gradient(100deg, #141D3F 0%, #1B1840 55%, #251633 100%); --glow: rgba(167, 139, 250, 0.3); }
.pg-request-add .vi-head { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px; padding: 8px 12px; margin-bottom: 12px; border-radius: 16px; background: var(--wash); border: 1px solid var(--border); }
.pg-request-add .title-block { display: flex; align-items: center; gap: 12px; flex: none; }
.pg-request-add .title-accent { width: 4px; height: 30px; flex: none; border-radius: 999px; background: linear-gradient(180deg, #1E3A8A, #60A5FA); }
.pg-request-add .vi-head h1 { font-size: 18px; font-weight: 800; letter-spacing: -0.01em; line-height: 1.2; white-space: nowrap; }
.pg-request-add .vi-head .sub { font-size: 12px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pg-request-add .vi-names { order: 2; flex: 1 1 0; display: flex; gap: 10px; min-width: 0; padding-left: 16px; border-left: 1px solid var(--border); }
.pg-request-add .vi-name { display: flex; align-items: center; gap: 10px; flex: 0 1 auto; min-width: 0; padding: 6px 14px 6px 6px; border-radius: 12px; background: color-mix(in srgb, var(--surface) 75%, transparent); border: 1px solid color-mix(in srgb, var(--border) 80%, transparent); }
.pg-request-add .vi-name-ico { width: 30px; height: 30px; flex: none; border-radius: 9px; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; color: var(--ic); background: color-mix(in srgb, var(--ic) 12%, var(--surface)); }
[data-theme="dark"] .pg-request-add .vi-name-ico { filter: brightness(1.5); }
.pg-request-add .vi-name-txt { display: flex; flex-direction: column; min-width: 0; line-height: 1.25; }
.pg-request-add .vi-name-txt span { font-size: 11px; font-weight: 500; color: var(--text-muted); }
.pg-request-add .vi-name-txt b { font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.pg-request-add .vi-meta { order: 3; flex: 0 1 auto; min-width: 0; overflow-x: auto; scrollbar-width: none; display: grid; grid-template-columns: auto auto; align-items: center; gap: 6px 20px; padding-left: 16px; border-left: 1px solid var(--border); }
.pg-request-add .meta-item { display: flex; align-items: center; gap: 7px; white-space: nowrap; }
.pg-request-add .meta-item > span:first-child { font-size: 11.5px; font-weight: 500; color: var(--text-muted); }
.pg-request-add .meta-item > span:first-child::after { content: ':'; }
.pg-request-add .meta-item > b { font-size: 13px; font-weight: 600; }
.pg-request-add .meta-item .pill { padding: 1px 9px; font-size: 11.5px; }
.pg-request-add .vi-actions { order: 4; margin-left: auto; display: flex; gap: 8px; position: relative; }
.pg-request-add .vi-actions > button.with-label { width: auto; gap: 7px; padding: 0 12px 0 10px; font-size: 13px; font-weight: 600; white-space: nowrap; }
.pg-request-add .vi-actions > button[aria-expanded="true"] { background: var(--brand-soft); border-color: var(--brand); }
.pg-request-add .vi-actions > button { width: 34px; height: 34px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; background: var(--surface); color: var(--brand); border: 1px solid var(--border); box-shadow: 0 4px 12px -8px rgba(15, 27, 61, 0.3); }
.pg-request-add .vi-actions > button i,
.pg-request-add .vi-actions > button .ico { transition: transform 0.15s ease; }
.pg-request-add .vi-actions > button:hover i,
.pg-request-add .vi-actions > button:hover .ico { transform: scale(1.2); }
.pg-request-add .vi-actions .tool-download { color: #DC2626; }
[data-theme="dark"] .pg-request-add .vi-actions .tool-download { color: #F87171; }
@media (max-width: 1000px) {
  .pg-request-add .vi-names { order: 4; flex-basis: 100%; padding-left: 0; border-left: 0; }
  .pg-request-add .vi-name { flex: 1; }
  .pg-request-add .vi-meta { order: 5; flex-basis: 100%; padding-left: 0; border-left: 0; }
}
.pg-request-add .pill-draft { color: #B45309; background: color-mix(in srgb, #F59E0B 15%, var(--surface)); }
.pg-request-add #hdType { color: var(--tc); background: color-mix(in srgb, var(--tc) 13%, var(--surface)); }
.pg-request-add #add-request-view .vi-head { margin-bottom: 14px; }
.pg-request-add .vi-head .vi-steps { order: 2; margin: 0 auto; display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 600; color: var(--text-muted); }
.pg-request-add .vi-steps span { display: inline-flex; align-items: center; gap: 6px; }
.pg-request-add .vi-steps b { width: 20px; height: 20px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; color: var(--text-faint); background: var(--surface); border: 1px solid var(--border); }
.pg-request-add .vi-steps .on { color: var(--brand); }
.pg-request-add .vi-steps .on b { color: #fff; background: var(--brand); border-color: var(--brand); }
.pg-request-add .vi-steps i { font-size: 9px; color: var(--text-faint); }
.pg-request-add .vi-head-wrap { max-width: 980px; margin: 0 auto; }
.pg-request-add .ix-tabs { gap: 8px; padding: 6px; border-radius: 14px; background: var(--surface-2); }
.pg-request-add .ix-tabs button { position: relative; height: auto; display: flex; align-items: center; gap: 12px; padding: 12px 16px 16px; border-radius: 10px; text-align: left; overflow: hidden; }
.pg-request-add .ix-tabs button + button { border-left: 0; }
.pg-request-add .ix-tabs button:hover { background: color-mix(in srgb, var(--surface) 70%, transparent); }
.pg-request-add .ix-tabs button[aria-selected="true"] { background: var(--surface); box-shadow: 0 4px 14px -8px rgba(15, 27, 61, 0.35); }
.pg-request-add .ix-tab-ico { width: 34px; height: 34px; flex: none; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; color: var(--text-faint); background: var(--surface); border: 1px solid var(--border); }
.pg-request-add .ix-tabs button[aria-selected="true"] .ix-tab-ico { color: #fff; background: var(--brand); border-color: var(--brand); }
[data-theme="dark"] .pg-request-add .ix-tabs button[aria-selected="true"] .ix-tab-ico { color: #0B1020; }
.pg-request-add .ix-tab-t b { display: block; font-size: 14px; font-weight: 700; color: var(--text-muted); }
.pg-request-add .ix-tabs button[aria-selected="true"] .ix-tab-t b { color: var(--brand); }
.pg-request-add .ix-tab-t small { display: block; margin-top: 1px; font-size: 11.5px; font-weight: 500; color: var(--text-faint); }
.pg-request-add .ix-tabs button:disabled { cursor: not-allowed; }
.pg-request-add .ix-tabs button:disabled:hover { background: transparent; }
.pg-request-add .ix-tabs button:disabled .ix-tab-t b,
.pg-request-add .ix-tabs button:disabled .ix-tab-ico { opacity: 0.55; }
.pg-request-add #ixForm .ix-step.done::before { box-shadow: 0 0 0 3px var(--surface), 0 0 0 5px color-mix(in srgb, #10B981 35%, transparent); }
.pg-request-add .ix-step.done .ix-card { border-color: color-mix(in srgb, #10B981 45%, var(--border)); }
.pg-request-add .ix-step.done .ix-head { background: color-mix(in srgb, #10B981 9%, var(--surface)); }
.pg-request-add .ix-step.done .ix-title { color: #047857; font-weight: 700; }
.pg-request-add .ix-step.done .ix-ico { color: #fff; background: #059669; }
.pg-request-add .ix-step.done .ix-chev { color: #059669; }
.pg-request-add .ix-step.done.open .ix-head { border-bottom-color: color-mix(in srgb, #10B981 30%, var(--border)); }
[data-theme="dark"] .pg-request-add .ix-step.done .ix-title { color: #34D399; }
[data-theme="dark"] .pg-request-add .ix-step.done .ix-head { background: color-mix(in srgb, #10B981 14%, var(--surface)); }
.pg-request-add .ix-tools { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px 12px; align-items: stretch; }
@media (max-width: 860px) {
  .pg-request-add .ix-tools { grid-template-columns: minmax(0, 1fr); }
}
.pg-request-add .ix-tool-h { padding: 10px 12px; }
.pg-request-add .ix-tool-b { padding: 2px 12px 12px; }
.pg-request-add .ix-tool-b .ix-grid { grid-template-columns: minmax(0, 1fr); gap: 10px; }
.pg-request-add .ix-tool-b .ix-l { margin-bottom: 5px; font-size: 12px; }
.pg-request-add .ix-tool-b .inp,
.pg-request-add .ix-tool-b .ix-chips { min-height: 36px; }
.pg-request-add #ixForm .ix-tool-b .inp { height: 36px; }
.pg-request-add .ix-tool-h small { font-size: 11px; }
.pg-request-add .ix-idbar { margin-bottom: 10px; }
.pg-request-add .ix-lock { margin-left: auto; font-size: 13px; color: var(--text-faint); }
.pg-request-add .ix-lock[hidden] { display: none; }
.pg-request-add .ix-tab-bar { position: absolute; left: 16px; right: 16px; bottom: 7px; height: 3px; border-radius: 999px; background: var(--border); overflow: hidden; }
.pg-request-add .ix-tab-bar span { display: block; width: 0; height: 100%; border-radius: inherit; background: #059669; transition: width 0.3s ease; }
.pg-request-add .ix-steps { margin-top: 20px; }
.pg-request-add .ix-head { padding: 14px 18px; }
.pg-request-add .ix-ico { width: 32px; height: 32px; font-size: 13px; border-radius: 9px; }
.pg-request-add .ix-title { font-size: 14.5px; }
.pg-request-add .ix-stat { margin-left: auto; padding: 2px 10px; border-radius: 999px; font-size: 11.5px; font-weight: 600; white-space: nowrap; color: var(--text-muted); background: var(--surface-2); border: 1px solid var(--border); }
.pg-request-add .ix-stat.part { color: #B45309; background: color-mix(in srgb, #F59E0B 12%, var(--surface)); border-color: color-mix(in srgb, #F59E0B 30%, transparent); }
.pg-request-add .ix-stat.full { color: #047857; background: color-mix(in srgb, #10B981 12%, var(--surface)); border-color: color-mix(in srgb, #10B981 30%, transparent); }
.pg-request-add .ix-stat.full::before { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; margin-right: 5px; font-size: 9.5px; }
.pg-request-add .ix-title { flex: 0 1 auto; }
.pg-request-add .ix-chev { margin-left: 10px; }
.pg-request-add .ix-body { padding: 22px 24px 20px; }
.pg-request-add .ix-grid { gap: 18px 32px; }
.pg-request-add #ixForm .inp { height: 40px; background-color: var(--surface); border-color: var(--border); }
.pg-request-add #ixForm textarea.inp { height: auto; }
.pg-request-add #ixForm .inp:hover { border-color: var(--border-strong); }
.pg-request-add #ixForm .csel-btn.inp { background-color: var(--surface); }
.pg-request-add .ix-l { margin-bottom: 6px; font-size: 12.5px; color: var(--text); }
.pg-request-add .ix-l .req { margin-left: -2px; }
.pg-request-add .ix-hint { font-style: normal; }
.pg-request-add .ix-foot { margin-top: 22px; padding-top: 16px; border-top: 1px solid var(--border); }
.pg-request-add .ix-next { padding: 9px 18px; border-radius: 10px; color: #fff; background: var(--brand); border-color: var(--brand); box-shadow: 0 8px 18px -10px rgba(11, 42, 122, 0.8); }
.pg-request-add .ix-next:hover { filter: brightness(1.1); }
[data-theme="dark"] .pg-request-add .ix-next { color: #0B1020; }
.pg-request-add .ix-group { display: flex; align-items: center; gap: 9px; margin-top: 4px; font-size: 11.5px; font-weight: 700; letter-spacing: 0.02em; color: var(--brand); }
.pg-request-add .ix-group::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.pg-request-add .ix-grid > .ix-group:first-child { margin-top: 0; }
.pg-request-add .ix-grid { row-gap: 16px; }
.pg-request-add .ix-spacer { visibility: hidden; }
@media (max-width: 860px) {
  .pg-request-add .ix-spacer { display: none; }
}
.pg-request-add .ix-l { min-height: 20px; }
.pg-request-add .ix-tag { font-weight: 600; letter-spacing: 0.01em; }
.pg-request-add .ix-in { position: relative; display: block; }
.pg-request-add .ix-in > i { position: absolute; left: 13px; top: 50%; transform: translateY(-50%); font-size: 12px; color: var(--text-faint); pointer-events: none; transition: color 0.15s ease; }
.pg-request-add .ix-in > .inp { padding-left: 36px; }
.pg-request-add .ix-in:focus-within > i { color: var(--brand); }
.pg-request-add .ix-q { display: flex; align-items: center; justify-content: space-between; gap: 10px 20px; flex-wrap: wrap; padding: 12px 14px; border-radius: 11px; border: 1px solid var(--border); background: color-mix(in srgb, var(--surface-2) 55%, var(--surface)); }
.pg-request-add .ix-q > .ix-l { flex: 1 1 320px; margin: 0; font-size: 13px; font-weight: 600; color: var(--text); }
.pg-request-add .ix-q .ix-seg { flex: none; background: var(--surface); }
.pg-request-add .ix-q .ix-seg button { min-width: 64px; }
.pg-request-add .ix-q .ix-seg button[aria-pressed="true"] { color: #fff; background: var(--brand); box-shadow: none; }
[data-theme="dark"] .pg-request-add .ix-q .ix-seg button[aria-pressed="true"] { color: #0B1020; }
.pg-request-add .ix-q:has(.ix-seg.invalid) { border-color: #DC2626; }
.pg-request-add .ix-q .ix-seg.invalid { box-shadow: none; }
.pg-request-add .ix-when { margin-top: -6px; border-style: solid; border-radius: 0 0 11px 11px; }
.pg-request-add .ix-firms { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
@media (max-width: 860px) {
  .pg-request-add .ix-firms { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
.pg-request-add .ix-firm { display: flex; align-items: center; gap: 9px; padding: 9px 12px; border-radius: 10px; font-size: 13px; font-weight: 500; cursor: pointer; border: 1px solid var(--border); background: var(--surface); transition: border-color 0.15s ease, background-color 0.15s ease; }
.pg-request-add .ix-firm:hover { border-color: var(--border-strong); }
.pg-request-add .ix-firm input { width: 15px; height: 15px; accent-color: var(--brand); flex: none; }
.pg-request-add .ix-firm:has(input:checked) { border-color: var(--brand); background: color-mix(in srgb, var(--brand) 6%, var(--surface)); color: var(--brand); font-weight: 600; }
.pg-request-add .ix-firms.invalid { padding: 6px; border-radius: 12px; outline: 1.5px solid #DC2626; }
.pg-request-add .vi-head > .vi-names:first-child { padding-left: 0; border-left: 0; }
.pg-request-add .tp-list { display: flex; flex-direction: column; gap: 10px; }
.pg-request-add .tp-card { padding: 12px 14px 14px; border-radius: 11px; border: 1px solid var(--border); background: var(--surface); }
.pg-request-add .tp-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; font-size: 12.5px; font-weight: 700; color: var(--brand); }
.pg-request-add .tp-x { display: inline-flex; align-items: center; gap: 6px; padding: 3px 8px; border-radius: 7px; font-size: 12px; font-weight: 600; color: var(--text-muted); }
.pg-request-add .tp-x:hover { color: #DC2626; background: color-mix(in srgb, #EF4444 10%, var(--surface)); }
.pg-request-add .tp-card .ix-grid { row-gap: 12px; }
.pg-request-add .tp-card .ix-when { margin-top: 0; }
.pg-request-add .tp-add { display: inline-flex; align-items: center; gap: 8px; margin-top: 10px; padding: 8px 14px; border-radius: 10px; font-size: 12.5px; font-weight: 600; color: var(--brand); border: 1.5px dashed color-mix(in srgb, var(--brand) 45%, var(--border)); background: var(--surface); transition: background-color 0.15s ease; }
.pg-request-add .tp-add:hover { background: var(--brand-soft); }
.pg-request-add .ix-err { margin-top: 5px; font-size: 11.5px; font-weight: 500; line-height: 1.4; color: #DC2626; }
.pg-request-add .ix-q > .ix-err { flex-basis: 100%; margin-top: 0; text-align: right; }
.pg-request-add .ix-step[hidden] { display: none; }
.pg-request-add .ix-l a.ix-link { margin-left: 8px; font-size: 12px; font-weight: 600; color: var(--brand); }
.pg-request-add .ix-l a.ix-link:hover { text-decoration: underline; }
.pg-request-add .ix-when.ix-off,
.pg-request-add .ix-step.ix-na .ix-body { opacity: 0.72; }
.pg-request-add .ix-off .ix-drop,
.pg-request-add .ix-na .ix-drop { pointer-events: none; opacity: 0.6; }
.pg-request-add .ix-off .ix-warn { display: none; }
.pg-request-add #ixForm .inp:disabled,
.pg-request-add #ixForm .dp-field:disabled,
.pg-request-add .ix-chips input:disabled { cursor: not-allowed; background: var(--surface-2); }
.pg-request-add .ix-off .ix-seg button:disabled,
.pg-request-add .ix-na .ix-seg button:disabled,
.pg-request-add .ix-check:has(input:disabled) { cursor: not-allowed; opacity: 0.65; }
.pg-request-add .ix-tool-b.off { opacity: 0.72; }
.pg-request-add .ix-tool-b.off .ix-chips { background: var(--surface-2); }
.pg-request-add .sw:disabled { cursor: not-allowed; opacity: 0.5; }
.pg-request-add .ix-na-note { display: flex; align-items: center; gap: 8px; margin-bottom: 14px; padding: 8px 12px; border-radius: 9px; font-size: 12.5px; font-weight: 600; color: var(--text-muted); background: var(--surface-2); }
.pg-request-add .ix-na-note[hidden] { display: none; }
.pg-request-add .doc-table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 13px; border: 1px solid var(--border); border-radius: 10px; }
.pg-request-add .doc-table th { padding: 9px 12px; text-align: left; font-size: 12px; font-weight: 700; color: var(--brand); background: var(--surface-2); }
.pg-request-add .doc-table th:first-child { border-radius: 10px 0 0 0; }
.pg-request-add .doc-table th:last-child { border-radius: 0 10px 0 0; }
.pg-request-add .doc-table td { padding: 8px 12px; vertical-align: top; border-top: 1px solid var(--border); }
.pg-request-add .doc-table td:first-child { width: 34%; padding-top: 16px; font-weight: 600; }
.pg-request-add .doc-table td:nth-child(3) { width: 210px; }
.pg-request-add .doc-table td:last-child { width: 56px; text-align: center; }
.pg-request-add .doc-table .ix-drop { padding: 8px 10px; }
.pg-request-add .doc-file { display: flex; align-items: center; gap: 8px; min-height: 38px; font-weight: 500; color: var(--brand); word-break: break-word; }
.pg-request-add .doc-file button,
.pg-request-add .doc-x { color: var(--text-faint); }
.pg-request-add .doc-file button:hover { color: #DC2626; }
.pg-request-add .doc-x { color: #DC2626; padding: 10px 4px; }
.pg-request-add .doc-add { display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 10px; font-size: 12.5px; font-weight: 600; color: var(--brand); border: 1.5px dashed color-mix(in srgb, var(--brand) 45%, var(--border)); background: var(--surface); }
.pg-request-add .doc-add:hover { background: var(--brand-soft); }
