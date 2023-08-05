# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import paramiko
from scp import SCPClient
from xmlhelpy import Integer
from xmlhelpy import option

from .main import system


@system.command(description="Copy file using the scp protocol")
@option("hostname", char="h", description="Hostname", required=True)
@option("port", char="P", description="Port", default=22, param_type=Integer)
@option("username", char="u", description="Username")
@option("password", char="p", description="Password")
@option("local", char="t", description="Local path", required=True, default="~")
@option("remote", char="s", description="Remote path", required=True, default="~")
@option("get", char="g", description="get / put", is_flag=True)
@option("recursive", char="r", description="Recursive", is_flag=True)
def scp(hostname, port, username, password, local, remote, get, recursive):
    """Copy file using the scp protocol"""

    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname,
            port=port,
            username=username,
            password=password,
        )

        with SCPClient(client.get_transport()) as _scp:
            if get:
                _scp.get(
                    remote_path=remote,
                    local_path=local,
                    recursive=recursive,
                )
            else:
                _scp.put(
                    local,
                    remote_path=remote,
                    recursive=recursive,
                    preserve_times=False,
                )
