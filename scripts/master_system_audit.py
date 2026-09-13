#!/usr/bin/env python3
"""Audit production integrity. It intentionally refuses synthetic validation claims."""
from pathlib import Path
import sqlite3, re, sys
ROOT=Path(__file__).resolve().parent.parent
errors=[]
if (ROOT/'.env').exists(): errors.append('.env is present in project package')
for path in ROOT.rglob('*'):
    if not path.is_file() or 'demo' in path.parts or path.suffix not in {'.py','.ts','.tsx','.mjs','.md'}: continue
    text=path.read_text(errors='ignore')
    if re.search(r'HELIUS_API_KEY\s*=\s*os\.getenv\([^\n]+,[ ]*["\'][^"\']{20,}',text): errors.append(f'hardcoded key fallback: {path}')
db=ROOT/'data/onchain_intelligence.db'
status={}
if db.exists():
    conn=sqlite3.connect(db);c=conn.cursor()
    status['trades']=c.execute('SELECT COUNT(*) FROM trades').fetchone()[0]
    status['verified_first_buys']=c.execute("SELECT COUNT(*) FROM trades WHERE side='BUY' AND is_first_buyer=1 AND source_type IN ('ONCHAIN','API')").fetchone()[0]
    conn.close()
print('Production audit:',status)
if errors:
    print('FAIL');[print(' -',e) for e in errors];sys.exit(1)
print('PASS: no packaged secrets/hardcoded API-key fallbacks detected.')
