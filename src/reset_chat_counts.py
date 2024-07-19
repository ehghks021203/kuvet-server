import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config.database import Database

def reset_daily_chat_counts():
    db = Database()
    sql = "UPDATE daily_chat_count SET chat_count=%s"
    db.execute(sql, (0))
    db.commit()
    db.close()

if __name__ == "__main__":
    reset_daily_chat_counts()