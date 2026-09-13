from pathlib import Path
from config.settings import REPORTS_DIR
class HTMLDashboardGenerator:
 def __init__(self,db): self.db=db
 def generate_html_dashboard(self):
  p=REPORTS_DIR/'dashboard.html';p.write_text('<!doctype html><meta charset="utf-8"><title>Validation pending</title><h1>Validation pending</h1><p>Use the Next.js UI. No static validated dashboard is generated until empirical data exists.</p>',encoding='utf-8');return p
