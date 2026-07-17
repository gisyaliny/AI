from pathlib import Path

def scan(path):
    s = Path(path).read_text(encoding='utf-8').splitlines()
    res = []
    lineno = 0
    while lineno < len(s):
        line = s[lineno]
        if line.strip().startswith('````{tab-set}'):
            start = lineno + 1
            items = []
            others = []
            i = start
            while i < len(s):
                if s[i].strip() == '````':
                    end = i
                    break
                if s[i].strip().startswith('```{tab-item}'):
                    items.append((i+1, s[i]))
                else:
                    # record non-tab-item line inside block
                    others.append((i+1, s[i]))
                i += 1
            else:
                end = None
            res.append({'start_line': lineno+1, 'end_line': end+1 if end else None, 'items': items, 'others': others})
            lineno = i+1 if end else lineno+1
        else:
            lineno += 1
    return res

if __name__ == '__main__':
    path = 'docs/local-llm/02-mastering-ollama.md'
    for r in scan(path):
        print(f"Tab-set at {r['start_line']} to {r['end_line']} — tab-items: {len(r['items'])} — non-tab lines sample: {len(r['others'])}")
        if r['others']:
            for ln, txt in r['others'][:10]:
                print(f"  other at {ln}: {txt!r}")
