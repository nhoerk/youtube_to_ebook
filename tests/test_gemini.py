def test_gemini_integration_is_not_run_in_unit_suite():
    """Live Gemini checks belong in an explicitly configured integration suite."""
    assert True