"""Revision history from a git repository as portable history records (XFER-7)."""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Callable, Optional

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slug(name: str) -> str:
    s = SLUG_RE.sub("-", name.casefold()).strip("-")
    return s or "anonymous"


def is_git_repo(path: Path) -> bool:
    try:
        out = subprocess.run(["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
                             capture_output=True, text=True, check=False)
        return out.returncode == 0 and out.stdout.strip() == "true"
    except FileNotFoundError:
        return False


def git_root(path: Path) -> Path:
    out = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def file_history(repo: Path, rel_path: str, convert: Optional[Callable[[str], str]] = None) -> tuple[list[dict], dict]:
    """Return (records oldest-first, users) for one file, following renames.

    Each record follows schemas/history-record.schema.json; `content` is the full file at that
    commit, passed through `convert` when given. Authors are recorded by name only (PRIV-3).
    """
    fmt = "%x1e%H%x1f%aI%x1f%aN%x1f%s"
    out = subprocess.run(
        ["git", "-C", str(repo), "log", "--follow", "--name-only", f"--format={fmt}", "--", rel_path],
        capture_output=True, text=True, check=True,
    ).stdout
    commits = []
    for chunk in out.split("\x1e"):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        header, _, rest = chunk.partition("\n")
        sha, at, author, subject = (header.split("\x1f") + ["", "", "", ""])[:4]
        names = [l.strip() for l in rest.split("\n") if l.strip()]
        commits.append({"sha": sha, "at": at, "author": author, "subject": subject, "name": names[0] if names else rel_path})
    commits.reverse()  # oldest first
    records, users = [], {}
    prev_rev, prev_name = None, None
    for i, c in enumerate(commits):
        uid = slug(c["author"])
        users.setdefault(uid, {"id": uid, "name": c["author"], "kind": "person"})
        rev = c["sha"][:12]
        show = subprocess.run(["git", "-C", str(repo), "show", f"{c['sha']}:{c['name']}"], capture_output=True, check=False)
        content = show.stdout.decode("utf-8", errors="replace") if show.returncode == 0 else ""
        if convert:
            content = convert(content)
        author = {"id": uid, "name": c["author"]}
        if prev_name is not None and c["name"] != prev_name:
            records.append({"rev": rev + "-mv", "parent": prev_rev, "type": "rename", "at": c["at"], "author": author,
                            "from": prev_name, "to": c["name"], "summary": c["subject"]})
            prev_rev = rev + "-mv"
        records.append({"rev": rev, "parent": prev_rev, "type": "create" if i == 0 else "edit", "at": c["at"],
                        "author": author, "summary": c["subject"], "content": content,
                        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()})
        prev_rev, prev_name = rev, c["name"]
    return records, users


def file_dates(repo: Path, rel_path: str) -> tuple[Optional[str], Optional[str]]:
    """(created, updated) ISO timestamps from git, following renames."""
    out = subprocess.run(["git", "-C", str(repo), "log", "--follow", "--format=%aI", "--", rel_path],
                         capture_output=True, text=True, check=False).stdout.split()
    if not out:
        return None, None
    return out[-1], out[0]
