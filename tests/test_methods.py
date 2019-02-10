from run_migrations import extract_sequence_num


def test_extract_sequence_num():
    version = extract_sequence_num("010.test_name.sql")
    assert version == 10
