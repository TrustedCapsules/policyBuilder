import datetime
import os
import random
from http import HTTPStatus
from typing import Tuple

from flask import Request, jsonify, current_app
from werkzeug.datastructures import FileStorage

from req_models import CapsuleRequest, VerifyRequest, RegisterRequest, DecryptRequest


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


def verify_request(request: Request) -> Tuple[str, HTTPStatus]:
    if not request.is_json:
        return jsonify({"success": False, "msg": "Must send json"}), HTTPStatus.BAD_REQUEST

    data: dict = request.get_json()
    if not VerifyRequest.is_valid(data):
        return jsonify({"success": False, "msg": "Invalid register data"}), HTTPStatus.BAD_REQUEST

    verify_req = VerifyRequest(data)
    ok = verify_req.authorize()
    if not ok:
        return jsonify({"success": False, "msg": "DB verify failed"}), HTTPStatus.BAD_REQUEST

    return jsonify({"success": True, "msg": ""}), HTTPStatus.OK


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'lua'


# generates a unique capsule name
# saves the policy and data under the same named folder for cgen
# returns capsule_name for cgen to run on
# see cgen.py for more info
def prep_capsule(policy_file: FileStorage, data_file: FileStorage) -> str:
    # NOTE: KEYSERVER prefix is found in https://github.com/TrustedCapsules/optee_app/blob/master/common/capsuleKeys.h
    # NOTE: Validation in https://github.com/TrustedCapsules/optee_app/blob/master/capsule_gen/cmd/cgen/gen_helper.c
    capsule_name = 'KEYSERVER_' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '__' + hex(
        random.getrandbits(16))
    with current_app.app_context():
        work_dir = current_app.config['CAPSULE_TEMP_WORK_PATH']
        capsule_path = os.path.join(work_dir, capsule_name)
        os.mkdir(capsule_path)
        policy_file.save(os.path.join(capsule_path, capsule_name + '.policy'))
        policy_file.close()
        data_file.save(os.path.join(capsule_path, capsule_name + '.data'))
        data_file.close()
        with open(os.path.join(capsule_path, capsule_name + '.kvstore'), 'w') as file:
            file.write('location: NSS Lab, Vancouver, BC')
            file.close()

        return capsule_name


def capsule_request(request: Request) -> Tuple[str, HTTPStatus]:
    with current_app.app_context():

        if 'policy' not in request.files or \
                'data' not in request.files or \
                not allowed_file(request.files['policy'].filename):
            return jsonify({"success": False, "msg": "Invalid upload"}), HTTPStatus.BAD_REQUEST

        capsule_name = prep_capsule(request.files['policy'], request.files['data'])
        if not capsule_name:
            return jsonify({"success": False, "msg": "No lua file"}), HTTPStatus.BAD_REQUEST

        data = request.form.to_dict()
        if not CapsuleRequest.is_valid(data, capsule_name):
            return jsonify({"success": False, "msg": "Invalid form data"}), HTTPStatus.BAD_REQUEST

        cap_req = CapsuleRequest(request.form, capsule_name)
        capsule_filename, ok = cap_req.insert()
        if not ok:
            return jsonify({"success": False, "msg": "DB insert failed"}), HTTPStatus.BAD_REQUEST

        capsule_url = request.url_root + 'generated_capsules/' + capsule_filename
        return jsonify({"success": True, "url": capsule_url})


def decrypt_request(request: Request) -> Tuple[str, HTTPStatus]:
    if not request.is_json:
        return jsonify({"success": False, "msg": "Must send json"}), HTTPStatus.BAD_REQUEST

    data: dict = request.get_json()
    if not DecryptRequest.is_valid(data):
        return jsonify({"success": False, "msg": "Invalid register data"}), HTTPStatus.BAD_REQUEST

    decrypt_req = DecryptRequest(data)
    key, ok = decrypt_req.get_key()
    if not ok:
        return jsonify({"success": False, "msg": "DB verify failed"}), HTTPStatus.BAD_REQUEST

    return jsonify({"success": True, "key": key}), HTTPStatus.OK
