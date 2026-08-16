"""
store.py — Durable storage for criteria versions and model scores.

Uses sqlite3 (stdlib). JSON fields store variable structures.
Designed for offline operation, minimal footprint, human-inspectable.
"""
import sqlite3
import json
from typing import List, Optional, Tuple, Dict, Any
from schema import CriteriaVersion, ModelScore, Frame


class DriftStore:
    DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS criteria_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artifact_name TEXT NOT NULL,
        version_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        frame_json TEXT NOT NULL,
        rubric_dimensions_json TEXT,
        rubric_weights_json TEXT,
        exemplar_count INTEGER,
        notes TEXT,
        UNIQUE(artifact_name, version_id)
    );

    CREATE TABLE IF NOT EXISTS model_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        criteria_artifact TEXT NOT NULL,
        criteria_version TEXT NOT NULL,
        score REAL NOT NULL,
        score_type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        source_url TEXT,
        notes TEXT,
        FOREIGN KEY (criteria_artifact, criteria_version)
            REFERENCES criteria_versions(artifact_name, version_id)
    );

    CREATE INDEX IF NOT EXISTS idx_cv_art_ver
        ON criteria_versions(artifact_name, version_id);
    CREATE INDEX IF NOT EXISTS idx_ms_model
        ON model_scores(model_name);
    CREATE INDEX IF NOT EXISTS idx_ms_criteria
        ON model_scores(criteria_artifact, criteria_version);
    """

    def __init__(self, path: str = "drift.db"):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.executescript(self.DB_SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ------------------------------------------------------------------
    # Criteria versions
    # ------------------------------------------------------------------
    def insert_criteria(self, cv: CriteriaVersion) -> int:
        cur = self.conn.execute(
            """INSERT OR REPLACE INTO criteria_versions
               (artifact_name, version_id, timestamp, frame_json,
                rubric_dimensions_json, rubric_weights_json,
                exemplar_count, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                cv.artifact_name,
                cv.version_id,
                cv.timestamp,
                json.dumps(cv.frame.to_dict()),
                json.dumps(cv.rubric_dimensions) if cv.rubric_dimensions else None,
                json.dumps(cv.rubric_weights) if cv.rubric_weights else None,
                cv.exemplar_count,
                cv.notes,
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_criteria_history(self, artifact_name: str) -> List[CriteriaVersion]:
        rows = self.conn.execute(
            """SELECT * FROM criteria_versions
               WHERE artifact_name = ?
               ORDER BY timestamp ASC""",
            (artifact_name,),
        ).fetchall()
        return [self._row_to_cv(r) for r in rows]

    def get_all_artifacts(self) -> List[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT artifact_name FROM criteria_versions"
        ).fetchall()
        return [r[0] for r in rows]

    def _row_to_cv(self, row: sqlite3.Row) -> CriteriaVersion:
        return CriteriaVersion(
            artifact_name=row["artifact_name"],
            version_id=row["version_id"],
            timestamp=row["timestamp"],
            frame=Frame.from_dict(json.loads(row["frame_json"])),
            rubric_dimensions=json.loads(row["rubric_dimensions_json"])
            if row["rubric_dimensions_json"] else None,
            rubric_weights=json.loads(row["rubric_weights_json"])
            if row["rubric_weights_json"] else None,
            exemplar_count=row["exemplar_count"],
            notes=row["notes"] or "",
        )

    # ------------------------------------------------------------------
    # Model scores
    # ------------------------------------------------------------------
    def insert_score(self, ms: ModelScore) -> int:
        cur = self.conn.execute(
            """INSERT INTO model_scores
               (model_name, criteria_artifact, criteria_version,
                score, score_type, timestamp, source_url, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                ms.model_name,
                ms.criteria_artifact,
                ms.criteria_version,
                ms.score,
                ms.score_type,
                ms.timestamp,
                ms.source_url,
                ms.notes,
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def get_scores(self, artifact: str, version: Optional[str] = None,
                   model: Optional[str] = None) -> List[ModelScore]:
        sql = "SELECT * FROM model_scores WHERE criteria_artifact = ?"
        params: List[Any] = [artifact]
        if version:
            sql += " AND criteria_version = ?"
            params.append(version)
        if model:
            sql += " AND model_name = ?"
            params.append(model)
        sql += " ORDER BY timestamp ASC"
        rows = self.conn.execute(sql, params).fetchall()
        return [self._row_to_ms(r) for r in rows]

    def get_score_matrix(self, artifact: str) -> Dict[str, Dict[str, float]]:
        """Return {model_name: {version_id: score}}."""
        rows = self.conn.execute(
            """SELECT model_name, criteria_version, score
               FROM model_scores WHERE criteria_artifact = ?""",
            (artifact,),
        ).fetchall()
        matrix: Dict[str, Dict[str, float]] = {}
        for r in rows:
            matrix.setdefault(r["model_name"], {})[r["criteria_version"]] = r["score"]
        return matrix

    def _row_to_ms(self, row: sqlite3.Row) -> ModelScore:
        return ModelScore(
            model_name=row["model_name"],
            criteria_artifact=row["criteria_artifact"],
            criteria_version=row["criteria_version"],
            score=row["score"],
            score_type=row["score_type"],
            timestamp=row["timestamp"],
            source_url=row["source_url"] or "",
            notes=row["notes"] or "",
        )

    # ------------------------------------------------------------------
    # Export / backup
    # ------------------------------------------------------------------
    def export_json(self, artifact: str) -> Dict[str, Any]:
        versions = self.get_criteria_history(artifact)
        scores = self.get_scores(artifact)
        return {
            "artifact": artifact,
            "criteria_versions": [v.to_dict() for v in versions],
            "model_scores": [s.to_dict() for s in scores],
        }
