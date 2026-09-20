import json

from src.core import job_manager


def test_job_stage_lifecycle_persists_state(tmp_path, monkeypatch):
    monkeypatch.setattr(job_manager, "JOB_DIR", tmp_path)

    job = job_manager.load_job("video-1")
    assert job["status"] == "pending"

    job_manager.start_stage(job, "downloaded")
    assert job["stages"]["downloaded"]["status"] == "running"

    job_manager.complete_stage(job, "downloaded", "data/raw.txt")
    saved = job_manager.load_job("video-1")
    assert saved["status"] == "running"
    assert job_manager.is_stage_complete(saved, "downloaded")
    assert saved["stages"]["downloaded"]["result"] == "data/raw.txt"


def test_failed_stage_is_resumable(tmp_path, monkeypatch):
    monkeypatch.setattr(job_manager, "JOB_DIR", tmp_path)

    job = job_manager.load_job("video-2")
    job_manager.start_stage(job, "cleaned")
    job_manager.fail_stage(job, "cleaned", RuntimeError("transcript missing"))

    saved = job_manager.load_job("video-2")
    assert saved["status"] == "failed"
    assert saved["stages"]["cleaned"]["status"] == "failed"
    assert saved["stages"]["cleaned"]["error"] == "transcript missing"
    assert not job_manager.is_stage_complete(saved, "cleaned")


def test_load_job_migrates_legacy_boolean_stages(tmp_path, monkeypatch):
    monkeypatch.setattr(job_manager, "JOB_DIR", tmp_path)
    (tmp_path / "video-3.json").write_text(
        json.dumps({"video_id": "video-3", "downloaded": True}),
        encoding="utf-8",
    )

    saved = job_manager.load_job("video-3")
    assert saved["stages"]["downloaded"]["status"] == "success"
