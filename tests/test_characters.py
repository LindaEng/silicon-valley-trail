from game.actions import load_characters

def test_load_characters():
    chars = load_characters()
    assert len(chars) > 0
    assert "name" in chars[0]