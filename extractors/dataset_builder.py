"""Production guard: synthetic seed generation is intentionally disabled.
Use demo/dataset_builder.py only for UI/algorithm demos with a separate demo database.
"""
class DatasetBuilder:
    def __init__(self, *args, **kwargs): pass
    def populate_seed_dataset(self):
        raise RuntimeError("Synthetic seed dataset disabled in production. Use explicit demo mode and a separate database.")
