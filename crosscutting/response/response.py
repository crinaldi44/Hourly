from flask import jsonify

"""
    Sends a response back to the client in a uniform format. Returns
    data in a uniform format including descriptive status codes and
    a defined message.
"""


def serve_response(message, status, data=[], headers={}):
    response = jsonify({
        "message": message,
        "status": status,
        "data": data
    })
    for i in headers.keys():
        response.headers.set(i, headers[i])
    return response, status
