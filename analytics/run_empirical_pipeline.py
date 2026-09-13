"""Production validation entry point.

This module deliberately refuses to manufacture the seven historical tests from demo
fixtures.  It runs only validators backed by rows whose provenance is ONCHAIN/API.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analytics.backtest_validator import BacktestValidator
from analytics.out_of_sample_tester import OutOfSampleValidator
from db.database import Database


def run_empirical_pipeline() -> dict:
    db = Database()
    backtest = BacktestValidator(db).run_full_validation()
    oos = OutOfSampleValidator(db.db_path).run_blind_test()

    status = "VALIDATED" if backtest.get("decision") == "GO" and oos.get("status") == "PASSED" else "DATA_INCOMPLETE"
    result = {
        "status": status,
        "backtest": backtest,
        "out_of_sample": oos,
        "note": (
            "Only ONCHAIN/API-provenance early BUY observations are eligible. "
            "No demo fixture, synthetic control or hard-coded significance metric is used."
        ),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# Backward-compatible name used by earlier scripts.
def run_all_7_tests() -> dict:
    return run_empirical_pipeline()


if __name__ == "__main__":
    run_empirical_pipeline()
