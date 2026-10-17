"""Tạo bảng nhân vật (turnaround sheet) cho "Trẻ con không được ăn thịt chó" bằng Codex CLI.

Ghép prompts/_style.txt + prompts/<nhân vật>.txt, đính kèm ảnh mẫu phong cách
(tham-chieu/mau_phong_cach.png, bảng Thị Nở của bộ Chí Phèo) rồi gọi `codex exec`.
Ảnh lưu ở <nhân vật>.png cạnh file này.

Ví dụ:
  python3 tao_bang_nhan_vat.py 01 06
  python3 tao_bang_nhan_vat.py --tat-ca -j 3
"""
import argparse
import glob
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
PROMPT_DIR = os.path.join(HERE, "prompts")
LOG_DIR = os.path.join(HERE, "log")
STYLE_REF = "tham-chieu/mau_phong_cach.png"


def load():
    style = open(os.path.join(PROMPT_DIR, "_style.txt"), encoding="utf-8").read().strip()
    chars = {}
    for path in sorted(glob.glob(os.path.join(PROMPT_DIR, "[0-9]*.txt"))):
        name = os.path.basename(path)[:-4]
        chars[name] = open(path, encoding="utf-8").read().strip()
    return style, chars


def run_one(style, name, body, overwrite=False, retries=1):
    dest = os.path.join(HERE, f"{name}.png")
    if os.path.exists(dest) and not overwrite:
        return name, "bỏ qua (đã có)"
    prompt = (f"{style}\n{body}\n\n"
              f"Use your image generation tool to create this single 16:9 image. "
              f"Then save the final PNG to ./{name}.png (copy it from wherever the image tool "
              f"stored it) and print the saved path. Do not create any other files.")
    log = os.path.join(LOG_DIR, f"{name}.log")
    for attempt in range(retries + 1):
        with open(log, "a", encoding="utf-8") as lf:
            lf.write(f"\n===== attempt {attempt + 1} =====\n")
            try:
                subprocess.run(
                    ["codex", "exec", "--skip-git-repo-check", "-s", "workspace-write",
                     "-i", STYLE_REF, "-"],
                    input=prompt, text=True, cwd=HERE, stdout=lf, stderr=subprocess.STDOUT,
                    timeout=900)
            except subprocess.TimeoutExpired:
                lf.write("TIMEOUT\n")
        if os.path.exists(dest) and os.path.getsize(dest) > 10_000:
            return name, f"xong (lần {attempt + 1})"
    return name, "LỖI (xem log)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="số nhân vật, ví dụ 01 06")
    ap.add_argument("--tat-ca", action="store_true", help="tạo tất cả nhân vật")
    ap.add_argument("--ghi-de", action="store_true", help="tạo lại cả ảnh đã có")
    ap.add_argument("-j", type=int, default=3, help="số ảnh chạy song song")
    a = ap.parse_args()

    style, chars = load()
    todo = {n: b for n, b in chars.items() if a.tat_ca or n[:2] in a.ids}
    if not todo:
        sys.exit("Không có nhân vật nào để tạo. Xem --help.")

    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"Tạo {len(todo)} bảng nhân vật, song song {a.j}…", flush=True)
    ok = fail = 0
    with ThreadPoolExecutor(max_workers=a.j) as ex:
        futs = [ex.submit(run_one, style, n, b, a.ghi_de) for n, b in todo.items()]
        for f in as_completed(futs):
            name, status = f.result()
            fail += status.startswith("LỖI")
            ok += not status.startswith("LỖI")
            print(f"[{ok + fail}/{len(todo)}] {name}: {status}", flush=True)
    print(f"Hoàn tất: {ok} thành công, {fail} lỗi.")


if __name__ == "__main__":
    main()
