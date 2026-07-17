from pathlib import Path

def fix_file(path: Path):
    txt = path.read_text(encoding='utf-8')
    new = txt.replace('````{tab-set}\n\n```{tab-item}', '````{tab-set}\n```{tab-item}')
    if new != txt:
        bak = path.with_suffix(path.suffix + '.tabfix.bak')
        bak.write_text(txt, encoding='utf-8')
        path.write_text(new, encoding='utf-8')
        return True
    return False

if __name__ == '__main__':
    mods = []
    for f in Path('docs').rglob('*.md'):
        if fix_file(f):
            mods.append(str(f))
    print('Modified files:', mods)
