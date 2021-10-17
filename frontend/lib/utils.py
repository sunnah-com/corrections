from auth import check_queue_permission
from flask import current_app


def api_action_response(success, message):
    return {"success": success, "message": message}


def all_queues(username):
    queues = [name
              for name in current_app.config["QUEUES"]
              if check_queue_permission(username, name)]
    return queues
