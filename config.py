TEST_MODE = True


def test_print(*args, **kwargs):
    """Print only in test mode"""
    if TEST_MODE:
        print(*args, **kwargs)

def normal_print(*args, **kwargs):
    """Print only in normal mode"""
    if not TEST_MODE:
        print(*args, **kwargs)