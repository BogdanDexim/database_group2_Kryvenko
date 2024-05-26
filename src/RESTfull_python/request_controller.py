from flask import request, jsonify
from request_model import Request
from app_init import app

request1 = Request()

@app.route("/request", methods=['GET'])
def get_all_request():
    return jsonify(request1.get_all_request())


@app.route("/request/<request_id>", methods=['GET'])
def get_request_by_id(request_id):
    return jsonify(request1.get_request_by_id(request_id))


@app.route("/request/add", methods=['POST'])
def add_request():
    url_params = request.args.to_dict()
    return jsonify(request1.add_request(url_params))


@app.route("/request/delete/<request_id>", methods=['DELETE'])
def delete_request(request_id):
    return jsonify(request1.delete_request(request_id))


@app.route("/request/edit/<request_id>", methods=['PUT'])
def edit_request(request_id):
    url_params = request.args.to_dict()
    return jsonify(request1.edit_request(request_id, url_params))