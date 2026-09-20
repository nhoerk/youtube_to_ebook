import json
from pathlib import Path
from datetime import datetime, timezone


JOB_DIR = Path("data/jobs")
JOB_DIR.mkdir(
    parents=True,
    exist_ok=True
)

STAGES = (
    "downloaded",
    "cleaned",
    "chunked",
    "summarized",
    "outline",
    "preface",
    "toc",
    "chapters",
    "manuscript",
    "docx",
    "pdf",
)


def _now():
    return datetime.now(timezone.utc).isoformat()


def load_job(video_id):

    file = JOB_DIR / f"{video_id}.json"

    if not file.exists():

        return {
            "video_id": video_id,
            "status": "pending",
            "stages": {},
        }

    job = json.loads(
        file.read_text(
            encoding="utf-8"
        )
    )
    job.setdefault("status", "pending")
    job.setdefault("stages", {})
    for stage in STAGES:
        if job.get(stage) and stage not in job["stages"]:
            job["stages"][stage] = {
                "status": "success",
                "completed_at": None,
            }
    return job


def save_job(job):

    file = (
        JOB_DIR /
        f"{job['video_id']}.json"
    )

    file.write_text(
        json.dumps(
            job,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def is_stage_complete(job, stage):
    return job.get("stages", {}).get(stage, {}).get("status") == "success"


def start_stage(job, stage):
    if stage not in STAGES:
        raise ValueError(f"Unknown job stage: {stage}")

    job.setdefault("stages", {})[stage] = {
        "status": "running",
        "started_at": _now(),
    }
    job["status"] = "running"
    save_job(job)


def complete_stage(job, stage, result=None):
    if stage not in STAGES:
        raise ValueError(f"Unknown job stage: {stage}")

    state = job.setdefault("stages", {}).setdefault(stage, {})
    state.update({
        "status": "success",
        "completed_at": _now(),
    })
    if result is not None:
        state["result"] = str(result)
    job[stage] = True
    job["status"] = "running"
    save_job(job)


def fail_stage(job, stage, error):
    if stage not in STAGES:
        raise ValueError(f"Unknown job stage: {stage}")

    job.setdefault("stages", {})[stage] = {
        "status": "failed",
        "failed_at": _now(),
        "error": str(error),
    }
    job["status"] = "failed"
    save_job(job)