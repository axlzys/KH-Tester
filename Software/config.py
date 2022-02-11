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

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

DEBUG = True

SCHEDULER_JOBSTORES = {
    'default': SQLAlchemyJobStore(url="mysql+pymysql://root:123456@192.168.0.111:3306/apscheduler?charset=utf8")
}

SCHEDULER_EXECUTORS = {
    'default': {'type': 'threadpool', 'max_workers': 5}
}

SCHEDULER_JOB_DEFAULTS = {
    'coalesce': False,
    'max_instances': 3
}

SCHEDULER_API_ENABLED = True