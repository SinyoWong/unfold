"""Check public links, Skill metadata and translation versions (stdlib only)."""
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
# Match local-only paths in .gitignore; release archives have no Git metadata.
LOCAL_ONLY = {
    'media', 'releases', 'deliverables', 'evals/results',
    'evals/compare.py', 'evals/comparison', 'evals/interactive',
    'CONTRIBUTING.md', 'CHANGELOG.md',
    'docs/install.md', 'docs/install.en.md', 'docs/releasing.md',
}


def public_files():
    files = []
    for base, directories, names in os.walk(ROOT, followlinks=False):
        kept = []
        for name in directories:
            path = Path(base) / name
            relative = path.relative_to(ROOT).as_posix()
            if name in {'.git', '.agents', '.venv', '__pycache__', 'node_modules'}:
                continue
            if relative in LOCAL_ONLY:
                continue
            if path.is_symlink() or getattr(path.lstat(), 'st_file_attributes', 0) & 0x400:
                continue
            kept.append(name)
        directories[:] = kept
        files.extend(Path(base) / name for name in names
                     if (Path(base) / name).relative_to(ROOT).as_posix() not in LOCAL_ONLY)
    return files


def check():
    files = public_files()
    public_paths = set(files)
    for path in files:
        public_paths.update(parent for parent in path.parents if parent.is_relative_to(ROOT))
    errors = []
    links = 0
    for path in files:
        if path.suffix != '.md':
            continue
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8-sig'), flags=re.S)
        for target in re.findall(r'!?\[[^\]]*\]\(([^)\n]+)\)', text):
            target = target.strip().strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith('//') or not parsed.path:
                continue
            links += 1
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing local target {target}')
            elif resolved not in public_paths:
                errors.append(f'{path.relative_to(ROOT)}: target is excluded from publication: {target}')

    for name in ('unfold-dev', 'unfold-review'):
        source = (ROOT / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
        frontmatter = re.match(r'\A---\n(.*?)\n---\n', source, re.S)
        if not frontmatter:
            errors.append(f'{name}: missing metadata block')
            continue
        header = frontmatter.group(1)
        if not re.search(rf'^name: {name}$', header, re.M) or not re.search(r'^description: .+', header, re.M):
            errors.append(f'{name}: missing name or description')
        version = re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$', header, re.M)
        translated = (ROOT / 'docs' / 'en' / f'{name}.md').read_text(encoding='utf-8')
        if not version or f'Source version: **{version.group(1)}**' not in translated:
            errors.append(f'{name}: translation version does not match')
        if 'do not load this document as a separate Skill' not in translated:
            errors.append(f'{name}: translation must remain reading-only')

    if errors:
        raise ValueError('\n'.join(errors))
    print(f'PASS repository: {links} local links, two Skill metadata blocks, translation versions')


if __name__ == '__main__':
    try:
        check()
    except (OSError, ValueError) as error:
        print(f'FAIL repository: {error}', file=sys.stderr)
        sys.exit(1)
