"""Shared helpers for the #7 SLR (protocol: notes/04-slr/_local/t07-slr-prompt.md v1.2)."""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # NCKH/
DATA = ROOT / "scripts" / "t07-slr" / "data"
DATA.mkdir(parents=True, exist_ok=True)
UA = "NCKH-DPL302m-SLR/1.0 (academic literature review; low volume)"

K1 = '(aerial OR "remote sensing" OR satellite OR UAV OR drone)'
K2 = '("object detection" OR detector)'
K3 = '(tiny OR "small object" OR "small objects")'
K4 = ('(oriented OR rotated OR "arbitrary-oriented" OR "rotated bounding box" '
      'OR "oriented bounding box")')
K5 = ('("label assignment" OR "sample assignment" OR "positive samples" '
      'OR "similarity metric")')
K6 = ('((angle OR orientation) AND (ambiguity OR "boundary discontinuity" OR '
      'periodicity OR "square-like" OR "angle coder" OR Gaussian))')
K7 = '(YOLO OR "real-time" OR lightweight)'

QUERIES = {
    "Q-A": f'{K1} AND {K2} AND ({K3} OR {K4}) AND (dataset OR benchmark OR survey OR review)',
    "Q-B": f"{K1} AND {K4} AND {K2} AND {K6}",
    "Q-C": f"{K2} AND {K3} AND {K5}",
    "Q-D": (f'{K1} AND {K2} AND {K3} AND (transformer OR attention OR "feature pyramid" '
            f'OR "feature fusion" OR "super-resolution" OR DETR)'),
    "Q-E": f"{K1} AND {K4} AND {K2} AND {K7}",
    "Q-G": ('(tiny OR small) AND (oriented OR rotated) AND (angle OR orientation) '
            'AND (size OR scale OR resolution) '
            'AND (ambiguity OR uncertainty OR identifiability OR "ill-posed")'),
}


def get_json(url, params=None, retries=5, pause=1.0):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8")), url
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(pause * (2 ** i))
    raise RuntimeError(f"GET failed after {retries} tries: {url} :: {last}")


def get_text(url, retries=4, pause=1.0):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(pause * (2 ** i))
    raise RuntimeError(f"GET failed: {url} :: {last}")
