#                 This software is part of the KH Tester
#                               Version 3.0
#                   Copyright (C) 2022 jiawei wu
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# version 3 along with this program in the file "LICENSE".  If not, see
# <http://www.gnu.org/licenses/agpl-3.0.txt>.

from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "/home/pi/APP/examples/examples/data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "xxx"
db = SQLAlchemy(app)

scheduler = APScheduler()

