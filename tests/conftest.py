import pytest


@pytest.fixture
def sql_filename_expected():
    return "045.createtable.sql"


@pytest.fixture
def sql_filename_hyphen():
    return "045-createtable.sql"


@pytest.fixture
def sql_filename_not_zero_padded():
    return "45.createtable.sql"


@pytest.fixture
def sql_filename_spaced():
    return "45 .createtable.sql"


@pytest.fixture
def sql_filename_no_sql_suffix():
    return "45.createtable.jpg"


@pytest.fixture
def sql_filename_no_separator():
    return "45createtable.sql"


@pytest.fixture
def sql_filename_bigint():
    return "23514352834592347502351435283459234750.createtable.sql"


@pytest.fixture
def sql_filename_no_version():
    return "createtable.sql"
