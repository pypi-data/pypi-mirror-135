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
import smtplib
from email.mime.text import MIMEText

from xmlhelpy import Integer
from xmlhelpy import option

from .main import misc


@misc.command(
    description="Send an e-mail using a SMTP server and the corresponding login data."
)
@option("smtp_server", char="s", description="URL of the SMTP server.", required=True)
@option(
    "smtp_port",
    char="o",
    description="Port of the SMTP server.",
    default=587,
    param_type=Integer,
)
@option(
    "from",
    var_name="from_address",
    char="f",
    description="Mail address where the e-mail will be send from. This is used as the"
    "username of the SMTP server.",
    required=True,
)
@option(
    "password",
    var_name="user_password",
    char="p",
    description="Password of the SMTP server account.",
    required=True,
)
@option(
    "to",
    var_name="to_address",
    char="t",
    description="Address of the recipient.",
    required=True,
)
@option("subject", char="i", description="Specify a subject for the e-mail.")
@option("message", char="m", description="Specify a body for the e-mail.", default="")
def send_mail(
    smtp_server, smtp_port, user_password, from_address, to_address, subject, message
):
    """Send an e-mail using a SMTP server and the corresponding login data"""
    msg = MIMEText(message)

    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()

        server.login(user=from_address, password=user_password)
        server.send_message(msg)
