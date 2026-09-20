import json
from pathlib import Path


JOB_DIR = Path("data/jobs")
JOB_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def load_job(video_id):

    file = JOB_DIR / f"{video_id}.json"

    if not file.exists():

        return {
            "video_id": video_id
        }

    return json.loads(
        file.read_text(
            encoding="utf-8"
        )
    )


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