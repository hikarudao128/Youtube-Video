"""Tạo ảnh từng phân cảnh "Trẻ con không được ăn thịt chó" bằng Codex CLI.

Đọc KHỐI PHONG CÁCH CHUNG trong PROMPT_PHAN_CANH.md và prompt cảnh trong
phan-canh-prompt/chuong_*.md, đính kèm bảng nhân vật tương ứng rồi gọi
`codex exec`. Ảnh lưu ở phan-canh/canh_<x>_<y>.png.

Ví dụ:
  python3 tao_phan_canh.py 0.1 2.3
  python3 tao_phan_canh.py --chuong 2
  python3 tao_phan_canh.py --tat-ca -j 4
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(HERE, "PROMPT_PHAN_CANH.md")
SCENE_GLOB = os.path.join(HERE, "phan-canh-prompt", "chuong_*.md")
OUT_DIR = os.path.join(HERE, "phan-canh")
LOG_DIR = os.path.join(OUT_DIR, "log")
SHEETS = {
    "01": "01_nguoi_bo.png",
    "02": "02_nguoi_me.png",
    "03": "03_cai_gai.png",
    "04": "04_cu_nhon.png",
    "05": "05_cu_nho.png",
    "06": "06_cu_con.png",
    "07": "07_mu_vu.png",
    "08": "08_con_cho.png",
    "09": "09_ba_ong_khach.png",
}
# Cảnh không có nhân vật chính vẫn đính kèm 2 bảng này để giữ phong cách vẽ.
STYLE_ONLY = ["01", "02"]

SCENE_RE = re.compile(
    r"#### CẢNH (\d+\.\d+)[^\n]*\n(?:Lời dẫn:[^\n]*\n)?Tham chiếu: ([^\n]*)\n```text\n(.*?)\n```", re.S)


def load():
    text = open(PROMPT_FILE, encoding="utf-8").read()
    style = re.search(r"KHỐI PHONG CÁCH CHUNG[^\n]*\n\n```text\n(.*?)\n```", text, re.S).group(1)
    scenes = []
    for path in sorted(glob.glob(SCENE_GLOB)):
        for sid, refs, body in SCENE_RE.findall(open(path, encoding="utf-8").read()):
            codes = re.findall(r"\b0[1-9]\b", refs)
            scenes.append({"id": sid, "refs": codes, "body": body.strip()})
    scenes.sort(key=lambda s: tuple(map(int, s["id"].split("."))))
    return style, scenes


def out_path(sid):
    return os.path.join(OUT_DIR, f"canh_{sid.replace('.', '_')}.png")


def build_prompt(style, sc, dest):
    if sc["refs"]:
        note = ("Attached character sheets: " +
                ", ".join(SHEETS[c].rsplit(".", 1)[0] for c in sc["refs"]) +
                ". Draw these characters exactly as on their sheets.")
    else:
        note = ("The attached sheets are STYLE references only; none of those characters "
                "appear in this scene unless the scene text says so.")
    rel = os.path.relpath(dest, HERE)
    return (f"{style} {sc['body']}\n\n{note}\n\n"
            f"Use your image generation tool to create this single 16:9 image. "
            f"Then save the final PNG to ./{rel} (copy it from wherever the image tool "
            f"stored it; create the folder if needed) and print the saved path. "
            f"Do not create any other files.")


QUOTA_HIT = threading.Event()


def run_one(style, sc, overwrite=False, retries=1):
    dest = out_path(sc["id"])
    if os.path.exists(dest) and not overwrite:
        return sc["id"], "bỏ qua (đã có)"
    if QUOTA_HIT.is_set():
        return sc["id"], "LỖI (hết quota Codex, bỏ qua)"
    # Vẽ ra file tạm; chỉ thay ảnh cũ khi đã có ảnh mới.
    tmp = dest[:-4] + "_moi.png"
    if os.path.exists(tmp):
        os.remove(tmp)
    codes = sc["refs"] or STYLE_ONLY
    images = ",".join(SHEETS[c] for c in codes)
    prompt = build_prompt(style, sc, tmp)
    log = os.path.join(LOG_DIR, f"canh_{sc['id'].replace('.', '_')}.log")
    for attempt in range(retries + 1):
        start = os.path.getsize(log) if os.path.exists(log) else 0
        with open(log, "a", encoding="utf-8") as lf:
            lf.write(f"\n===== attempt {attempt + 1} =====\n")
            try:
                subprocess.run(
                    ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write",
                     "-i", images, "-"],
                    input=prompt, text=True, cwd=HERE, stdout=lf, stderr=subprocess.STDOUT,
                    timeout=900)
            except subprocess.TimeoutExpired:
                lf.write("TIMEOUT\n")
        if os.path.exists(tmp) and os.path.getsize(tmp) > 10_000:
            os.replace(tmp, dest)
            return sc["id"], f"xong (lần {attempt + 1})"
        with open(log, encoding="utf-8", errors="ignore") as lf:
            lf.seek(start)
            if "usage limit" in lf.read().lower():
                QUOTA_HIT.set()
                return sc["id"], "LỖI (hết quota Codex, xem log)"
    return sc["id"], "LỖI (xem log)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="số cảnh, ví dụ 0.1 2.3")
    ap.add_argument("--chuong", type=int, action="append", help="tạo cả một chương (lặp lại được)")
    ap.add_argument("--tat-ca", action="store_true", help="tạo tất cả cảnh")
    ap.add_argument("--ghi-de", action="store_true", help="tạo lại cả cảnh đã có ảnh")
    ap.add_argument("-j", type=int, default=3, help="số cảnh chạy song song")
    a = ap.parse_args()

    style, scenes = load()
    if a.tat_ca:
        todo = scenes
    elif a.chuong:
        todo = [s for s in scenes if int(s["id"].split(".")[0]) in a.chuong]
    else:
        todo = [s for s in scenes if s["id"] in a.ids]
    if not todo:
        sys.exit("Không có cảnh nào để tạo. Xem --help.")

    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"Tạo {len(todo)} cảnh, song song {a.j}…", flush=True)
    ok = fail = 0
    with ThreadPoolExecutor(max_workers=a.j) as ex:
        futs = [ex.submit(run_one, style, s, a.ghi_de) for s in todo]
        for f in as_completed(futs):
            sid, status = f.result()
            fail += status.startswith("LỖI")
            ok += not status.startswith("LỖI")
            print(f"[{ok + fail}/{len(todo)}] cảnh {sid}: {status}", flush=True)
    print(f"Hoàn tất: {ok} thành công, {fail} lỗi.")


if __name__ == "__main__":
    main()
