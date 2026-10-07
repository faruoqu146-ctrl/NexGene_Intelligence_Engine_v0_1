from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = (ROOT / "backend" / "app" / "main.py").read_text()


def test_intelligence_surfaces_exist():
    assert "/api/v1/intelligence" in MAIN
    assert "intelligence" in MAIN.lower()
