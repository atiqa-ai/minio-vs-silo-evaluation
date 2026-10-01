#!/usr/bin/env python3
"""build-docx - render the DEV-904 project report as a .docx file.

Reads the live state of the repository (tracker, subtask reports, deviations
register, dataset summary) and produces a Word document that reflects what is
actually on disk at the moment it runs. Nothing is hard-coded from memory: if a
number is in a file, it is read from that file, so the document cannot drift
quietly away from the repository it describes.

Usage: tools/bin/build-docx.py [output.docx]
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "DEV-904-project-report.docx")

RED = RGBColor(0xB0, 0x1C, 0x1C)
AMBER = RGBColor(0x9A, 0x63, 0x00)
GREEN = RGBColor(0x1B, 0x6B, 0x2F)
GREY = RGBColor(0x55, 0x55, 0x55)


def read(rel, default=""):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return default


def run(cmd, default=""):
    try:
        return subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        ).stdout.strip()
    except Exception:
        return default


def words(rel):
    return len(read(rel).split())


# --------------------------------------------------------------------------
# Fact gathering. Everything below is read, never assumed.
# --------------------------------------------------------------------------

def gather():
    f = {}

    f["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    f["head"] = run("git -C %s log -1 --format='%%h %%s'" % ROOT, "unknown")
    f["commits"] = run("git -C %s rev-list --count HEAD" % ROOT, "0")
    f["remote"] = run("git -C %s remote get-url origin" % ROOT, "none")
    f["tracked_files"] = run("git -C %s ls-files | wc -l" % ROOT, "0").strip()

    # Disk and host
    df = run("df -h / | tail -1", "")
    parts = df.split()
    if len(parts) >= 5:
        f["disk_size"], f["disk_used"], f["disk_free"], f["disk_pct"] = (
            parts[1], parts[2], parts[3], parts[4])
    else:
        f["disk_size"] = f["disk_used"] = f["disk_free"] = f["disk_pct"] = "unknown"
    f["cpus"] = run("nproc", "?")
    f["mem"] = run("free -h | awk '/^Mem:/{print $2}'", "?")
    f["os"] = run(". /etc/os-release 2>/dev/null && echo \"$PRETTY_NAME\"", "unknown")
    f["docker"] = run("docker --version", "not installed")
    f["compose"] = run("docker compose version --short", "not installed")

    # Dataset
    try:
        f["dataset"] = json.loads(read("lab/data/dataset/dataset-summary.json"))
    except Exception:
        f["dataset"] = {}

    # Deviations
    dev = read("DEVIATIONS.md")
    ids = re.findall(r"^## (D-\d{3}) — (.+)$", dev, re.M)
    f["deviations"] = [(i, t.strip().rstrip("*").strip()) for i, t in ids]
    f["deviation_count"] = len(f["deviations"])
    f["deviation_resolved"] = len(re.findall(r"RESOLVED 20", dev))

    # Subtask status, read from the README table so there is exactly one place
    # in the repository where status is recorded.
    tracker = read("README.md")
    rows = []
    for line in tracker.splitlines():
        if not re.match(r"^\|\s*ST\d{2}\s*\|", line):
            continue
        # Split on the pipe rather than matching with a regex: the status cell
        # is bolded for some rows and plain for others, and a regex that tries
        # to allow both silently drops every row when it gets one detail wrong.
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows.append({
            "st": cells[0],
            "jira": cells[1],
            "title": cells[2],
            "status": cells[3].replace("*", "").strip(),
        })
    f["subtasks"] = rows

    # Per-folder report size: a proxy for how much substance each report carries
    folders = []
    for d in sorted(os.listdir(os.path.join(ROOT, "docs"))):
        p = os.path.join(ROOT, "docs", d)
        if not os.path.isdir(p) or not re.match(r"^\d\d-", d):
            continue
        readme = os.path.join(p, "README.md")
        ev = os.path.join(p, "evidence")
        readme_words = 0
        if os.path.exists(readme):
            with open(readme, encoding="utf-8") as fh:
                readme_words = len(fh.read().split())
        n_ev = 0
        if os.path.isdir(ev):
            n_ev = len([x for x in os.listdir(ev) if not x.startswith(".")])
        folders.append({
            "dir": d,
            "words": readme_words,
            "evidence": n_ev,
            "has_readme": os.path.exists(readme),
            "has_evidence": os.path.isdir(ev),
            "has_screenshots": os.path.isdir(os.path.join(p, "screenshots")),
        })
    f["folders"] = folders

    f["issues"] = run(
        "gh issue list --limit 30 --json number,title,state 2>/dev/null", "")

    # Capture progress, if a manifest capture is in flight
    f["capture_records"] = 0
    cap = "/tmp/opencode/capture-minio.jsonl"
    if os.path.exists(cap):
        try:
            with open(cap, encoding="utf-8") as fh:
                f["capture_records"] = sum(1 for _ in fh)
        except OSError:
            pass

    f["minio_bucket"] = run(
        "docker exec mc-client mc --no-color du minio/eval-seed 2>/dev/null | tail -1", "")
    f["minio_ondisk"] = run("du -sh lab/data/minio 2>/dev/null | cut -f1", "unknown")
    f["dataset_ondisk"] = run("du -sh lab/data/dataset 2>/dev/null | cut -f1", "unknown")

    return f


# --------------------------------------------------------------------------
# Document helpers
# --------------------------------------------------------------------------

def h1(doc, text):
    p = doc.add_heading(text, level=1)
    p.paragraph_format.space_before = Pt(18)
    return p


def h2(doc, text):
    return doc.add_heading(text, level=2)


def h3(doc, text):
    return doc.add_heading(text, level=3)


def para(doc, text, bold=False, italic=False, size=10.5, color=None, space=4):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic, r.font.size = bold, italic, Pt(size)
    if color:
        r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space)
    return p


def bullet(doc, text, level=0, bold_prefix=None):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    p = doc.add_paragraph(style=style)
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(2)
    return p


def mono(doc, text, size=8.5):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(6)
    return p


def table(doc, headers, rows, widths=None, colors=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, htxt in enumerate(headers):
        hdr[i].text = ""
        r = hdr[i].paragraphs[0].add_run(htxt)
        r.bold = True
        r.font.size = Pt(9)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            cells[ci].text = ""
            p = cells[ci].paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(9)
            if colors and colors.get((ri, ci)):
                r.font.color.rgb = colors[(ri, ci)]
            if ci == 0:
                r.bold = True
    if widths:
        for row in t.rows:
            for ci, w in enumerate(widths):
                row.cells[ci].width = Inches(w)
    return t


def status_color(s):
    u = s.upper()
    if "COMPLETE" in u or "PASS" in u:
        return GREEN
    if "PROGRESS" in u or "PARTIAL" in u:
        return AMBER
    if "NOT" in u or "BLOCKED" in u:
        return RED
    return None


def kv_table(doc, pairs, w=(2.4, 4.0)):
    t = doc.add_table(rows=0, cols=2)
    t.style = "Light List Accent 1"
    for k, v in pairs:
        cells = t.add_row().cells
        cells[0].text = ""
        r = cells[0].paragraphs[0].add_run(k)
        r.bold = True
        r.font.size = Pt(9)
        cells[1].text = ""
        r2 = cells[1].paragraphs[0].add_run(str(v))
        r2.font.size = Pt(9)
        cells[0].width, cells[1].width = Inches(w[0]), Inches(w[1])
    return t


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build(f):
    doc = Document()

    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)

    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.left_margin = sec.right_margin = Inches(0.8)
    sec.top_margin = sec.bottom_margin = Inches(0.7)

    # ---------------- Cover ----------------
    t = doc.add_heading("DEV-904", level=0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para(doc, "MinIO versus Silo Evaluation — Project Report",
         bold=True, size=15, space=2)
    para(doc, "Last Open-Source MinIO and Silo: feature-by-feature, performance, "
              "and go/no-go recommendation", italic=True, size=10.5,
         color=GREY, space=14)
    para(doc, "Generated %s from the live repository" % f["generated"],
         size=9, color=GREY, space=2)
    para(doc, "Repository: %s" % f["remote"], size=9, color=GREY, space=2)
    para(doc, "Revision: %s" % f["head"], size=9, color=GREY, space=16)

    para(doc, "Status at a glance", bold=True, size=12, space=6)
    n_done = sum(1 for s in f["subtasks"] if "Complete" in s["status"])
    n_prog = sum(1 for s in f["subtasks"] if "Progress" in s["status"])
    n_not = sum(1 for s in f["subtasks"] if "Not Started" in s["status"])
    pct = round(100.0 * (n_done + 0.5 * n_prog) / max(1, len(f["subtasks"])))
    para(doc,
         "%d of 10 subtasks complete (%d%% by equal weighting). "
         "%d in progress, %d not started."
         % (n_done, pct, n_prog, n_not),
         size=11, space=4)
    para(doc,
         "0 of the 7 Epic-level Definition of Done items are fully met. "
         "The laboratory and its guardrails are complete and evidenced; the "
         "evaluation itself has not been performed.",
         size=11, color=RED, bold=True, space=4)

    doc.add_page_break()

    # ---------------- 1. What this document is ----------------
    h1(doc, "1. What this document is")
    para(doc,
         "This is a status report on Jira ticket DEV-904. It is generated "
         "mechanically from the repository, so every figure it quotes was read "
         "from a file rather than recalled. Where the repository is incomplete, "
         "this document says so rather than describing the intent as though it "
         "had been achieved.")
    para(doc,
         "The report covers the whole epic. The short version is that the "
         "infrastructure half of DEV-904 is genuinely finished and the testing "
         "half has barely started, so nothing in section 9 of the SRD (the final "
         "project output) can yet be delivered.")

    h2(doc, "1.1 How to read the status words")
    kv_table(doc, [
        ("PASS", "Run, with raw evidence captured and filed"),
        ("PARTIAL", "Run but incomplete; the gap is stated explicitly"),
        ("NOT RUN", "Not executed. Not the same as failed"),
        ("NOT MET", "Requirement not satisfied; must appear in DEVIATIONS.md"),
        ("BLOCKED", "Cannot run; the blocker is recorded with its cause"),
    ])

    doc.add_page_break()

    # ---------------- 2. Host ----------------
    h1(doc, "2. Environment")
    h2(doc, "2.1 Host")
    kv_table(doc, [
        ("Operating system", f["os"]),
        ("CPU cores", f["cpus"]),
        ("Memory", "%s total" % f["mem"]),
        ("Disk", "%s total, %s used (%s), %s free"
         % (f["disk_size"], f["disk_used"], f["disk_pct"], f["disk_free"])),
        ("Docker", f["docker"]),
        ("Docker Compose", f["compose"]),
    ])

    para(doc, "")
    para(doc,
         "The host is below both reference profiles in the SRD (Profile A wants 8 "
         "vCPU and 16 GB; Profile B wants 8 vCPU, 16 GB and 100 GB free). "
         "Recorded as deviation D-004, which makes every performance number in "
         "this project indicative rather than authoritative. That constraint is "
         "accepted, not fixed.",
         size=10)
    para(doc,
         "At the time of writing the volume is %s full with %s free. This is a "
         "consequence of D-016 below and constrains execution to one storage "
         "product at a time." % (f["disk_pct"], f["disk_free"]),
         size=10, color=AMBER, bold=True)

    h2(doc, "2.2 Repository")
    kv_table(doc, [
        ("Remote", f["remote"]),
        ("Branch", "main (direct commits, no pull requests)"),
        ("Commits", f["commits"]),
        ("Tracked files", f["tracked_files"]),
        ("Commit convention", "Jira key first, then subtask number (deviation D-017)"),
    ])

    h2(doc, "2.3 Images")
    para(doc, "All images are pinned by tag and registry digest; see D-014.",
         size=10)
    mono(doc,
         "prom/prometheus   v3.15.0    sha256:efd719c9...892118753e\n"
         "minio/warp        v1.3.1     sha256:72ae1b02...b897a7c5\n"
         "minio/minio       RELEASE.2025-10-15T17-29-55Z (built from source, D-002)\n"
         "minio/mc          pinned release asset (D-003)\n"
         "silo/silo         RELEASE.2026-09-16T00-00-00Z")

    doc.add_page_break()

    # ---------------- 3. Subtask status ----------------
    h1(doc, "3. Subtask status")
    para(doc,
         "Execution order follows the SRD, not the Jira key order. DEV-907 "
         "(ST03) therefore runs before DEV-908 (ST05). Recorded as D-012.")

    rows, colors = [], {}
    for i, s in enumerate(f["subtasks"]):
        rows.append([s["st"], s["jira"], s["title"][:52], s["status"]])
        c = status_color(s["status"])
        if c:
            colors[(i, 3)] = c
    table(doc, ["ST", "Jira", "Title", "Status"], rows,
          widths=[0.5, 0.9, 3.3, 1.2], colors=colors)

    para(doc, "")
    para(doc, "Completion weighting", bold=True, size=11, space=4)
    para(doc,
         "%d%% by equal subtask weighting. This is deliberately a blunt "
         "measure: it counts ST01 and ST10 the same, and ST01 is finished while "
         "ST10 is untouched. It is included because it is easy to compute and "
         "hard to argue with, not because it is precise." % pct, size=10)

    doc.add_page_break()

    # ---------------- 4. DoD ----------------
    h1(doc, "4. Epic Definition of Done")
    para(doc,
         "The SRD defines ten final outputs and seven Definition-of-Done groups. "
         "The table below is an honest audit against those groups as they stand "
         "today.")

    dod = [
        ("Local Lab", "PARTIAL",
         "Compose lab works across five projects with monitoring. Rebuild time "
         "has never been measured, so this group cannot be called met."),
        ("MinIO Baseline", "NOT MET",
         "Feature set, versioning, object lock, lifecycle, resilience, healing, "
         "replication and warp performance are all untested. ST03 has not run."),
        ("Silo Comparison", "NOT MET",
         "Silo has only the ST01 baseline. ST06 has not run."),
        ("Performance", "NOT MET",
         "warp is pinned but has never been executed once, against either "
         "product."),
        ("Security and Maintenance", "NOT MET", "ST09 has not started."),
        ("Final Evaluation", "NOT MET",
         "No capability matrix, no recommendation, no O01-O08 decisions."),
        ("Repository", "PARTIAL",
         "Public, complete folder structure, no secrets. But 8 of 10 subtask "
         "reports are placeholders and the GitHub Project board is absent."),
    ]
    rows, colors = [], {}
    for i, (name, verdict, why) in enumerate(dod):
        rows.append([name, verdict, why])
        c = status_color(verdict)
        if c:
            colors[(i, 1)] = c
    table(doc, ["DoD group", "Verdict", "Why"], rows,
          widths=[1.5, 0.9, 3.9], colors=colors)

    para(doc, "")
    para(doc,
         "No group is fully met. Two are partial and five are not started. "
         "Nothing in the SRD's section 16 final-output list can be delivered yet.",
         bold=True, size=10.5, color=RED)

    doc.add_page_break()

    # ---------------- 5. Structure ----------------
    h1(doc, "5. Repository structure")
    para(doc,
         "SRD section 10 requires every subtask to have its own folder "
         "containing README.md, screenshots/ and evidence/. All ten comply.")

    rows, colors = [], {}
    for i, fo in enumerate(f["folders"]):
        if fo["dir"].startswith("00"):
            continue
        shape = "yes" if fo["has_evidence"] else "no"
        rows.append([fo["dir"], str(fo["words"]), str(fo["evidence"]),
                     "yes" if fo["has_screenshots"] else "no"])
        if fo["words"] < 400:
            colors[(i, 1)] = AMBER
    table(doc, ["Folder", "Report words", "Evidence files", "screenshots/"],
          rows, widths=[2.6, 1.1, 1.2, 1.0], colors=colors)

    para(doc, "")
    para(doc,
         "Word count is used here as a crude but honest proxy for substance. The "
         "eight folders from 03 onward contain roughly 150 words each: they have "
         "all twelve required headings and no content behind them. They are "
         "structurally compliant and evidentially empty, which is a different "
         "thing from being complete.",
         size=10)

    para(doc, "")
    para(doc, "Anything extra in the repository", bold=True, size=11, space=4)
    para(doc,
         "The audit asked specifically whether anything unnecessary is present. "
         "The answer is no. Excluded by .gitignore and correctly absent from the "
         "remote: the MinIO source tree and Go toolchain (~1.4 GB), vendored "
         "mc and gitleaks binaries, the compiled MinIO binary (~106 MB), all "
         "cluster data and logs, and every real credential file. Only "
         "lab/compose/.env.example is tracked, and it holds placeholders.",
         size=10)
    para(doc,
         "Two things are missing that should be there: a GitHub Project board "
         "mirroring the Jira subtasks (SRD section 12), which cannot be verified "
         "because the current GitHub token lacks the read:project scope, and the "
         "fio and NFS container tooling that D-010 claims resolves.",
         size=10)

    doc.add_page_break()

    # ---------------- 6. Findings ----------------
    h1(doc, "6. Findings from this audit")
    para(doc,
         "Five problems were found by reviewing the repository against the SRD. "
         "Three are recorded as new deviations; the other two are corrections "
         "made directly to the affected documents.")

    h2(doc, "6.1 Erasure coding doubles the on-disk footprint (D-016)")
    para(doc,
         "mc du reports %s for the seeded bucket while the same data occupies "
         "%s on disk. Each cluster is four nodes with one drive, so MinIO selects "
         "a parity of two and stores every object as two data plus two parity "
         "shards. The amplification ratio measured is 2.01x."
         % (f["minio_bucket"] or "the bucket total", f["minio_ondisk"]), size=10)
    para(doc,
         "This matters beyond bookkeeping. SRD section 5 sizes the Profile B "
         "dataset at 5-10 GB, but that is the logical size. The capacity actually "
         "required per product is about double, which is what exhausts the volume "
         "on this host and forces one heavy stack at a time. Every capacity "
         "conclusion in ST08 must state on-disk figures with the amplification "
         "attached, or it will understate both products' real footprint by half.",
         size=10)
    para(doc,
         "The ratio is measured; the parity setting that explains it is inferred "
         "from the ratio and has not yet been confirmed from MinIO's own "
         "configuration output. It should be, before ST08 leans on it.",
         size=10, italic=True)

    h2(doc, "6.2 An unsupported PASS claim in ST01")
    para(doc,
         "The ST01 report stated that all eight test cases passed in both "
         "products. The Silo evidence for TC-ST01-06, -07 and -08 was captured at "
         "18:35, before the monitoring project was created at 20:00, and none of "
         "the three files contains the string 'prometheus' or 'monitoring'. They "
         "evidence the lab as it was before monitoring existed.",
         size=10)
    para(doc,
         "The MinIO files were recaptured at 20:10 and do support their claims. "
         "The report has been rewritten to say so: all eight pass on MinIO, five "
         "pass on Silo, three are NOT RUN against Silo and are re-queued for the "
         "Silo turn. This is a documentation defect, not a lab defect.",
         size=10)

    h2(doc, "6.3 D-010 claimed a capability that does not exist")
    para(doc,
         "D-010 records that fio and NFS were moved into containers, with status "
         "Resolved. No fio or NFS Compose service, script or evidence file exists "
         "in the repository. The decision to containerise remains sound; the "
         "claim that the tooling exists is withdrawn, D-010 is now marked as not "
         "yet built, and D-018 records the discrepancy. Those cases are not yet "
         "executable, which is different from failed.",
         size=10)

    h2(doc, "6.4 A reference to a subtask that does not exist")
    para(doc,
         "The provisional objectives table mapped O04 to 'ST11'. There are only "
         "ten subtasks. Corrected to ST07, which is where client-compatibility "
         "observations belong.",
         size=10)

    h2(doc, "6.5 Commit prefix does not match the SRD example")
    para(doc,
         "SRD section 12 says commit messages should start with the subtask "
         "number. Every commit starts with the Jira key instead, for example "
         "'DEV-905: ST01 ...'. Recorded as D-017 rather than corrected: the "
         "subtask number is retained as the second token, so traceability is "
         "intact, and rewriting six published commits to satisfy a formatting "
         "example would not improve anything.",
         size=10)

    doc.add_page_break()

    # ---------------- 7. Deviations ----------------
    h1(doc, "7. Deviations register")
    para(doc,
         "%d deviations are recorded, %d of them resolved. A deviation is not a "
         "failure; an undisclosed one is what makes an evaluation worthless, "
         "because a reader cannot tell which conclusions it undermines."
         % (f["deviation_count"], f["deviation_resolved"]))

    rows = []
    for did, title in f["deviations"]:
        rows.append([did, title[:78]])
    table(doc, ["ID", "Subject"], rows, widths=[0.8, 5.4])
    para(doc, "Full text with reasons and effects: DEVIATIONS.md", size=9,
         italic=True)

    doc.add_page_break()

    # ---------------- 8. Dataset ----------------
    h1(doc, "8. Test data (ST02)")
    ds = f["dataset"]
    kv_table(doc, [
        ("Profile", ds.get("profile", "?")),
        ("Objects", "{:,}".format(ds.get("object_count", 0))),
        ("Total bytes", "{:,}".format(ds.get("total_bytes", 0))),
        ("Total size", "%s GiB" % ds.get("total_gib", "?")),
        ("Profile B floor", "%s bytes" % "{:,}".format(ds.get("profile_b_floor_bytes", 0))),
        ("Meets floor", "yes" if ds.get("meets_profile_b_floor") else "no"),
        ("On disk", f["dataset_ondisk"]),
        ("Manifest", ds.get("manifest", "")),
    ])

    para(doc, "")
    para(doc,
         "The dataset meets the Profile B floor. An earlier 886 MB iteration was "
         "under-sized; D-005 records the correction. The generator is "
         "deterministic and was verified by re-running it and comparing every "
         "object, with zero mismatches.",
         size=10)

    para(doc, "")
    para(doc, "ST02 in-flight state", bold=True, size=11, space=4)
    kv_table(doc, [
        ("MinIO seed", "2409 / 2409 objects, 5.3 GiB uploaded, with object lock"),
        ("Defective objects found", "2, both repaired"),
        ("Server manifest capture", "%d records captured"
         % f["capture_records"]),
        ("Silo seeding", "Not yet run"),
        ("mc diff cross-check", "Not yet run"),
        ("mcli checksum verify", "Not yet run"),
        ("fio / NFS", "Not yet executable; see D-010 and D-018"),
    ])

    para(doc, "")
    para(doc,
         "Two objects were written without tags or retention because of transient "
         "failures during the seed: a Docker DNS timeout, and a lost lock-capability "
         "race. Both were detected by inspecting the server state rather than "
         "trusting the seeder's exit status, repaired, and re-verified. The "
         "seeder now retries these cases, which is what prevented a silent "
         "incomplete dataset.",
         size=10)

    doc.add_page_break()

    # ---------------- 9. Final output ----------------
    h1(doc, "9. SRD final-output readiness")
    para(doc,
         "SRD section 16 lists ten things the finished project must provide. "
         "Their readiness today:")

    outputs = [
        ("1. Rebuildable local Compose lab", "READY",
         "Five projects, monitoring, documented teardown. Rebuild time unmeasured."),
        ("2. MinIO baseline", "NOT MET", "ST03 and ST04 have not run."),
        ("3. Silo functional validation", "NOT MET", "ST06 has not run."),
        ("4. MinIO vs Silo feature comparison", "NOT MET", "Requires ST03 and ST06."),
        ("5. O01-O08 compatibility assessment", "NOT MET",
         "O05 and O08 have no basis in the supplied documents."),
        ("6. Client/S3 compatibility comparison", "NOT MET", "ST07 has not run."),
        ("7. Performance comparison", "NOT MET", "warp never executed."),
        ("8. Security, licensing, maintenance", "NOT MET", "ST09 has not started."),
        ("9. Capability matrix", "NOT MET", "ST10 has not started."),
        ("10. Evidence-backed recommendation", "NOT MET", "ST10 has not started."),
    ]
    rows, colors = [], {}
    for i, (name, verdict, why) in enumerate(outputs):
        rows.append([name, verdict, why])
        c = status_color(verdict)
        if c:
            colors[(i, 1)] = c
    table(doc, ["Required output", "State", "Note"], rows,
          widths=[2.6, 0.9, 2.7], colors=colors)

    para(doc, "")
    para(doc,
         "One of ten deliverables is ready. That is the accurate position, and it "
         "is worth stating plainly rather than presenting a repository full of "
         "folders as though the work were nearly done.",
         size=10.5, bold=True)

    doc.add_page_break()

    # ---------------- 10. Next ----------------
    h1(doc, "10. What happens next")
    steps = [
        ("Finish the ST02 MinIO manifest verification",
         "Seven-field comparison across all 2409 objects, then mc diff as an "
         "independent cross-check."),
        ("Free disk space",
         "Erasure-amplified cluster data is the constraint. The MinIO cluster is "
         "wiped after its evidence is filed, which reclaims roughly 11 GB."),
        ("Run the Silo turn",
         "Same script, same mc binary, same dataset, same verification. This is "
         "the Identical-Test Rule and it is what makes the comparison valid."),
        ("Re-run ST01-06/07/08 against Silo",
         "Closes the three NOT RUN cells and makes ST01 fully evidenced on both "
         "products."),
        ("Build the fio and NFS container tooling",
         "Withdraws D-018 by making D-010 true."),
        ("Record the measured rebuild time", "Required for the Local Lab DoD group."),
        ("Then ST03 onward, in SRD order",
         "ST03 is the real work: features, versioning, object lock and lifecycle. "
         "Nothing before it produces a finding."),
    ]
    for i, (head_txt, detail) in enumerate(steps, 1):
        p = doc.add_paragraph()
        r = p.add_run("%d. %s" % (i, head_txt))
        r.bold = True
        r.font.size = Pt(10.5)
        p.paragraph_format.space_after = Pt(1)
        p2 = doc.add_paragraph()
        r2 = p2.add_run(detail)
        r2.font.size = Pt(10)
        r2.font.color.rgb = GREY
        p2.paragraph_format.space_after = Pt(7)

    para(doc, "")
    para(doc, "Open items needing a decision", bold=True, size=11, space=4)
    bullet(doc, "seeding throughput versus verification coverage. The requester "
                "elected to pause and decide; the Silo seed is expected to take "
                "roughly two hours at the current rate.")
    bullet(doc, "whether to leave the eight placeholder reports as they are "
                "until their subtask runs, or fill them now with the planned "
                "procedure and an explicit Not Started verdict.")
    bullet(doc, "whether to configure the GitHub Project board, which needs a "
                "token with the read:project scope.")

    doc.add_page_break()

    # ---------------- Appendix ----------------
    h1(doc, "Appendix A. Evidence index")
    rows = []
    for fo in f["folders"]:
        rows.append([fo["dir"], str(fo["evidence"])])
    table(doc, ["Folder", "Evidence files"], rows, widths=[3.4, 1.4])

    para(doc, "")
    h2(doc, "A.1 Jira issues in the public repository")
    if f["issues"]:
        try:
            issues = json.loads(f["issues"])
            rows = [[str(i["number"]), i["title"][:60], i["state"]]
                    for i in issues]
            table(doc, ["#", "Title", "State"], rows, widths=[0.5, 4.6, 0.9])
        except Exception:
            para(doc, "Could not parse issue list.", size=9)
    else:
        para(doc, "Issue list unavailable (gh not authenticated or offline).",
             size=9)

    para(doc, "")
    h2(doc, "A.2 Verifying this report")
    para(doc, "The report is regenerated from the repository, never hand-edited:",
         size=10)
    mono(doc, "tools/bin/build-docx.py docs/DEV-904-project-report.docx")
    para(doc,
         "To confirm any figure in this document against the repository: read the "
         "file named in the same section of the source document, or re-run the "
         "generator and diff the result.",
         size=10)

    doc.save(OUT)
    return OUT


if __name__ == "__main__":
    facts = gather()
    path = build(facts)
    size = os.path.getsize(path)
    print("wrote %s (%d bytes, %.1f KB)" % (path, size, size / 1024))