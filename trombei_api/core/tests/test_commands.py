"""
Test custom Django management commands.
"""
from unittest.mock import patch
from unittest import skip

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('trombei_api.core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""
    @skip("skiping")
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    @skip("skiping")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting Error."""
        patched_check.side_effect = [Psycopg2OpError] * 1 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 5)
        patched_check.assert_called_with(databases=['default'])