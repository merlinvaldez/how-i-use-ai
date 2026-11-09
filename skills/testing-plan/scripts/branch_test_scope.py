#!/usr/bin/env python3
"""
Summarize branch changes into Vercel- and Supabase-oriented testing surfaces.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

JUNK_PREFIXES = (
    ".git/",
    ".next/",
    ".turbo/",
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
        capture_output=True,
        text=True,
        check=False,
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
    return len(parts) > 1 and parts[0].startswith(".") and parts[0] not in {".github", ".vercel"}


def is_env_template_path(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if is_junk_path(normalized):
        return False
    name = Path(normalized).name.lower()
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
            capture_output=True,
            text=True,
            check=False,
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
    return sorted(
        {
            normalize_repo_path(line.strip())
            for line in output.splitlines()
            if line.strip() and not is_junk_path(line.strip())
        }
    )


def route_from_app_page(path: str) -> str | None:
    match = re.match(r"^app/(.*)/page\.(?:js|jsx|ts|tsx|mdx)$", path)
    if not match:
        return None
    raw = match.group(1)
    if raw == "":
        return "/"
    segments = []
    for segment in raw.split("/"):
        if not segment or (segment.startswith("(") and segment.endswith(")")):
            continue
        segments.append(segment)
    return "/" + "/".join(segments)


def route_from_pages(path: str) -> str | None:
    match = re.match(r"^pages/(.+)\.(?:js|jsx|ts|tsx|html|mdx)$", path)
    if not match:
        return None
    raw = match.group(1)
    if raw.startswith("api/") or raw in {"_app", "_document", "_error"}:
        return None
    if raw == "index":
        return "/"
    if raw.endswith("/index"):
        raw = raw[:-6]
    return "/" + raw


def route_from_static_file(path: str) -> str | None:
    match = re.match(r"^([^/]+)\.html$", path)
    if not match:
        return None
    raw = match.group(1)
    return "/" if raw == "index" else f"/{raw}.html"


def api_path_from_file(path: str) -> str | None:
    patterns = (
        (r"^app/api/(.*)/route\.(?:js|jsx|ts|tsx)$", "/api/{}"),
        (r"^pages/api/(.*)\.(?:js|jsx|ts|tsx)$", "/api/{}"),
        (r"^api/(.*)\.(?:js|jsx|ts|tsx)$", "/api/{}"),
        (r"^supabase/functions/(.*?)/index\.(?:ts|js)$", "/functions/v1/{}"),
    )
    for pattern, template in patterns:
        match = re.match(pattern, path)
        if match:
            return template.format(match.group(1))
    return None


def add_env_refs_from_text(
    text: str,
    current_file: str,
    seen: set[tuple[str, str]],
    results: list[dict[str, str]],
) -> None:
    for pattern in ENV_REF_PATTERNS:
        for match in pattern.finditer(text):
            key = (match.group(1), current_file)
            if not current_file or key in seen:
                continue
            seen.add(key)
            results.append({"name": match.group(1), "path": current_file})


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
    for args in (
        ("diff", "--unified=0", "--no-color", f"{merge_base}..HEAD"),
        ("diff", "--cached", "--unified=0", "--no-color"),
        ("diff", "--unified=0", "--no-color"),
    ):
        collect_env_refs_from_diff_output(run_git(repo, *args), seen, results)

    for item in worktree_files:
        if item["status"] != "??":
            continue
        path = item["path"]
        if is_junk_path(path) or is_env_template_path(path):
            continue
        full_path = repo / path
        if not full_path.exists() or not full_path.is_file():
            continue
        try:
            content = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
        add_env_refs_from_text(content, path, seen, results)
    return sorted(results, key=lambda item: (item["name"], item["path"]))


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
        results[relative_path] = sorted(
            {
                match.group(1)
                for line in content.splitlines()
                if (match := key_pattern.match(line))
            }
        )
    return results


def infer_preview_routes(paths: list[str]) -> list[str]:
    routes: set[str] = set()
    for path in paths:
        normalized = normalize_repo_path(path)
        for resolver in (route_from_app_page, route_from_pages, route_from_static_file):
            route = resolver(normalized)
            if route:
                routes.add(route)
    return sorted(routes)


def infer_api_paths(paths: list[str]) -> list[str]:
    api_paths: set[str] = set()
    for path in paths:
        normalized = normalize_repo_path(path)
        api_path = api_path_from_file(normalized)
        if api_path:
            api_paths.add(api_path)
    return sorted(api_paths)


def classify_changed_paths(paths: list[str]) -> dict[str, bool]:
    lowered = [normalize_repo_path(path).lower() for path in paths]
    return {
        "frontend": any(
            path.endswith((".tsx", ".ts", ".jsx", ".js", ".html", ".css"))
            and not path.startswith("pages/api/")
            and not path.startswith("app/api/")
            and "/api/" not in f"/{path}/"
            for path in lowered
        ),
        "api": any(
            path.startswith("pages/api/")
            or path.startswith("app/api/")
            or path.startswith("supabase/functions/")
            or "/api/" in f"/{path}/"
            for path in lowered
        ),
        "env": any(is_env_template_path(path) or Path(path).name.startswith(".env") for path in lowered),
        "migration": any(
            path.startswith("supabase/migrations/")
            or "/migrations/" in f"/{path}/"
            or path.endswith(".sql")
            for path in lowered
        ),
        "auth": any(
            any(keyword in path for keyword in ("auth", "login", "signup", "session", "middleware"))
            for path in lowered
        ),
        "storage": any(
            any(keyword in path for keyword in ("storage", "bucket", "upload", "file"))
            for path in lowered
        ),
        "rls_or_policy": any(
            any(keyword in path for keyword in ("policy", "policies", "rls"))
            for path in lowered
        ),
        "cron_or_background": any(
            any(keyword in path for keyword in ("cron", "queue", "worker", "job", "schedule"))
            for path in lowered
        ),
    }


def load_vercel_project(repo: Path) -> dict[str, object] | None:
    project_path = repo / ".vercel" / "project.json"
    if not project_path.exists():
        return None
    try:
        return json.loads(project_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"path": str(project_path), "parse_error": True}


def detect_supabase_artifacts(files: list[str]) -> dict[str, list[str]]:
    normalized = [normalize_repo_path(path) for path in files]
    return {
        "migrations": [path for path in normalized if path.startswith("supabase/migrations/")],
        "functions": [path for path in normalized if path.startswith("supabase/functions/")],
        "seed_files": [
            path
            for path in normalized
            if path.startswith("supabase/seed")
            or path.endswith("/seed.sql")
            or Path(path).name in {"seed.sql", "seed.ts", "seed.js"}
        ],
        "storage_files": [path for path in normalized if "storage" in path or "bucket" in path],
    }


def build_focus_areas(
    classification: dict[str, bool],
    preview_routes: list[str],
    api_paths: list[str],
    missing_env_keys: list[str],
    supabase_artifacts: dict[str, list[str]],
) -> list[str]:
    focus: list[str] = []
    if preview_routes:
        focus.append("preview-routes")
    if classification["api"] or api_paths:
        focus.append("api-endpoints")
    if classification["migration"] or supabase_artifacts["migrations"]:
        focus.append("database-migrations")
    if classification["rls_or_policy"]:
        focus.append("rls-and-policies")
    if classification["auth"]:
        focus.append("auth-and-session")
    if classification["storage"] or supabase_artifacts["storage_files"]:
        focus.append("storage")
    if missing_env_keys or classification["env"]:
        focus.append("environment-variables")
    if classification["cron_or_background"]:
        focus.append("background-jobs")
    return focus


def build_suggested_checks(
    preview_routes: list[str],
    api_paths: list[str],
    missing_env_keys: list[str],
    classification: dict[str, bool],
    supabase_artifacts: dict[str, list[str]],
) -> list[str]:
    checks: list[str] = []
    if preview_routes:
        checks.append("Open the preview deployment and exercise these changed routes: " + ", ".join(preview_routes[:6]))
    if api_paths:
        checks.append("Call the changed server endpoints directly and verify status codes and payloads: " + ", ".join(api_paths[:6]))
    if missing_env_keys:
        checks.append("Verify the new env vars exist in the Vercel preview environment: " + ", ".join(missing_env_keys))
    if classification["migration"] or supabase_artifacts["migrations"]:
        checks.append("Verify the relevant Supabase migrations have been applied and match the expected schema.")
    if classification["rls_or_policy"]:
        checks.append("Verify signed-out, signed-in, and role-specific RLS behavior in Supabase and through the app.")
    if classification["auth"]:
        checks.append("Run sign-in, sign-out, and session persistence checks on the preview deployment.")
    if classification["storage"] or supabase_artifacts["storage_files"]:
        checks.append("Run upload, retrieval, and deletion checks for any changed Supabase storage flow.")
    if classification["cron_or_background"]:
        checks.append("Check deployment logs or function logs for the changed background behavior.")
    return checks


def build_report(repo: Path, base_ref: str) -> dict[str, object]:
    repo_root = Path(run_git(repo, "rev-parse", "--show-toplevel").strip())
    head_ref = run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    merge_base = run_git(repo_root, "merge-base", base_ref, "HEAD").strip()

    changed_files = parse_name_status(
        run_git(repo_root, "diff", "--name-status", "--find-renames", f"{merge_base}..HEAD")
    )
    worktree_files = parse_status_porcelain(
        run_git(repo_root, "status", "--porcelain=v1", "--untracked-files=all")
    )
    changed_paths = sorted(
        {normalize_repo_path(item["path"]) for item in changed_files}
        | {normalize_repo_path(item["path"]) for item in worktree_files}
    )

    preview_routes = infer_preview_routes(changed_paths)
    api_paths = infer_api_paths(changed_paths)
    all_files = tracked_and_untracked_files(repo_root)
    env_targets = [path for path in all_files if is_env_template_path(path)]
    env_template_keys = parse_env_template_keys(repo_root, env_targets)
    added_env_refs = collect_added_env_refs(repo_root, merge_base, worktree_files)
    documented_env_keys = {key for keys in env_template_keys.values() for key in keys}
    missing_env_keys = sorted({item["name"] for item in added_env_refs if item["name"] not in documented_env_keys})
    classification = classify_changed_paths(changed_paths)
    supabase_artifacts = detect_supabase_artifacts(all_files)
    focus_areas = build_focus_areas(classification, preview_routes, api_paths, missing_env_keys, supabase_artifacts)
    suggested_checks = build_suggested_checks(preview_routes, api_paths, missing_env_keys, classification, supabase_artifacts)

    return {
        "repo_root": str(repo_root),
        "head_ref": head_ref,
        "base_ref": base_ref,
        "merge_base": merge_base,
        "changed_files": changed_files,
        "worktree_files": worktree_files,
        "changed_paths": changed_paths,
        "preview_routes": preview_routes,
        "api_paths": api_paths,
        "env_template_targets": env_targets,
        "added_env_var_references": added_env_refs,
        "missing_env_keys": missing_env_keys,
        "classification": classification,
        "focus_areas": focus_areas,
        "suggested_checks": suggested_checks,
        "vercel_project": load_vercel_project(repo_root),
        "supabase_artifacts": supabase_artifacts,
    }


def render_markdown(report: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append("# Branch Test Scope")
    lines.append("")
    lines.append(f"- Repo root: `{report['repo_root']}`")
    lines.append(f"- Head branch: `{report['head_ref']}`")
    lines.append(f"- Base branch: `{report['base_ref']}`")
    lines.append(f"- Merge base: `{report['merge_base']}`")
    lines.append("")
    lines.append("## Changed Files")
    if report["changed_files"]:
        for item in report["changed_files"]:
            old_path = item.get("old_path")
            if old_path:
                lines.append(f"- `{item['status']}` `{old_path}` -> `{item['path']}`")
            else:
                lines.append(f"- `{item['status']}` `{item['path']}`")
    else:
        lines.append("- No committed branch delta found.")
    lines.append("")
    lines.append("## Uncommitted Files")
    if report["worktree_files"]:
        for item in report["worktree_files"]:
            lines.append(f"- `{item['status']}` `{item['path']}`")
    else:
        lines.append("- Working tree is clean.")
    lines.append("")
    lines.append("## Preview Routes")
    if report["preview_routes"]:
        for route in report["preview_routes"]:
            lines.append(f"- `{route}`")
    else:
        lines.append("- No route-like frontend paths inferred from the changed files.")
    lines.append("")
    lines.append("## API Paths")
    if report["api_paths"]:
        for path in report["api_paths"]:
            lines.append(f"- `{path}`")
    else:
        lines.append("- No API paths inferred from the changed files.")
    lines.append("")
    lines.append("## Supabase Artifacts")
    has_artifacts = False
    for label, paths in report["supabase_artifacts"].items():
        if not paths:
            continue
        has_artifacts = True
        lines.append(f"- {label}:")
        for path in paths[:10]:
            lines.append(f"  - `{path}`")
    if not has_artifacts:
        lines.append("- No explicit Supabase directories detected.")
    lines.append("")
    lines.append("## Missing Env Keys")
    if report["missing_env_keys"]:
        for key in report["missing_env_keys"]:
            lines.append(f"- `{key}`")
    else:
        lines.append("- No new undocumented env keys detected.")
    lines.append("")
    lines.append("## Focus Areas")
    if report["focus_areas"]:
        for area in report["focus_areas"]:
            lines.append(f"- `{area}`")
    else:
        lines.append("- No specific focus areas inferred from the branch delta.")
    lines.append("")
    lines.append("## Suggested Checks")
    if report["suggested_checks"]:
        for check in report["suggested_checks"]:
            lines.append(f"- {check}")
    else:
        lines.append("- No specific checks inferred; this looks like a low-impact delta.")
    lines.append("")
    lines.append("## Vercel Project")
    vercel_project = report["vercel_project"]
    if vercel_project is None:
        lines.append("- No `.vercel/project.json` file detected.")
    else:
        for key in ("projectId", "orgId", "projectName"):
            if key in vercel_project:
                lines.append(f"- `{key}`: `{vercel_project[key]}`")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize changed files into a Vercel + Supabase testing scope."
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
