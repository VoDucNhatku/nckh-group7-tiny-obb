import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

NAMES = ["airplane", "bridge", "storage-tank", "ship", "swimming-pool", "vehicle", "person", "wind-mill"]


def _poly(cx, cy, w, h, r):
    c, s = np.cos(r), np.sin(r)
    v1 = np.array([w / 2 * c, w / 2 * s])
    v2 = np.array([-h / 2 * s, h / 2 * c])
    ctr = np.array([cx, cy])
    return np.stack([ctr + v1 + v2, ctr + v1 - v2, ctr - v1 - v2, ctr - v1 + v2])


@pytest.fixture(scope="session")
def tiny_dataset(tmp_path_factory):
    """Dataset YOLO-OBB nhỏ: 4 ảnh train, 3 ảnh val, 128×128, vật 3–20 px. Trả về đường dẫn file yaml."""
    import cv2

    root = tmp_path_factory.mktemp("tinyds")
    rng = np.random.default_rng(0)
    for split, n in (("train", 4), ("val", 3)):
        (root / "images" / split).mkdir(parents=True)
        (root / "labels" / split).mkdir(parents=True)
        for i in range(n):
            img = (rng.random((128, 128, 3)) * 255).astype(np.uint8)
            lines = []
            for _ in range(int(rng.integers(3, 7))):
                cx, cy = rng.uniform(20, 108, 2)
                w, h = rng.uniform(3, 20), rng.uniform(3, 12)
                r = rng.uniform(0, np.pi)
                p = _poly(cx, cy, w, h, r)
                cv2.fillPoly(img, [p.astype(np.int32)], (255, 255, 255))
                lines.append(" ".join([str(int(rng.integers(0, 8)))] + [f"{v / 128:.6f}" for v in p.flatten()]))
            cv2.imwrite(str(root / "images" / split / f"im{i}.png"), img)
            (root / "labels" / split / f"im{i}.txt").write_text("\n".join(lines) + "\n")
    y = root / "tiny.yaml"
    y.write_text(f"path: {root.as_posix()}\ntrain: images/train\nval: images/val\nnames:\n"
                 + "".join(f"  {i}: {n}\n" for i, n in enumerate(NAMES)))
    return y


@pytest.fixture(scope="session")
def random_weights(tmp_path_factory):
    """Một checkpoint YOLO26n-OBB khởi tạo ngẫu nhiên (8 lớp), không tải gì từ mạng."""
    from ultralytics import YOLO
    from ultralytics.nn.tasks import OBBModel

    m = YOLO("yolo26n-obb.yaml")
    m.model = OBBModel("yolo26n-obb.yaml", nc=8, verbose=False)
    m.model.names = dict(enumerate(NAMES))
    m.model.args = {"task": "obb", "imgsz": 128}
    f = tmp_path_factory.mktemp("w") / "rand.pt"
    m.save(f)
    return f
