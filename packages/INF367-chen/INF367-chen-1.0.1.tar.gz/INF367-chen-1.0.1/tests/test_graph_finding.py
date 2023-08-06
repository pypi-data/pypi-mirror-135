import pytest


@pytest.mark.parametrize("summand_first,summand_second,expected", [
    (2, 2, 4),
    (2, 3, 5),
    (1, 7, 8),
    (5, 5, 10),
])
def test_all_might_failure(summand_first, summand_second, expected):
    assert summand_first + summand_second == expected
