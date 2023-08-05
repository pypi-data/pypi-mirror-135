import pytest

from nexusmaker.tools import remove_combining_cognates

def test_remove_combining_cognates(nexusmaker):
    x = remove_combining_cognates(nexusmaker, keep=1)
    print(x)
    assert False
    
    