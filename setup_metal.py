#!/usr/bin/env python3
"""Install paired official vLLM/Metal wheels into this project, never globally."""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "vllm-comparison"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", default="v0.30.0", help="Official Metal release tag")
    args = parser.parse_args()
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        parser.error("This installer requires native Apple Silicon macOS.")
    if int(platform.mac_ver()[0].split(".")[0]) < 15:
        parser.error("The official Metal wheels require macOS 15 or later.")
    uv = shutil.which("uv")
    if not uv:
        bootstrap = ROOT / ".bootstrap"
        python = bootstrap / "bin/python"
        if not python.exists():
            subprocess.run([sys.executable, "-m", "venv", str(bootstrap)], check=True)
        subprocess.run([str(python), "-m", "pip", "install", "--no-cache-dir", "uv"], check=True)
        uv = str(bootstrap / "bin/uv")
    env = dict(os.environ)
    env.update(UV_CACHE_DIR=str(ROOT / ".cache/uv"),
               UV_PYTHON_INSTALL_DIR=str(ROOT / ".cache/python"))
    release = json.loads(fetch("https://api.github.com/repos/vllm-project/vllm-metal/releases/tags/" + args.release))
    wheels = [a["browser_download_url"] for a in release["assets"]
              if a["name"].endswith("cp312-cp312-macosx_15_0_arm64.whl")]
    if len(wheels) != 1:
        raise RuntimeError("Release must contain exactly one native Python 3.12 Metal wheel.")
    core_tag = fetch("https://raw.githubusercontent.com/vllm-project/vllm-metal/" + args.release
                     + "/.github/vllm-release-tag.commit").strip()
    # The Metal project publishes which vLLM core version its release needs.
    if not core_tag.startswith("v") or any(c not in "0123456789.vpost" for c in core_tag):
        raise RuntimeError("Unexpected upstream vLLM release tag: " + core_tag)
    version = core_tag[1:]
    core_wheel = ("https://github.com/vllm-project/vllm/releases/download/" + core_tag
                  + "/vllm-" + version + "%2Bcpu-cp312-cp312-macosx_11_0_arm64.whl")
    python = ROOT / ".venv/bin/python"
    if not python.exists():
        subprocess.run([uv, "venv", str(ROOT / ".venv"), "--python", "3.12", "--seed"], env=env, check=True)
    subprocess.run([uv, "pip", "install", "--python", str(python), core_wheel, wheels[0]], env=env, check=True)
    (ROOT / "installation.json").write_text(json.dumps({
        "metal_release": args.release, "vllm_release": core_tag,
        "metal_wheel": wheels[0], "vllm_wheel": core_wheel,
    }, indent=2) + "\n")
    print("Ready. Run: .venv/bin/python compare_vllm.py")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print("Installation failed: " + str(error), file=sys.stderr)
        sys.exit(1)
