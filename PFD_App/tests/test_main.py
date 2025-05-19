# impertieren von Funktionen aus app/main.py
from app.main import hello
# Testfunktion
def test_hello():
    assert hello() == "Hallo Welt!"
