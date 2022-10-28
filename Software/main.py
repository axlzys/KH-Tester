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

import time
from flask import render_template, jsonify,request
from flask_moment import Moment
import datetime
from Tester import tester
from database import db,testResult,KHResult,timesleep,runtime,SampleV,PharmacyV,TargKH,KHpump
from app import app,scheduler


moment = Moment(app)
@app.route('/main')
@app.route('/')
def main():
    return render_template('main.html', time=datetime.datetime.utcnow())

@app.route('/KHhistry')
def KHhistry():
    KHResultlist = KHResult.query.order_by(KHResult.id.desc()).limit(50)
    return render_template('KHhistry.html',KHResultlist= KHResultlist)

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/realtimePH')
def realtimePH():
    users = testResult.query.order_by(testResult.id.desc()).first()
    users= users.PHresult
    return str(users)

def autoreadPH():
    realtimePH = tester().readPH(1)
    PH1 = testResult(Date=datetime.datetime.now().strftime('%Y-%m-%d'),
                     Time=datetime.datetime.now().strftime('%H:%M:%S'), PHresult=realtimePH)
    db.session.add(PH1)
    db.session.commit()
    return str(realtimePH)

@app.route('/dbph')
def PHlist():
    users = testResult.query.order_by(testResult.id.desc()).limit(10)
    users = users[::-1]
    x_data = [i.Time for i in users]
    y_data = [i.PHresult for i in users]

    data = {
        'x_data': x_data,
        'y_data': y_data
    }
    return jsonify(data)

@app.route('/CalibrationPH')
def CalibrationPH1():
    aa = tester().CalibrationPH(1)
    return jsonify(aa)

@app.route('/CalibrationKH')
def CalibrationKH1():
    aa = tester().CalibrationPH(1)
    return jsonify(aa)

@app.route('/realtimeKH')
def realtimeKH():
    users = KHResult.query.order_by(KHResult.id.desc()).first()
    users = users.KHresult
    return jsonify(users)

@app.route('/runkhtest')
def runkhtest():
    Samplev = SampleV.query.order_by(SampleV.id.desc()).first()
    samplev = Samplev.SPV
    pharmacyV = PharmacyV.query.order_by(PharmacyV.id.desc()).first()
    pharmacyV = pharmacyV.PHV
    aciv= pharmacyV/100
    lastkhtime = runtime.query.order_by(runtime.id.desc()).first()
    lastkhtime = lastkhtime.Time
    lastkhdata = runtime.query.order_by(runtime.id.desc()).first()
    lastkhdata = lastkhdata.Date
    lastkh = lastkhdata + lastkhtime
    lastkhdatatime = datetime.datetime.strptime(lastkh, '%Y-%m-%d%H:%M:%S')
    time14 = lastkhdatatime + datetime.timedelta(minutes=15)
    if time14 < datetime.datetime.now():
        runtime1 = runtime(Date=datetime.datetime.now().strftime('%Y-%m-%d'),
                           Time=datetime.datetime.now().strftime('%H:%M:%S'))
        db.session.add(runtime1)
        db.session.commit()
        drops = tester().KHtester()
        if drops != False:
            drops = drops
            VHCL = drops * aciv
            khresult = (VHCL / samplev) * 280
            khresult2 = round(khresult, 1)
            KH1 = KHResult(Date=datetime.datetime.now().strftime('%Y-%m-%d'),
                           Time=datetime.datetime.now().strftime('%H:%M:%S'), KHresult=khresult2)
            db.session.add(KH1)
            db.session.commit()
            tester().drainbot()
            tester().fillbot()
            return jsonify(khresult2)
        else:
            return "反应仓进水超时，请检查进水管，液位开关等。"
    else:
        return jsonify("15分钟内刚进行过测试，请稍后再试")

@app.route('/dbkh')
def KHlist():
    users = KHResult.query.order_by(KHResult.id.desc()).limit(10)
    users = users[::-1]
    x_data = [i.Time for i in users]
    y_data = [i.KHresult for i in users]

    data = {
        'x_data': x_data,
        'y_data': y_data
    }
    return jsonify(data)


@app.route('/test1')
def printTime():

    lastkhtime = KHResult.query.order_by(KHResult.id.desc()).first()
    lastkhtime = lastkhtime.Time
    lastkhdata = KHResult.query.order_by(KHResult.id.desc()).first()
    lastkhdata = lastkhdata.Date
    lastkh = lastkhdata + lastkhtime
    lastkhdatatime = datetime.datetime.strptime(lastkh,'%Y-%m-%d%H:%M:%S')
    time14 = lastkhdatatime + datetime.timedelta(minutes=15)

    if time14 > datetime.datetime.now():

        print(lastkhdatatime)
    #print(time14)
    else:
        print(datetime.datetime.now())

    #print(time14 - now)
    return 'ok'

@app.route('/testpwm1')
def testpwm1():
    time11 = timesleep.query.order_by(timesleep.id.desc()).first()
    time12 = time11.time

    return jsonify(time12)



@app.route('/getjson',methods=['GET','POST'])
def getjson():
    a = request.json
    if a:
        data = a['opt']
        data = int(data)
        TIME = timesleep(time = data)
        db.session.add(TIME)
        db.session.commit()
        time14 = data * 3600
    for job in scheduler.get_jobs():
            scheduler.modify_job(id = 'job2', trigger='interval', seconds=time14)
    return jsonify(data)

@app.route('/CalibrationSPV')
def CalibrationSPV():
    tester().drainbot()
    tester().fillbot()
    return jsonify("反应仓容积校准完成，请拿出反应仓测量容积并输入。")

@app.route('/getSPV',methods=['GET','POST'])
def getSPV():
    b= request.json
    if b:
        data1 = b['opt1']
        data1 = float(data1)
        SPV1 = SampleV(SPV = data1)
        db.session.add(SPV1)
        db.session.commit()
    return jsonify(data1)

@app.route('/readSPV')
def readSPV():
    Samplev = SampleV.query.order_by(SampleV.id.desc()).first()
    Samplev = Samplev.SPV
    return jsonify(Samplev)

@app.route('/CalibrationACIV')
def CalibrationACIV():
    tester().CalibrationACIVcore()
    return jsonify("药水泵流量校准完成，请拿测量容积并输入。")

@app.route('/getACIV',methods=['GET','POST'])
def getACIV():
    c = request.json
    if c:
        data1 = c['opt2']
        data1 = float(data1)
        ACIV1 = PharmacyV(PHV = data1)
        db.session.add(ACIV1)
        db.session.commit()
    return jsonify(data1)

@app.route('/readACIV')
def readACIV():
    pharmacyV = PharmacyV.query.order_by(PharmacyV.id.desc()).first()
    pharmacyV = pharmacyV.PHV
    return jsonify(pharmacyV)

@app.route('/CalibrationKHpump')
def CalibrationKHpump():
    tester().KHpumpon()
    time.sleep(10)
    tester().KHpumpoff()
    return jsonify("滴定泵流量校准完成，请拿测量容积并输入。")

@app.route('/getKHpump',methods=['GET','POST'])
def getKHpump():
    c = request.json
    if c:
        data1 = c['opt3']
        data1 = float(data1)
        KHpump1 = KHpump(KHpumpV = data1)
        db.session.add(KHpump1)
        db.session.commit()
    return jsonify(data1)

@app.route('/readKHpump')
def readKHpump():
    kHpump = KHpump.query.order_by(KHpump.id.desc()).first()
    kHpump = kHpump.KHpumpV
    kHpump= kHpump
    return jsonify(kHpump)

@app.route('/gettar',methods=['GET','POST'])
def gettar():
    c = request.json
    if c:
        data2 = c['opt2']
        data2 = float(data2)
        TargKH1 = TargKH(targetKH = data2)
        db.session.add(TargKH1)
        db.session.commit()
    return jsonify(data2)

@app.route('/readtar')
def readtar():
    targKH = TargKH.query.order_by(TargKH.id.desc()).first()
    targKH = targKH.targetKH
    targKH= targKH
    return jsonify(targKH)

@app.route('/Inpumpon')
def Inpumpon():
    tester().Inpumpon()

@app.route('/Inpumpoff')
def Inpumpoff():
    tester().Inpumpoff()

@app.route('/Outpumpon')
def Outpumpon():
    tester().Outpumpon()

@app.route('/Outpumpoff')
def Outpumpoff():
    tester().Outpumpoff()

@app.route('/KHpumpon')
def KHpumpon():
    tester().KHpumpon()

@app.route('/KHpumpoff')
def KHpumpoff():
    tester().KHpumpoff()

@app.route('/pharmacypumpon')
def pharmacypumpon():
    tester().pharmacypumpon()

@app.route('/pharmacypumpoff')
def pharmacypumpoff():
    tester().pharmacypumpoff()

@app.route('/getkhtime')
def getkhtime():
    time20 = timesleep.query.order_by(timesleep.id.desc()).first()
    time21 = time20.time
    time21 = time21 * 3600
    return time21

@app.route('/autorunkhtest')
def autorun():
    lastkhtime = runtime.query.order_by(runtime.id.desc()).first()
    lastkhtime = lastkhtime.Time
    lastkhdata = runtime.query.order_by(runtime.id.desc()).first()
    lastkhdata = lastkhdata.Date
    lastkh = lastkhdata + lastkhtime
    lastkhdatatime = datetime.datetime.strptime(lastkh, '%Y-%m-%d%H:%M:%S')
    time14 = lastkhdatatime + datetime.timedelta(minutes=10)
    if time14 < datetime.datetime.now():
        runtime1 = runtime(Date=datetime.datetime.now().strftime('%Y-%m-%d'),
                           Time=datetime.datetime.now().strftime('%H:%M:%S'))
        db.session.add(runtime1)
        db.session.commit()
        return autorunkhtest()
    else:
        scheduler.pause_job("job2")
        time.sleep(10)
        scheduler.resume_job("job2")
        return "10分钟内进行过手动测试，自动测试自动延期。"

def autorunkhtest():
    targKH = TargKH.query.order_by(TargKH.id.desc()).first()
    targKH = targKH.targetKH
    tar = targKH
    Samplev = SampleV.query.order_by(SampleV.id.desc()).first()
    samplev = Samplev.SPV
    pharmacyV = PharmacyV.query.order_by(PharmacyV.id.desc()).first()
    pharmacyV = pharmacyV.PHV
    aciv = pharmacyV / 100
    drops = tester().KHtester()
    if drops != False:
        drops = drops
        VHCL = drops * aciv
        khresult = (VHCL/samplev)*280
        khresult2 = round(khresult,1)
        if tar == 0:
            tester().KHpumpon()
        elif tar - khresult2 > 0 and tar - khresult2 <0.5:
            tester().KHpumpoff()
        elif tar - khresult2 >= 0.5 and tar - khresult2 <1:
            tester().KHpumpon()
            time.sleep(3)
            tester().KHpumpoff()
        elif tar - khresult2 >= 1 and tar - khresult2 <2:
            tester().KHpumpon()
            time.sleep(6)
            tester().KHpumpoff(0)
        elif tar - khresult2 >= 2:
            tester().KHpumpon()
            time.sleep(10)
            tester().KHpumpoff(0)
        KH1 = KHResult(Date=datetime.datetime.now().strftime('%Y-%m-%d') ,Time = datetime.datetime.now().strftime('%H:%M:%S'),KHresult = khresult2,ADDKH = 1)
        db.session.add(KH1)
        db.session.commit()
        tester().drainbot()
        tester().fillbot()
        return jsonify(khresult2)
    else:
        return "反应仓进水超时，请检查进水管，液位开关等。"

@app.route('/AutoBalanceKH')
def AutoBalanceKH():
    tester().pharmacypump(1)
    return "OK"

@app.route('/stir')
def stirmix():
    tester().stir()
    return "OK"

class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'job2', # 任务id
            'func': '__main__:autorun', # 任务执行程序
            'args': None, # 执行程序参数
            'trigger': 'interval', # 任务执行类型，定时器
            'seconds': getkhtime(), # 任务执行时间，单位秒
        },
        {
            'id': 'job3',  # 任务id
            'func': '__main__:autoreadPH',  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'interval',  # 任务执行类型，定时器
            'seconds': 10,  # 任务执行时间，单位秒
        }
    ]


app.config.from_object(SchedulerConfig())

if __name__ == '__main__':
    scheduler.init_app(app)  # 把任务列表载入实例flask
    scheduler.start()  # 启动任务计划
    app.run(host='0.0.0.0', port=5000, debug=False)



