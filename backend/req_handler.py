from req_models import CapsuleRequest, RegisterRequest
from flask import Request, jsonify
from http import HTTPStatus
from typing import Tuple
from werkzeug.utils import secure_filename
import os


def register_request(request: Request) -> Tuple[str, HTTPStatus]:
    if not request.is_json:
        return jsonify({"success": False, "msg": "Must send json"}), HTTPStatus.BAD_REQUEST

    data: dict = request.get_json()
    if not RegisterRequest.is_valid(data):
        return jsonify({"success": False, "msg": "Invalid register data"}), HTTPStatus.BAD_REQUEST

    reg_req = RegisterRequest(data)
    nonce, ok = reg_req.insert()
    if not ok:
        return jsonify({"success": False, "msg": "DB insert failed"}), HTTPStatus.BAD_REQUEST

    return jsonify({"success": True, "nonce": nonce}), HTTPStatus.OK


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'lua'


def capsule_request(request: Request) -> Tuple[str, HTTPStatus]:
    is_lua_uploaded = False
    filename = None
    for name_field, file in request.files.items():
        if file.filename == '' or not allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads/', filename))
        is_lua_uploaded = True
        break

    if not is_lua_uploaded:
        return jsonify({"success": False, "msg": "No lua file"}), HTTPStatus.BAD_REQUEST

    data = request.form.to_dict()
    if not CapsuleRequest.is_valid(data):
        return jsonify({"success": False, "msg": "Invalid form data"}), HTTPStatus.BAD_REQUEST

    print('filename is:', filename)
    cap_req = CapsuleRequest(request.form, filename)
    capsule_filename, ok = cap_req.insert()
    if not ok:
        return jsonify({"success": False, "msg": "DB insert failed"}), HTTPStatus.BAD_REQUEST

    capsule_url = request.url + capsule_filename  # TODO: fix to generate proper url
    return jsonify({"success": True, "url": capsule_url})