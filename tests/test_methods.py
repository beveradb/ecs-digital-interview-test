import pytest

import run_migrations as r


def test_extract_sequence_sql_filename_expected(sql_filename_expected):
    version = r.extract_sequence_num(sql_filename_expected)
    assert version == 10


def test_extract_sequence_sql_filename_hyphen(sql_filename_hyphen):
    version = r.extract_sequence_num(sql_filename_hyphen)
    assert version == 10


def test_extract_sequence_sql_filename_not_zero_padded(
        sql_filename_not_zero_padded):
    version = r.extract_sequence_num(sql_filename_not_zero_padded)
    assert version == 10


def test_extract_sequence_sql_filename_spaced(sql_filename_spaced):
    version = r.extract_sequence_num(sql_filename_spaced)
    assert version == 10


def test_extract_sequence_sql_filename_no_sql_suffix(
        sql_filename_no_sql_suffix):
    version = r.extract_sequence_num(sql_filename_no_sql_suffix)
    assert version == 10


def test_extract_sequence_sql_filename_no_separator(
        sql_filename_no_separator):
    version = r.extract_sequence_num(sql_filename_no_separator)
    assert version == 10


def test_extract_sequence_sql_filename_bigint(
        sql_filename_bigint):
    version = r.extract_sequence_num(sql_filename_bigint)
    assert version == 23514352834592347502351435283459234750


def test_extract_sequence_sql_filename_no_version(
        sql_filename_no_version):
    with pytest.raises(AttributeError):
        r.extract_sequence_num(sql_filename_no_version)


def test_append_migration_to_list_sql_filename_expected(sql_filename_expected):
    migrations = []
    r.append_migration_to_list(migrations, sql_filename_expected)
    assert migrations == [(10, sql_filename_expected)]
