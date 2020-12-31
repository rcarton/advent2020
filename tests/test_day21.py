from advent.days.day21 import first, second

EXAMPLE = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".splitlines(
    keepends=True
)


def test_first():
    assert first(EXAMPLE) == 5


def test_second():
    assert second(EXAMPLE) == "mxmxvkd,sqjhc,fvjkl"
