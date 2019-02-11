import pytest


@pytest.fixture
def sql_filename_expected():
    return "010.test_name.sql"


@pytest.fixture
def sql_filename_hyphen():
    return "010-test_name.sql"


@pytest.fixture
def sql_filename_not_zero_padded():
    return "10.test_name.sql"


@pytest.fixture
def sql_filename_spaced():
    return "10 .test_name.sql"


@pytest.fixture
def sql_filename_no_sql_suffix():
    return "10.test_name.jpg"


@pytest.fixture
def sql_filename_no_separator():
    return "10test_name.sql"


@pytest.fixture
def sql_filename_bigint():
    return "23514352834592347502351435283459234750.test_name.sql"


@pytest.fixture
def sql_filename_no_version():
    return "test_name.sql"
