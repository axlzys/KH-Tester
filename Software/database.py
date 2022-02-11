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

from app import db

class testResult(db.Model):
    __tablename__ = "testresult"
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    Time = db.Column(db.String)
    Temp = db.Column(db.Float)
    PHresult = db.Column(db.Float)

class KHResult(db.Model):
    __tablename__ = "KHResult"
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    Time = db.Column(db.String)
    KHresult = db.Column(db.Float)
    ADDKH = db.Column(db.Integer)

class timesleep(db.Model):
    __tablename__ = "timesleep"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

class runtime(db.Model):
    __tablename__ = "runtime"
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    Time = db.Column(db.String)

class SampleV(db.Model):
    __tablename__ = "SampleV"
    id = db.Column(db.Integer, primary_key=True)
    SPV = db.Column(db.Float)

class PharmacyV(db.Model):
    __tablename__ = "PharmacyV"
    id = db.Column(db.Integer, primary_key=True)
    PHV = db.Column(db.Float)

class KHpump(db.Model):
    __tablename__ = "KHpump"
    id = db.Column(db.Integer, primary_key=True)
    KHpumpV = db.Column(db.Float)

class TargKH(db.Model):
    __tablename__ = "TargKH"
    id = db.Column(db.Integer, primary_key=True)
    targetKH = db.Column(db.Float)

db.create_all()