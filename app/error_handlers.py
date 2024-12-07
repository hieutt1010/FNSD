from flask import jsonify

def not_found_error(error):
    return jsonify({"message": "Resource not found"}), 404
