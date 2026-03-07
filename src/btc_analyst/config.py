from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data_raw: Path
    data_processed: Path
    models: Path
    reports: Path

    @classmethod
    def from_root(cls, root: Path) -> "ProjectPaths":
        return cls(
            root=root,
            data_raw=root / "data" / "raw",
            data_processed=root / "data" / "processed",
            models=root / "models",
            reports=root / "reports" / "generated",
        )

    def ensure(self) -> None:
        for path in (self.data_raw, self.data_processed, self.models, self.reports):
            path.mkdir(parents=True, exist_ok=True)

