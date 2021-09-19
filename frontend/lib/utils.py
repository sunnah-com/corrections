from flask import current_app


def api_action_response(success, message):
    return {"success": success, "message": message}


def all_queues():
    return current_app.config["QUEUES"]
