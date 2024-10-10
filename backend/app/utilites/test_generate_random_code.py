from app.utilites.generate_random_code import generate_numeric_code


def test_generate_random_code():
    codeA = generate_numeric_code(6)
    codeB = generate_numeric_code(6)

    assert codeA != codeB
    assert len(codeA) == 6
    assert len(codeB) == 6

    codeC = generate_numeric_code(12)
    assert len(codeC) == 12
