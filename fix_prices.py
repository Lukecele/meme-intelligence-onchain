#!/usr/bin/env python3
import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    if "const [solPrice, setSolPrice] = useState<number>(145.5" in content:
        import_stmt = 'import React, { useState, useEffect'
        if import_stmt not in content:
            # We assume it's already there
            pass
        
        replacement = """  const [solPrice, setSolPrice] = useState<number>(145.5);

  useEffect(() => {
    fetch("/api/price?mint=So11111111111111111111111111111111111111112")
      .then(res => res.json())
      .then(data => {
        if (data.success && data.priceUsd) {
          setSolPrice(data.priceUsd);
        }
      })
      .catch(() => {});
  }, []);"""
        content = content.replace("  const [solPrice, setSolPrice] = useState<number>(145.5);", replacement)
        content = content.replace("  const [solPrice, setSolPrice] = useState<number>(145.50);", replacement)
        content = content.replace("|| 145.50", "|| solPrice")
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")

patch_file("web/src/components/LiveRadarFeed.tsx")
patch_file("web/src/components/InvestmentSimulator.tsx")
