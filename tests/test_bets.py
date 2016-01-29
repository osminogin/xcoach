import os
import pytest
import xlrd
from django.core import management
from django.conf import settings

BETTING_FILE = 'BettingPandL.xls'


@pytest.fixture()
def xls_data(request):
    test_dir = os.path.dirname(request.module.__file__)
    xls_file = os.path.join(test_dir, 'fixtures', BETTING_FILE)

    # Go around Excel file
    rows = []
    with xlrd.open_workbook(xls_file) as book:
        sheet = book.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            # Skip table header
            if rownum in [0, 1]:
                continue
            rows.append(sheet.row_values(rownum))
    return rows

# TODO: Many tests


@pytest.mark.django_db
def test_importbets_command(xls_data):
    path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', BETTING_FILE)
    management.call_command('importbets', path)
    assert 0  # For debug

