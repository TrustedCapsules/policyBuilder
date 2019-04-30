import os
import subprocess
from typing import Tuple

from flask import current_app


# see https://github.com/TrustedCapsules/optee_app/tree/master/capsule_gen/cmd to build the binary

# generates the upload file
# returns the generated filename, True on success, False on failure
def execute_cgen(capsule_name: str, uuid: str) -> Tuple[str, bool]:
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
            -s      section to decode [Default: all] [Options: header, policy, kvstore, log, data]
    """
    with current_app.app_context():
        cgen_bin = os.path.join(current_app.config['CGEN_PATH'], 'cgen')
        work_dir = os.path.join(current_app.config['CAPSULE_TEMP_WORK_PATH'], capsule_name)
        output_path = current_app.config['GENERATED_CAPSULES_PATH']
        cmd = f"{cgen_bin} encode -n {capsule_name} -p {work_dir}/ -o {output_path}/ -u {uuid}"
        ret_val = subprocess.run(cmd, shell=True).returncode
        return capsule_name + '.capsule', (ret_val is 0)


# returns the hex uuid
def get_capsule_uuid(capsule_file_name: str) -> str:
    # for offsets, see https://github.com/TrustedCapsules/optee_app/blob/master/common/capsuleCommon.h
    with open(os.path.join(current_app.config['GENERATED_CAPSULES_PATH'], capsule_file_name), 'rb') as r:
        uuid = r.read()[11:43]
        return uuid.decode('ascii')
