import random
from math import sqrt
from statistics import median, stdev
from wickedhot.res_sample import update_res_samples, initialize_res_samples


def test_res_sample():

    fields = ['height', 'weight', 'age']
    data_row_1 = {'height': 56.7, 'weight': 34.7, 'age': 72}
    data_row_2 = {'height': 88.0, 'weight': 24.5, 'age': 100}

    data_1 = [data_row_1 for _ in range(200)]
    data_2 = [data_row_2 for _ in range(10)]
    data_stream = (i for i in data_1 + data_2)

    res_samples = initialize_res_samples(fields)
    num_samples = 50

    random_generator = random.Random()
    random_generator.seed(42)

    for row_index, row in enumerate(data_stream):
        for field in fields:
            value = row[field]
            update_res_samples(res_samples, row_index, field, value, num_samples, random_generator)

    medians = {field: median(res_samples[field]) for field in fields}
    assert medians == {'height': 56.7, 'weight': 34.7, 'age': 72.0}

    assert len(res_samples['age']) == 50


def test_res_sample_uniform():
    # shows that it does sample fairly from a uniform distribution
    # even is previously sorted

    num = 10000
    fields = ['foo']
    data_stream = sorted([{'foo': random.random()} for _ in range(num)], key=lambda x: x['foo'])

    res_samples = initialize_res_samples(fields)
    num_samples = 1000

    random_generator = random.Random()
    random_generator.seed(42)

    for row_index, row in enumerate(data_stream):
        value = row['foo']
        update_res_samples(res_samples, row_index, 'foo', value, num_samples, random_generator)

    med = median(res_samples['foo'])
    stand_dev = stdev(res_samples['foo'])

    tol = 0.015

    assert len(res_samples['foo']) == 1000
    assert abs(med-0.5) < tol

    st_dev_expected = 1/sqrt(12)
    assert abs(stand_dev-st_dev_expected) < tol
