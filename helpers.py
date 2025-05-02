from flask_limiter.util import get_remote_address

def validate_phone(phone):
    import phonenumbers
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except:
        return False

def rate_limited(max_per_minute, period=60):
    from flask_limiter import Limiter
    limiter = Limiter(key_func=get_remote_address)
    return limiter.limit(f"{max_per_minute}/{period}seconds")