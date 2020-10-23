def test_ydl_get_entries(entries):
    if not entries:
        raise AssertionError()

    if len(entries) != 2:
        raise AssertionError()
