import pytest
from wickedhot.transform_stream import transform_numeric_string, transform_stream


def test_transform_numeric_string_raises_assertion():
    with pytest.raises(AssertionError):
        transform_numeric_string([4, '6'], -999)


def test_transform_numeric_string():
    default = -555
    assert transform_numeric_string('0', default) == (0, True)
    assert transform_numeric_string('77', default) == (77, True)

    assert transform_numeric_string('77.7', default) == (77.7, True)
    assert transform_numeric_string('-77.7', default) == (-77.7, True)

    assert transform_numeric_string(0, default) == (0, True)
    assert transform_numeric_string(77, default) == (77, True)
    assert transform_numeric_string(77.7, default) == (77.7, True)

    # Booleans
    assert transform_numeric_string(True, default) == (1, True)
    assert transform_numeric_string(False, default) == (0, True)

    # now some that fail

    assert transform_numeric_string('hello', default) == (default, False)


def test_transform_stream():
    stream = [{'color': 'red', 'height': '85.4', 'weight': '145', 'married': True},
              {'color': 'blue', 'height': '15.3', 'weight': '130', 'married': False},
              {'color': 'green', 'height': 22.8, 'weight': 120, 'married': 'blah'},
              {'color': 'yellow', 'height': '100.0', 'weight': 'misssing', 'married': 'True'}]

    numeric_cols = ['height', 'weight', 'married']
    result = list(transform_stream(stream, numeric_cols, default_numeric=-555))

    expected = [{'color': 'red', 'height': 85.4, 'weight': 145, 'married': 1},
                {'color': 'blue', 'height': 15.3, 'weight': 130, 'married': 0},
                {'color': 'green', 'height': 22.8, 'weight': 120, 'married': -555},
                {'color': 'yellow', 'height': 100.0, 'weight': -555, 'married': -555}]

    assert result == expected

    # check that you can capture conversion stats
    failed_stats = {}
    _ = list(transform_stream(stream, numeric_cols, default_numeric=-555, num_failed=failed_stats))
    assert failed_stats == {'married': 2, 'weight': 1}
