from my_cookbook.util import core


def request():
    return {
        "version": "1.0",
        "session": {
            "application": {
                "applicationId": core.APP_ID
            },
            "sessionId": "default_session_id",
            "new": False
        }
    }
