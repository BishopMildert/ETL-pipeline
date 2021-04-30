import src.db.core as db_core
import psycopg2 as pg

def test_query():
    def mock_data():
        return 