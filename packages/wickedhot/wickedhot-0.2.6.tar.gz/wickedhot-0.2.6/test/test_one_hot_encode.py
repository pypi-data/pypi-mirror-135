from wickedhot import one_hot_encode as ohe
from random import Random


def test_get_one_hot_encoder_dicts_from_data_stream_with_ties():
    data = [{'letter': 'a', 'animal': 'dog', 'color': 'red'},
            {'letter': 'a', 'animal': 'dog', 'color': 'red'},
            {'letter': 'a', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'b', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'b', 'animal': 'dog', 'color': 'blue'},
            {'letter': 'b', 'animal': 'cat', 'color': 'green'}]

    stream = (i for i in data)

    categorical_n_levels_dict = {'letter': 1, 'animal': 1, 'color': 2}

    encoders = ohe.get_one_hot_encoder_dicts_from_data_stream(stream, categorical_n_levels_dict)

    expected = {'letter': {'a': 0},
                'animal': {'cat': 0},
                'color': {'blue': 0, 'red': 1}}

    assert encoders == expected


def test_get_key_val_pair_to_index_lookup_simple():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = []
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)

    expected = {('animal', 'cat'): 0,
                ('color', 'blue'): 1,
                ('color', 'red'): 2,
                ('letter', 'a'): 3}

    assert index == expected


def test_get_key_val_pair_to_index_lookup_simple_with_numeric():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = ['blah']
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)

    expected = {'blah': 0,
                ('animal', 'cat'): 1,
                ('color', 'blue'): 2,
                ('color', 'red'): 3,
                ('letter', 'a'): 4}

    assert index == expected


def test_get_line_encoder_and_decoder():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = []
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)
    e, d = ohe.get_line_encoder_and_decoder(index)

    line = {'letter': 'a', 'animal': 'cat', 'color': 'blue'}
    encoded_line = e(line)
    expected = [1.0, 1.0, 0.0, 1.0]

    assert encoded_line == expected

    decoded_line = d(encoded_line)
    assert decoded_line == line


def test_get_line_encoder_and_decoder_with_numerics():
    encoder_dict = {'letter': {'a': 0},
                    'animal': {'cat': 0},
                    'color': {'blue': 0, 'red': 1}}

    non_encoded_keys = ['foo', 'bar']
    index = ohe.get_key_val_pair_to_index_lookup(encoder_dict, non_encoded_keys)
    e, d = ohe.get_line_encoder_and_decoder(index)

    line = {'foo': 88.0, 'letter': 'a', 'animal': 'cat', 'color': 'blue', 'bar': 5.5}
    encoded_line = e(line)
    expected = [5.5, 88.0, 1.0, 1.0, 0.0, 1.0]

    assert encoded_line == expected

    decoded_line = d(encoded_line)
    assert decoded_line == line


def test_get_one_hot_encoder_dicts_from_data_stream():
    data = [{'letter': 'a', 'animal': 'dog', 'color': 'red'},
            {'letter': 'b', 'animal': 'dog', 'color': 'red'},
            {'letter': 'b', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'c', 'animal': 'cat', 'color': 'blue'},
            {'letter': 'a', 'animal': 'dog', 'color': 'blue'},
            {'letter': 'a', 'animal': 'mouse', 'color': 'green'}]

    stream = (i for i in data)

    categorical_n_levels_dict = {'letter': 2, 'animal': 5, 'color': 2}

    encoders = ohe.get_one_hot_encoder_dicts_from_data_stream(stream, categorical_n_levels_dict)

    expected = {'letter': {'a': 0, 'b': 1},
                'animal': {'dog': 0, 'cat': 1, 'mouse': 2},
                'color': {'blue': 0, 'red': 1}}

    assert encoders == expected


def test_get_numeric_stats():
    rand_generator = Random()
    rand_generator.seed(42)

    stream = [{'a': 0.0, 'b': 10.0, 'c': 100.0, 'd': 'foo'},
              {'a': 1.0, 'b': -10.0, 'c': 600.0, 'd': 'foo'},
              {'a': 5.0, 'b': 90.0, 'c': -1000.0, 'd': 'foo'}]

    numeric_stats = ohe.get_numeric_stats(stream, ['a', 'b', 'c'], rand_generator)

    expected = {'a': {'mean': 2.0,
                      'min': 0.0,
                      'max': 5.0,
                      'median': 1.0},
                'b': {'mean': 30.0,
                      'min': -10.0,
                      'max': 90.0,
                      'median': 10.0},
                'c': {'mean': -100.0,
                      'min': -1000,
                      'max': 600.0,
                      'median': 100.0}}

    assert numeric_stats == expected


def test_get_numeric_stats_with_strings():
    rand_generator = Random()
    rand_generator.seed(42)

    stream = [{'a': '0.0', 'b': '10.0', 'c': 100.0, 'd': 'foo'},
              {'a': 1.0, 'b': -10.0, 'c': 600.0, 'd': 'foo'},
              {'a': 5.0, 'b': 90.0, 'c': -1000.0, 'd': 'foo'}]

    numeric_stats = ohe.get_numeric_stats(stream, ['a', 'b', 'c'], rand_generator)

    expected = {'a': {'mean': 2.0,
                      'min': 0.0,
                      'max': 5.0,
                      'median': 1.0},
                'b': {'mean': 30.0,
                      'min': -10.0,
                      'max': 90.0,
                      'median': 10.0},
                'c': {'mean': -100.0,
                      'min': -1000,
                      'max': 600.0,
                      'median': 100.0}}

    assert numeric_stats == expected
