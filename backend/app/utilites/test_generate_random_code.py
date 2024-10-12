from app.utilites.generate_random_code import generate_numeric_code, generate_string_code


def test_numeric_code():
    code_a = generate_numeric_code(6)
    code_b = generate_numeric_code(6)

    assert code_a != code_b
    assert len(code_a) == 6
    assert len(code_b) == 6

    code_c = generate_numeric_code(12)
    assert len(code_c) == 12


def test_string_code():
    code_a = generate_string_code(6)
    code_b = generate_string_code(6)

    assert code_a != code_b
    assert len(code_a) == 6
    assert len(code_b) == 6

    code_c = generate_string_code(12)
    assert len(code_c) == 12
