import datetime
import os
from typing import Tuple

from flask import current_app


# see https://github.com/TrustedCapsules/optee_app/tree/master/capsule_gen/cmd to build the binary

# generates the upload file
# returns the generate file name, True on success, False on failure
def execute_cgen(lua_file_name: str) -> Tuple[str, bool]:
    """
    Usage: cgen <op> -n <capsule name> [-p path] [-o outpath] [-s SECTION]

      Expected structure with -n NAME:
      path flag must contain folder NAME
      and contain NAME.kvstore, NAME.data, NAME.policy

      encode        encodes a plaintext policy, data, log, kvstore into capsule
            -n      capsule name [Required]
            -u      capsule uuid [Default: ffffffffffffffffffffffffffffffff]
            -p      path [Default: ./]
            -o      output path [Default: ./]
      decode        decodes capsule into plaintext policy, data, log, kvstore
            -n      capsule name [Required]
            -p      path [Default: ./]
            -s      section to decode [Default: all] [Options: header, policy, kv, log, data]
    """
    with current_app.app_context():
        cgen_path = os.path.join(current_app.config['CGEN_PATH'], 'cgen')
        upload_path = current_app.config['UPLOADED_LUA_PATH']
        output_path = current_app.config['GENERATED_CAPSULES_PATH']
        current_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        out_file_name = 'cap_' + current_time + '.capsule'
        cmd = f"{cgen_path} encode -n {lua_file_name} -p {upload_path}/ -o {output_path}/"
        ret_val = os.system(cmd)
        print("cgen cmd: ", cmd)
        print("cgen retval: ", ret_val)
        return out_file_name, (ret_val is 0)


# returns the hex uuid
def get_capsule_uuid(capsule_file_name: str) -> str:
    # for offsets, see https://github.com/TrustedCapsules/optee_app/blob/master/common/capsuleCommon.h
    with open(os.path.join(current_app.config['GENERATED_CAPSULES_PATH'], capsule_file_name), 'rb') as r:
        uuid = r.read()[12:44]
        return str(uuid)
