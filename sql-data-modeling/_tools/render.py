"""Render ERDs (Workbench-style crow's foot) to PDF/PNG and write MySQL DDL for Workbench import."""
import subprocess, sys, os, html
sys.path.insert(0, os.path.dirname(__file__))
import models as M

HDR = {'U': '#e8701a', 'D': '#1f3a68', 'N': '#3d6b8f'}  # UBC orange, DigiSonos navy, neutral

def esc(s): return html.escape(s)

def table_html(name, cols, color, highlight=(), prefix=''):
    rows = [f'<TR><TD BGCOLOR="{color}" COLSPAN="2" ALIGN="LEFT"><FONT COLOR="white" POINT-SIZE="12"><B>{esc(name)}</B></FONT></TD></TR>']
    for c, ty, f in cols:
        fl = f.split()
        mark = ''
        if 'PK' in fl: mark += '<FONT COLOR="#c99a06"><B>PK</B></FONT>'
        if 'FK' in fl: mark += (' ' if mark else '') + '<FONT COLOR="#cc1f1f"><B>FK</B></FONT>'
        label = f'<B>{esc(c)}</B>' if 'PK' in fl else esc(c)
        bg = ' BGCOLOR="#fff27a"' if c in highlight else ''
        markcell = f'<FONT POINT-SIZE="9">{mark}</FONT>' if mark else ' '
        rows.append(f'<TR><TD ALIGN="LEFT" WIDTH="34" PORT="w_{prefix}{c}"{bg}>{markcell}</TD>'
                    f'<TD ALIGN="LEFT" PORT="{prefix}{c}"{bg}>{label}</TD></TR>')
    return ('<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" BGCOLOR="white" COLOR="#555555">'
            + ''.join(rows) + '</TABLE>>')

def ends(child_card, parent_card):
    head = {'0..*': 'crowodot', '1..*': 'crowtee', '0..1': 'teeodot'}[child_card]
    tail = 'teetee' if parent_card == '1' else 'teeodot'
    return head, tail

def pk_of(tables, t):
    return [c for c, _, f in tables[t] if 'PK' in f.split()][0]

def rel_edges(model, nid=lambda t: t, prefix=''):
    T = model['tables']; out = []
    for p, ch, fk, lab, cc, pc in model['rels']:
        head, tail = ends(cc, pc)
        ident = 'PK' in dict((c, f) for c, _, f in T[ch])[fk].split()
        out.append(f'"{nid(p)}":"{prefix}{pk_of(T,p)}":e -> "{nid(ch)}":"w_{prefix}{fk}":w '
                   f'[dir=both, arrowhead={head}, arrowtail={tail}, style={"solid" if ident else "dashed"}, '
                   f'label=" {esc(lab)} "];')
    return out

GRAPH_ATTRS = ['node [shape=plain, fontname="DejaVu Sans", fontsize=10];',
               'edge [fontname="DejaVu Sans", fontsize=9, color="#333333", arrowsize=1.1, penwidth=1.1];']

LEGEND = ('legend [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" COLOR="#999999">'
          '<TR><TD ALIGN="LEFT"><B>Legend</B></TD></TR>'
          '<TR><TD ALIGN="LEFT"><FONT COLOR="#c99a06"><B>PK</B></FONT> primary key   <FONT COLOR="#cc1f1f"><B>FK</B></FONT> foreign key</TD></TR>'
          '<TR><TD ALIGN="LEFT">||  exactly one     o|  zero or one</TD></TR>'
          '<TR><TD ALIGN="LEFT">|&lt;  one or many    o&lt;  zero or many</TD></TR>'
          '<TR><TD ALIGN="LEFT">solid line = identifying, dashed = non-identifying</TD></TR>'
          '</TABLE>>];')

def run_dot(dot_src, base):
    open(base + '.dot', 'w').write(dot_src)
    subprocess.run(['dot', '-Tpdf', base + '.dot', '-o', base + '.pdf'], check=True)
    subprocess.run(['dot', '-Tpng', '-Gdpi=110', base + '.dot', '-o', base + '.png'], check=True)
    os.remove(base + '.dot')

def render(model, base, color, rankdir='LR'):
    d = ['digraph ERD {', f'graph [rankdir={rankdir}, splines=true, nodesep=0.45, ranksep=0.9, pad=0.3, '
         f'labelloc=t, fontsize=18, fontname="DejaVu Sans", label=<<B>{esc(model["title"])}</B>>];'] + GRAPH_ATTRS
    for t, cols in model['tables'].items():
        d.append(f'"{t}" [label={table_html(t, cols, color)}];')
    d += rel_edges(model)
    d.append(LEGEND)
    d.append('}')
    run_dot('\n'.join(d), base)

def ddl(model, path, schema):
    T = model['tables']; out = [f"-- {model['title']}",
        "-- MySQL DDL. Open in MySQL Workbench 8.x: File > Import > Reverse Engineer MySQL Create Script,",
        "-- tick 'Place imported objects on a diagram', then arrange the tables.", "",
        f"CREATE SCHEMA IF NOT EXISTS {schema};", f"USE {schema};", ""]
    # order tables so parents come first
    done, order = set(), []
    while len(order) < len(T):
        for t in T:
            if t in done: continue
            parents = {p for p, ch, *_ in model['rels'] if ch == t and p != t}
            # allow cycles (team<->employee): defer FK with ALTER
            if parents <= done or all(pp in done or (t, pp) in CYCLES for pp in parents):
                order.append(t); done.add(t)
    deferred = []
    for t in order:
        lines, pks = [], [c for c, _, f in T[t] if 'PK' in f.split()]
        for c, ty, f in T[t]:
            fl = f.split()
            nn = ' NOT NULL' if ('PK' in fl or 'NN' in fl or ('FK' in fl and 'NULL' not in fl)) else ''
            lines.append(f"  `{c}` {ty}{nn}")
        lines.append(f"  PRIMARY KEY ({', '.join('`'+p+'`' for p in pks)})")
        for c, _, f in T[t]:
            if 'UQ' in f.split(): lines.append(f"  UNIQUE (`{c}`)")
        for chk in model.get('checks', []):
            if 'rating' in [c for c, *_ in T[t]]: lines.append(f"  {chk}")
        for p, ch, fk, lab, cc, pc in model['rels']:
            if ch != t: continue
            cons = f"CONSTRAINT `fk_{ch}_{fk}` FOREIGN KEY (`{fk}`) REFERENCES `{p}` (`{pk_of(T,p)}`)"
            if (t, p) in CYCLES: deferred.append(f"ALTER TABLE `{t}` ADD {cons};")
            else: lines.append("  " + cons)
        out.append(f"CREATE TABLE `{t}` (\n" + ",\n".join(lines) + "\n) ENGINE=InnoDB;\n")
    out += deferred
    open(path, 'w').write("\n".join(out) + "\n")

CYCLES = {('team', 'employee')}  # team.manager_id -> employee is added after employee exists

def render_flows(base):
    """Exchanging tables only, fixed layout: DigiSonos column left, UBC column right, flows top-down in process order."""
    hl, order = {'U': {}, 'D': {}}, {'U': [], 'D': []}
    for _, _, src, dst in M.FLOWS:
        for co, t, cols in src + dst:
            hl[co].setdefault(t, set()).update(cols)
            if t not in order[co]: order[co].append(t)
    full = {'U': M.UBC['tables'], 'D': M.DIGISONOS['tables']}
    X = {'D': 130, 'U': 1010}          # column centers (points)
    d = ['digraph B2B {', 'graph [splines=true, pad=0.4, outputorder=edgesfirst];'] + GRAPH_ATTRS
    tops = {}
    for co in 'DU':
        y = 0
        for t in order[co]:
            h = 21 * (len(full[co][t]) + 1)
            tops[(co, t)] = y
            d.append(f'"{co}_{t}" [pos="{X[co]},{-(y + h/2)}!", label={table_html(t, full[co][t], HDR[co], hl[co][t])}];')
            y += h + 55
    hdr = lambda co, txt: (f'hdr_{co} [shape=plaintext, pos="{X[co]},50!", label=<<FONT POINT-SIZE="18" '
                           f'COLOR="{HDR[co]}"><B>{txt}</B></FONT>>];')
    d += [hdr('D', 'DigiSonos (buyer)'), hdr('U', 'United Box Company (seller)'),
          'title [shape=plaintext, pos="570,115!", label=<<FONT POINT-SIZE="20"><B>MP5 Task Two: B2B data flows between DigiSonos and UBC</B></FONT><BR/>'
          '<FONT POINT-SIZE="11">Only tables that send or receive data are shown; full ERDs are in the Task One files.<BR/>'
          'Yellow = exchanged fields. Orange arrows = data flows, numbered in process order (0 to 5).</FONT>>];']
    for step, lab, src, dst in M.FLOWS:
        pairs = [(src[min(i, len(src)-1)], dst[min(i, len(dst)-1)]) for i in range(max(len(src), len(dst)))]
        both = 'both ways' in lab
        for i, ((sco, st, sc), (dco, dt, dc)) in enumerate(pairs):
            txt = f' {esc(lab)}' if i == 0 else ''
            sp = 'e' if sco == 'D' else 'w'; dp = 'e' if dco == 'D' else 'w'
            sport = sc[0] if sco == 'D' else 'w_' + sc[0]
            dport = dc[0] if dco == 'D' else 'w_' + dc[0]
            d.append(f'"{sco}_{st}":"{sport}":{sp} -> "{dco}_{dt}":"{dport}":{dp} [color="#e67e22", '
                     f'penwidth=2.4, arrowsize=1.2, dir={"both" if both else "forward"}, arrowhead=normal, arrowtail=normal, '
                     f'label=<<B><FONT COLOR="#c0392b" POINT-SIZE="15">{step}</FONT></B>'
                     + (f'<FONT COLOR="#c0392b">{txt}</FONT>' if txt else '') + '>];')
    d.append('}')
    open(base + '.dot', 'w').write('\n'.join(d))
    for fmt, extra in [('pdf', []), ('png', ['-Gdpi=110'])]:
        subprocess.run(['neato', '-n2', f'-T{fmt}', *extra, base + '.dot', '-o', f'{base}.{fmt}'], check=True)
    os.remove(base + '.dot')

if __name__ == '__main__':
    out = sys.argv[1]
    j = lambda *p: os.path.join(out, *p)
    for p in ['MP2-Notflix', 'MP4-UBC-Sales', 'MP5-B2B-Integration']: os.makedirs(j(p), exist_ok=True)
    render(M.NOTFLIX, j('MP2-Notflix', 'MP2 Notflix ERD'), HDR['N'])
    ddl(M.NOTFLIX, j('MP2-Notflix', 'notflix_schema.sql'), 'notflix')
    render(M.UBC_SALES, j('MP4-UBC-Sales', 'MP4 Farrow UBC Sales ERD'), HDR['U'])
    ddl(M.UBC_SALES, j('MP4-UBC-Sales', 'ubc_sales_schema.sql'), 'ubc_sales')
    render(M.UBC, j('MP5-B2B-Integration', 'MP5 Task1 UBC integrated ERD'), HDR['U'])
    ddl(M.UBC, j('MP5-B2B-Integration', 'ubc_integrated_schema.sql'), 'ubc')
    render(M.DIGISONOS, j('MP5-B2B-Integration', 'MP5 Task1 DigiSonos integrated ERD'), HDR['D'])
    ddl(M.DIGISONOS, j('MP5-B2B-Integration', 'digisonos_integrated_schema.sql'), 'digisonos')
    render_flows(j('MP5-B2B-Integration', 'MP5 Task2 B2B data flows'))
    print('done')
