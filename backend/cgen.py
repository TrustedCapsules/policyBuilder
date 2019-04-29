import datetime
import os

from flask import current_app


# see https://github.com/TrustedCapsules/optee_app/tree/master/capsule_gen/cmd to build the binary

# generates the upload file
# returns True on success, False on failure
def execute_cgen(lua_file_name: str, output_dir: str) -> bool:
    """
    cgen <op> -n <capsule name> [-p path] [-o outpath] [-s SECTION]
      encode   encode plaintext policy, data, log, kvstore into capsule
            -n      capsule name
            -u      capsule uuid [Default: ffffffffffffffffffffffffffffffff]
            -p      path, default local
            -o      output path, default local
      decode        decode capsule into plaintext policy, data, log, kvstore
            -n      capsule name
            -p      path, default local
            -s      section to decode
    """
    with current_app.app_context():
        cgen_path = current_app.config['CGEN_PATH']
        upload_path = current_app.config['UPLOAD_PATH']
        current_time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        ret_val = os.system(
            f"{cgen_path}/cgen encode -n {lua_file_name} -p {upload_path} -o {output_dir}/capsule_{current_time}")
        return ret_val is 0
