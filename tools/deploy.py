#!/usr/bin/env python3
"""Deploy the built site to its Sankara.net subtree over SSH.

This mirrors .github/workflows/deploy-hetzner.yml step for step: the same
build, the same payload checks, the same guarded remote path, the same rsync
flags, the same post-deploy smoke check. A local run and an Actions run should
put the same bytes in the same place.

Deploy settings are never stored here. They are resolved in the order the
sankara-net-ops skill documents:

  1. ~/.config/sankara-net/env/main.env
  2. the surface env, ~/.config/sankara-net/env/surfaces/<SURFACE>.env
  3. an SSH alias, read with `ssh -G` (which resolves config without
     connecting)
  4. explicit --host / --user / --key arguments

Values are read, never printed. When something is missing this reports the
key or file by name and stops.

Usage:

    python tools/deploy.py --dry-run
    python tools/deploy.py --yes
    python tools/deploy.py --yes --ssh-alias <alias>
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

# The surface this script is allowed to write to. Both are literals and both
# are asserted before anything connects: a deploy that has drifted off its own
# subtree should fail here rather than on the server, where --delete would
# already be loose in a tree this repo does not own.
REMOTE_PATH = "/var/www/sankara.net/astro/solar-eclipses/"
PUBLIC_URL = "https://sankara.net/astro/solar-eclipses/computing.html"
SMOKE_STRING = "Computing Solar Eclipses"
SURFACE = "astro-solar-eclipses"

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

CONFIG_ROOT = Path(
    os.environ.get("SANKARA_NET_CONFIG_ROOT", Path.home() / ".config" / "sankara-net")
)
MAIN_ENV = CONFIG_ROOT / "env" / "main.env"
SURFACE_ENV = CONFIG_ROOT / "env" / "surfaces" / f"{SURFACE}.env"

# The payload files the workflow asserts before it will deploy.
REQUIRED = [
    "computing.html",
    "assets/site.css",
    "assets/site.js",
    "assets/site3d.js",
]

SAFE_HOST = re.compile(r"^[A-Za-z0-9.-]+$")
SAFE_USER = re.compile(r"^[A-Za-z0-9._-]+$")


class DeployError(Exception):
    """Raised when a deploy invariant or a configuration lookup fails."""


def log(message: str) -> None:
    print(f"==> {message}", flush=True)


# ------------------------------------------------------------------ settings

def parse_env_file(path: Path) -> dict[str, str]:
    """Read the KEY=VALUE format the Sankara.net deploy config uses."""
    values: dict[str, str] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        key, sep, value = line.partition("=")
        if not sep:
            raise DeployError(f"{path.name}: invalid assignment at line {number}.")
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise DeployError(f"{path.name}: invalid key at line {number}.")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def from_ssh_alias(alias: str) -> dict[str, str]:
    """Resolve an SSH alias with `ssh -G`, which reads config without connecting."""
    if not SAFE_HOST.fullmatch(alias):
        raise DeployError("SSH alias contains unsupported characters.")
    ssh = shutil.which("ssh")
    if not ssh:
        raise DeployError("ssh was not found on PATH.")
    proc = subprocess.run(
        [ssh, "-G", alias], capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise DeployError(f"`ssh -G {alias}` failed; is the alias defined?")
    found: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        field, _, value = line.partition(" ")
        field = field.lower()
        if field in ("hostname", "user") and value:
            found[field] = value.strip()
        elif field == "identityfile" and value and "key" not in found:
            found["key"] = os.path.expanduser(value.strip())
    if "hostname" not in found:
        raise DeployError(f"`ssh -G {alias}` did not resolve a hostname.")
    return found


def resolve_settings(args: argparse.Namespace) -> dict[str, str]:
    """Walk the documented lookup order and report what is missing by name."""
    host = user = key = ""
    tried: list[str] = []

    for env_path in (MAIN_ENV, SURFACE_ENV):
        if env_path.is_file():
            values = parse_env_file(env_path)
            host = values.get("SANKARA_NET_HETZNER_HOST", host)
            user = values.get("SANKARA_NET_HETZNER_USER", user)
            key = values.get("SANKARA_NET_HETZNER_SSH_KEY", key)
            tried.append(str(env_path))
        else:
            tried.append(f"{env_path} (absent)")

    if args.ssh_alias:
        found = from_ssh_alias(args.ssh_alias)
        host = found.get("hostname", host)
        user = found.get("user", user)
        key = found.get("key", key)
        tried.append(f"ssh -G {args.ssh_alias}")

    host = args.host or host
    user = args.user or user
    key = args.key or key

    missing = [
        name
        for name, value in (
            ("SANKARA_NET_HETZNER_HOST", host),
            ("SANKARA_NET_HETZNER_USER", user),
            ("SANKARA_NET_HETZNER_SSH_KEY", key),
        )
        if not value
    ]
    if missing:
        raise DeployError(
            "Deploy settings are incomplete.\n"
            f"  missing: {', '.join(missing)}\n"
            "  looked in: " + "\n             ".join(tried) + "\n"
            "Set them in the env file, pass --ssh-alias, or pass --host/--user/--key."
        )

    if not SAFE_HOST.fullmatch(host):
        raise DeployError("Hetzner host contains unsupported characters.")
    if not SAFE_USER.fullmatch(user):
        raise DeployError("Hetzner user contains unsupported characters.")

    key_path = Path(os.path.expanduser(key))
    if not key_path.is_file():
        raise DeployError("The configured SSH key path does not exist.")

    return {"host": host, "user": user, "key": str(key_path)}


# --------------------------------------------------------------------- build

def run(command: list[str], where: Path) -> None:
    proc = subprocess.run(command, cwd=where, check=False)
    if proc.returncode != 0:
        raise DeployError(f"{command[0]} {command[1] if len(command) > 1 else ''} failed.")


def build() -> None:
    log("building")
    run([sys.executable, "tools/merge_refs.py"], ROOT)
    run([sys.executable, "tools/build.py", "--clean"], ROOT)
    # The public URL ends in computing.html; the build's home page is the page
    # that belongs there. The rest of the tree ships with it so the links and
    # assets that page uses keep resolving.
    shutil.copyfile(SITE / "index.html", SITE / "computing.html")


def verify_payload() -> None:
    log("verifying payload")
    if REMOTE_PATH != "/var/www/sankara.net/astro/solar-eclipses/":
        raise DeployError("The remote path guard has been altered.")
    for name in REQUIRED:
        if not (SITE / name).is_file():
            raise DeployError(f"missing from the build: {name}")
    landing = (SITE / "computing.html").read_text(encoding="utf-8", errors="replace")
    if "<title>" not in landing:
        raise DeployError("computing.html has no <title>.")
    if SMOKE_STRING not in landing:
        raise DeployError(
            f"computing.html does not contain {SMOKE_STRING!r}, "
            "which the post-deploy check greps for."
        )


# -------------------------------------------------------------------- deploy

def rsync(settings: dict[str, str], dry_run: bool) -> None:
    rsync_bin = shutil.which("rsync")
    if not rsync_bin:
        raise DeployError("rsync was not found on PATH.")
    ssh_command = (
        f"ssh -i {settings['key']} -o IdentitiesOnly=yes"
        " -o StrictHostKeyChecking=accept-new"
        " -o ServerAliveInterval=30 -o ServerAliveCountMax=10"
    )
    # --delete is safe only because REMOTE_PATH is a checked literal naming a
    # subtree this repo owns outright. /var/www/sankara.net/ is shared.
    command = [rsync_bin, "-avz", "--delete"]
    if dry_run:
        command.append("--dry-run")
    command += [
        "-e", ssh_command,
        f"{SITE.as_posix()}/",
        f"{settings['user']}@{settings['host']}:{REMOTE_PATH}",
    ]
    log(f"rsync{' --dry-run' if dry_run else ''} -> {REMOTE_PATH}")
    proc = subprocess.run(command, check=False)
    if proc.returncode != 0:
        raise DeployError(f"rsync exited {proc.returncode}.")


def verify_live() -> None:
    log(f"checking {PUBLIC_URL}")
    request = urllib.request.Request(
        PUBLIC_URL, headers={"User-Agent": "eclipse-research-deploy"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise DeployError(f"{PUBLIC_URL} returned {response.status}.")
        body = response.read().decode("utf-8", errors="replace")
    if SMOKE_STRING not in body:
        raise DeployError(f"{PUBLIC_URL} does not contain {SMOKE_STRING!r}.")
    log("live page looks right")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="build, verify, and show what rsync would transfer")
    parser.add_argument("--yes", action="store_true",
                        help="perform the live deploy")
    parser.add_argument("--ssh-alias",
                        help="resolve host/user/key from this SSH config alias")
    parser.add_argument("--host", help="override the Hetzner host")
    parser.add_argument("--user", help="override the deploy user")
    parser.add_argument("--key", help="override the SSH key path")
    parser.add_argument("--skip-build", action="store_true",
                        help="deploy the existing site/ without rebuilding")
    args = parser.parse_args()

    if not args.dry_run and not args.yes:
        parser.error("pass --dry-run or --yes")

    try:
        settings = resolve_settings(args)
        if not args.skip_build:
            build()
        verify_payload()
        rsync(settings, dry_run=args.dry_run)
        if args.dry_run:
            log("dry run only; nothing was written to the server")
            return 0
        verify_live()
    except DeployError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
