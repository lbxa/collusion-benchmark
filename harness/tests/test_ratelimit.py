from veracity_harness.ratelimit import try_acquire


def test_requests_per_model_stay_within_a_sliding_minute_across_callers(tmp_path):
    path = tmp_path / "rate.sqlite"
    # Separate calls stand in for separate processes: all state lives in the file.
    assert [try_acquire(path, "@cf/a", 2, now) for now in (100.0, 101.0)] == [0.0, 0.0]
    # A third start inside the minute waits until the oldest one leaves the window.
    assert try_acquire(path, "@cf/a", 2, 110.0) == 50.0
    # Other models have their own allowance.
    assert try_acquire(path, "@cf/b", 2, 110.0) == 0.0
    assert try_acquire(path, "@cf/a", 2, 160.5) == 0.0
    assert try_acquire(path, "@cf/a", 2, 161.5) == 0.0
    assert try_acquire(path, "@cf/a", 2, 162.0) > 0.0
