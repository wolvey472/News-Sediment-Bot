
import pandas as pd
import pytest
from finBERT_cases import TEST_normal, TEST_weird, TEST_smart

df = pd.read_excel(r"C:\Users\carso\Downloads\CS50 Project NEW\test.xlsx")




@pytest.mark.parametrize("text, expected_label", TEST_weird.items())
def test_finbert_labels(text, expected_label):
    from finBERT_model import finBERT

    result = finBERT(text)

    assert result["label"] == expected_label



#       pytest finBERT_test.py
    