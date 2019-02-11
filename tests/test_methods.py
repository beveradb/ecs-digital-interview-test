import pytest

import run_migrations as r


def test_extract_sequence_sql_filename_expected(sql_filename_expected):
    version = r.extract_sequence_num(sql_filename_expected)
    assert version == 45


def test_extract_sequence_sql_filename_hyphen(sql_filename_hyphen):
    version = r.extract_sequence_num(sql_filename_hyphen)
    assert version == 45


def test_extract_sequence_sql_filename_not_zero_padded(
        sql_filename_not_zero_padded):
    version = r.extract_sequence_num(sql_filename_not_zero_padded)
    assert version == 45


def test_extract_sequence_sql_filename_spaced(sql_filename_spaced):
    version = r.extract_sequence_num(sql_filename_spaced)
    assert version == 45


def test_extract_sequence_sql_filename_no_sql_suffix(
        sql_filename_no_sql_suffix):
    version = r.extract_sequence_num(sql_filename_no_sql_suffix)
    assert version == 45


def test_extract_sequence_sql_filename_no_separator(
        sql_filename_no_separator):
    version = r.extract_sequence_num(sql_filename_no_separator)
    assert version == 45


def test_extract_sequence_sql_filename_bigint(
        sql_filename_bigint):
    version = r.extract_sequence_num(sql_filename_bigint)
    assert version == 23514352834592347502351435283459234750


def test_extract_sequence_sql_filename_no_version(
        sql_filename_no_version):
    with pytest.raises(AttributeError):
        r.extract_sequence_num(sql_filename_no_version)


def test_append_migration_sql_filename_expected(sql_filename_expected):
    migrations = []
    r.append_migration(migrations, sql_filename_expected)
    assert migrations == [(45, sql_filename_expected)]


def test_append_migration_sql_filename_expected_existing_value(
        sql_filename_expected):
    migrations = [(2, "test.sql")]
    r.append_migration(migrations, sql_filename_expected)
    assert migrations == [(2, "test.sql"),
                          (45, sql_filename_expected)]


def test_find_migrations_in_directory_expected(tmpdir, sql_filename_expected):
    filepath = tmpdir.join(sql_filename_expected)
    filepath.write("test")
    migrations = r.find_migrations_in_directory(str(tmpdir))
    assert migrations == [(45, str(filepath))]
