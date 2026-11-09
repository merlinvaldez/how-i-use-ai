#!/usr/bin/env python3
"""
Summarize documentation-relevant changes between the current branch and a base branch.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DOC_SUFFIXES = {".md", ".mdx", ".rst", ".adoc", ".txt"}
JUNK_PREFIXES = (
    ".git/",
    ".next/",
    ".turbo/",
    ".vercel/",
    ".codex-skill-staging/",
    "node_modules/",
    "dist/",
    "build/",
    "coverage/",
    ".venv/",
    "venv/",
)
ENV_TEMPLATE_NAMES = {
    ".env.example",
    ".env.sample",
    ".env.template",
    ".env.local.example",
    ".env.development.example",
    ".env.production.example",
    "example.env",
    "sample.env",
}
ENV_REF_PATTERNS = (
    re.compile(r"process\.env\.([A-Z][A-Z0-9_]*)"),
    re.compile(r"process\.env\[['\"]([A-Z][A-Z0-9_]*)['\"]\]"),
    re.compile(r"import\.meta\.env\.([A-Z][A-Z0-9_]*)"),
    re.compile(r"os\.environ\[['\"]([A-Z][A-Z0-9_]*)['\"]\]"),
    re.compile(r"os\.getenv\(['\"]([A-Z][A-Z0-9_]*)['\"]"),
    re.compile(r"getenv\(['\"]([A-Z][A-Z0-9_]*)['\"]"),
    re.compile(r"ENV\[['\"]([A-Z][A-Z0-9_]*)['\"]\]"),
    re.compile(r"System\.getenv\(['\"]([A-Z][A-Z0-9_]*)['\"]"),
)


def run_git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"git {' '.join(args)} failed")
    return completed.stdout


def normalize_repo_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_junk_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if any(normalized.startswith(prefix) for prefix in JUNK_PREFIXES):
        return True
    parts = Path(normalized).parts
    return len(parts) > 1 and parts[0].startswith(".") and parts[0] not in {".github"}


def is_doc_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if is_junk_path(normalized):
        return False
    file_path = Path(normalized)
    name = file_path.name.lower()
    return name.startswith("readme") or file_path.suffix.lower() in DOC_SUFFIXES or normalized.startswith("docs/")


def is_env_template_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if is_junk_path(normalized):
        return False
    file_path = Path(normalized)
    name = file_path.name.lower()
    return (
        name in ENV_TEMPLATE_NAMES
        or name.endswith(".env.example")
        or name.endswith(".env.sample")
        or name.endswith(".env.template")
    )


def normalize_base_ref(repo: Path, requested: str) -> str:
    candidates = [requested]
    if requested == "main":
        candidates.extend(["origin/main", "master", "origin/master"])
    for candidate in candidates:
        completed = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", candidate],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode == 0:
            return candidate
    raise RuntimeError(f"Could not resolve base ref '{requested}'")


def parse_name_status(output: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split("\t")
        status_token = parts[0]
        status = status_token[:1]
        if status in {"R", "C"} and len(parts) >= 3:
            items.append({"status": status, "path": parts[2], "old_path": parts[1]})
        elif len(parts) >= 2:
            items.append({"status": status, "path": parts[1]})
    return [item for item in items if not is_junk_path(item["path"])]


def parse_status_porcelain(output: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for raw_line in output.splitlines():
        if not raw_line:
            continue
        status = raw_line[:2].strip() or "?"
        path = raw_line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not is_junk_path(path):
            items.append({"status": status, "path": path})
    return items


def tracked_and_untracked_files(repo: Path) -> list[str]:
    output = run_git(repo, "ls-files", "--cached", "--others", "--exclude-standard")
    files = [line.strip() for line in output.splitlines() if line.strip()]
    return sorted({path for path in files if not is_junk_path(path)})


def parse_env_template_keys(repo: Path, env_targets: list[str]) -> dict[str, list[str]]:
    key_pattern = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=")
    results: dict[str, list[str]] = {}
    for relative_path in env_targets:
        full_path = repo / relative_path
        if not full_path.exists() or not full_path.is_file():
            continue
        try:
            content = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        keys: list[str] = []
        for line in content.splitlines():
            match = key_pattern.match(line)
            if match:
                keys.append(match.group(1))
        results[relative_path] = sorted(set(keys))
    return results


def add_env_refs_from_text(
    text: str,
    current_file: str,
    seen: set[tuple[str, str]],
    results: list[dict[str, str]],
) -> None:
    for pattern in ENV_REF_PATTERNS:
        for match in pattern.finditer(text):
            name = match.group(1)
            key = (name, current_file)
            if not current_file or key in seen:
                continue
            seen.add(key)
            results.append({"name": name, "path": current_file})


def collect_env_refs_from_diff_output(
    diff_output: str,
    seen: set[tuple[str, str]],
    results: list[dict[str, str]],
) -> None:
    current_file = ""
    for line in diff_output.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        add_env_refs_from_text(line, current_file, seen, results)


def collect_added_env_refs(
    repo: Path,
    merge_base: str,
    worktree_files: list[dict[str, str]],
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    collect_env_refs_from_diff_output(
        run_git(repo, "diff", "--unified=0", "--no-color", f"{merge_base}..HEAD"),
        seen,
        results,
    )
    collect_env_refs_from_diff_output(
        run_git(repo, "diff", "--cached", "--unified=0", "--no-color"),
        seen,
        results,
    )
    collect_env_refs_from_diff_output(
        run_git(repo, "diff", "--unified=0", "--no-color"),
        seen,
        results,
    )

    for item in worktree_files:
        if item["status"] != "??":
            continue
        relative_path = item["path"]
        if is_junk_path(relative_path) or is_doc_path(relative_path) or is_env_template_path(relative_path):
            continue
        full_path = repo / relative_path
        if not full_path.exists() or not full_path.is_file():
            continue
        try:
            content = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        add_env_refs_from_text(content, relative_path, seen, results)

    return sorted(results, key=lambda item: (item["name"], item["path"]))


def classify_paths(paths: list[str]) -> dict[str, bool]:
    normalized = [path.replace("\\", "/").lower() for path in paths]
    return {
        "dependency_changed": any(
            Path(path).name in {
                "package.json",
                "package-lock.json",
                "pnpm-lock.yaml",
                "yarn.lock",
                "requirements.txt",
                "requirements-dev.txt",
                "pyproject.toml",
                "poetry.lock",
                "composer.json",
                "cargo.toml",
                "go.mod",
            }
            for path in normalized
        ),
        "config_changed": any(
            path.startswith("config/")
            or path.startswith(".github/")
            or Path(path).name.startswith(".env")
            or Path(path).name
            in {
                "vercel.json",
                "docker-compose.yml",
                "docker-compose.yaml",
                "dockerfile",
            }
            for path in normalized
        ),
        "api_or_route_changed": any(
            "/api/" in f"/{path}/"
            or "/routes/" in f"/{path}/"
            or path.startswith("pages/api/")
            or path.startswith("app/api/")
            for path in normalized
        ),
        "script_or_cli_changed": any(
            path.startswith("scripts/")
            or path.startswith("bin/")
            or Path(path).name.endswith((".sh", ".ps1"))
            for path in normalized
        ),
        "source_changed": any(
            not is_doc_path(path)
            and not is_env_template_path(path)
            and Path(path).suffix.lower()
            in {
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
                ".py",
                ".rb",
                ".go",
                ".rs",
                ".java",
                ".cs",
                ".php",
                ".swift",
                ".kt",
                ".sql",
                ".json",
                ".yaml",
                ".yml",
            }
            for path in normalized
        ),
    }


def build_suggestions(
    documentation_targets: list[str],
    changed_doc_files: list[str],
    env_targets: list[str],
    missing_env_keys: list[str],
    classification: dict[str, bool],
    changed_paths: list[str],
) -> list[str]:
    suggestions: list[str] = []
    if not changed_paths:
        return ["No branch delta detected against the selected base branch."]
    if missing_env_keys and env_targets:
        suggestions.append(
            "Update example env files with missing keys: " + ", ".join(missing_env_keys)
        )
    if missing_env_keys and not env_targets:
        suggestions.append(
            "No example env file was found; create one or document required env vars in the README."
        )
    if classification["dependency_changed"]:
        suggestions.append("Refresh README setup, install, and local development command sections.")
    if classification["config_changed"]:
        suggestions.append("Refresh configuration docs and any setup steps that depend on changed config.")
    if classification["api_or_route_changed"]:
        suggestions.append("Review API, route, or integration docs for stale request or path details.")
    if classification["script_or_cli_changed"]:
        suggestions.append("Review CLI or script usage docs so command examples stay accurate.")
    if classification["source_changed"] and not changed_doc_files:
        suggestions.append(
            "Source files changed without matching doc edits; inspect README and docs surfaces for drift."
        )
    if documentation_targets and not changed_doc_files:
        suggestions.append(
            "Likely doc targets to inspect first: " + ", ".join(documentation_targets[:5])
        )
    return suggestions


def build_report(repo: Path, base_ref: str) -> dict[str, object]:
    repo_root = Path(run_git(repo, "rev-parse", "--show-toplevel").strip())
    head_ref = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    merge_base = run_git(repo_root, "merge-base", base_ref, "HEAD").strip()

    changed_files = parse_name_status(
        run_git(repo_root, "diff", "--name-status", "--find-renames", f"{merge_base}..HEAD")
    )
    worktree_files = parse_status_porcelain(
        run_git(repo_root, "status", "--porcelain=v1", "--untracked-files=normal")
    )

    known_files = tracked_and_untracked_files(repo_root)
    documentation_targets = [path for path in known_files if is_doc_path(path)]
    env_targets = [path for path in known_files if is_env_template_path(path)]

    changed_paths = sorted(
        {item["path"] for item in changed_files} | {item["path"] for item in worktree_files}
    )
    changed_doc_files = sorted(path for path in changed_paths if is_doc_path(path))
    changed_env_templates = sorted(path for path in changed_paths if is_env_template_path(path))

    added_env_refs = collect_added_env_refs(repo_root, merge_base, worktree_files)
    env_template_keys = parse_env_template_keys(repo_root, env_targets)
    documented_env_keys = {
        key for keys in env_template_keys.values() for key in keys
    }
    missing_env_keys = sorted(
        {item["name"] for item in added_env_refs if item["name"] not in documented_env_keys}
    )

    classification = classify_paths(changed_paths)
    suggestions = build_suggestions(
        documentation_targets=documentation_targets,
        changed_doc_files=changed_doc_files,
        env_targets=env_targets,
        missing_env_keys=missing_env_keys,
        classification=classification,
        changed_paths=changed_paths,
    )

    return {
        "repo_root": str(repo_root),
        "head_ref": head_ref,
        "base_ref": base_ref,
        "merge_base": merge_base,
        "changed_files": changed_files,
        "worktree_files": worktree_files,
        "documentation_targets": documentation_targets,
        "changed_documentation_files": changed_doc_files,
        "env_template_targets": env_targets,
        "changed_env_templates": changed_env_templates,
        "added_env_var_references": added_env_refs,
        "missing_env_keys": missing_env_keys,
        "suggested_actions": suggestions,
    }


def render_markdown(report: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append("# Branch Doc Delta")
    lines.append("")
    lines.append(f"- Repo root: `{report['repo_root']}`")
    lines.append(f"- Head branch: `{report['head_ref']}`")
    lines.append(f"- Base branch: `{report['base_ref']}`")
    lines.append(f"- Merge base: `{report['merge_base']}`")
    lines.append("")

    changed_files = report["changed_files"]
    lines.append("## Changed Files")
    if changed_files:
        for item in changed_files:
            old_path = item.get("old_path")
            if old_path:
                lines.append(f"- `{item['status']}` `{old_path}` -> `{item['path']}`")
            else:
                lines.append(f"- `{item['status']}` `{item['path']}`")
    else:
        lines.append("- No committed branch delta found.")
    lines.append("")

    worktree_files = report["worktree_files"]
    lines.append("## Uncommitted Files")
    if worktree_files:
        for item in worktree_files:
            lines.append(f"- `{item['status']}` `{item['path']}`")
    else:
        lines.append("- Working tree is clean.")
    lines.append("")

    lines.append("## Documentation Targets")
    doc_targets = report["documentation_targets"]
    if doc_targets:
        for path in doc_targets[:20]:
            lines.append(f"- `{path}`")
        if len(doc_targets) > 20:
            lines.append(f"- ... {len(doc_targets) - 20} more")
    else:
        lines.append("- No documentation targets detected.")
    lines.append("")

    lines.append("## Env Template Targets")
    env_targets = report["env_template_targets"]
    if env_targets:
        for path in env_targets:
            lines.append(f"- `{path}`")
    else:
        lines.append("- No example env files detected.")
    lines.append("")

    lines.append("## Added Env Variable References")
    env_refs = report["added_env_var_references"]
    if env_refs:
        for item in env_refs:
            lines.append(f"- `{item['name']}` in `{item['path']}`")
    else:
        lines.append("- No added env var references detected in the branch diff.")
    lines.append("")

    lines.append("## Missing Env Keys")
    missing_keys = report["missing_env_keys"]
    if missing_keys:
        for key in missing_keys:
            lines.append(f"- `{key}`")
    else:
        lines.append("- No missing env keys detected from the branch diff.")
    lines.append("")

    lines.append("## Suggested Actions")
    for item in report["suggested_actions"]:
        lines.append(f"- {item}")
    lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize doc-relevant branch changes relative to a base branch."
    )
    parser.add_argument("--repo", default=".", help="Path to the git repository root or a child path.")
    parser.add_argument("--base", default="main", help="Base branch or ref to compare against.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    try:
        base_ref = normalize_base_ref(repo, args.base)
        report = build_report(repo, base_ref)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
