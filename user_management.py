import database
from config import POINTS_PER_TAP, TAP_COOLDOWN
import datetime

def register_user(telegram_id, ip_address):
    user = database.get_user(telegram_id)
    if not user:
        database.create_user(telegram_id, None, ip_address)
        return True
    return False

def can_tap(telegram_id):
    user = database.get_user(telegram_id)
    if not user.last_tap:
        return True
    time_since_last_tap = datetime.datetime.utcnow() - user.last_tap
    return time_since_last_tap.total_seconds() >= TAP_COOLDOWN

def tap(telegram_id):
    if can_tap(telegram_id):
        database.update_user_points(telegram_id, POINTS_PER_TAP)
        return True
    return False

def generate_invite_link(telegram_id):
    # Implement invite link generation logic
    return f"https://t.me/Kingi_Coin_Bot?start={telegram_id}"

# Add more user management functions as needed