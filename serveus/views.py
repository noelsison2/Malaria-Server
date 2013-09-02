import os
import datetime
import zipfile
import base64
import sha
import time
import glob
import xml.etree.ElementTree as ET
from flask import render_template, flash, redirect, request, url_for, make_response
from flask.ext.login import login_user, current_user, LoginManager, logout_user, login_required
from flask.ext.wtf import Required
from serveus import app
from forms import LoginForm
from werkzeug import secure_filename
from datetime import date
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from misc import Pagination

from models import db, User, UserType, Case, Key, Image

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
@app.route('/index/')
def index():
    form=LoginForm()
    return render_template("index.html",form=form)

@app.route('/dashboard/')
@login_required
def dashboard():
    cases = Case.query.all()
    return render_template("dashboard.html", user = current_user, cases=cases, date=datetime.datetime.now().strftime('%B %d, %Y'))

@app.route('/records/')
@login_required
def records2():
    print request.args.get('page')
    if not request.args.get('page'):
        page = 1
    else:
        page = int(request.args.get('page'))
    # Malaria Case Filters
    print request.args.get('malaria_selection')
    print request.args.get('region_selection')
    print request.args.get('date_start')
    print request.args.get('date_end')
    # Table sorter
    print request.args.get('sort_by') # date, location, diagnosis
    print request.args.get('order') # asc, desc
    if request.args:
        print 'Arguments present'
    else:
        print 'No arguments given'
    malariaList = ['Any Malaria Species','Falciparum','Vivax','Ovale','Malariae','No Malaria']
    regionList = ['The Philippines','NCR (National Capital Region)','CAR (Cordillera Administrative Region)','Region I (Ilocos Region)','Region II (Cagayan Valley)','Region III (Central Luzon)','Region IV-A (CALABARZON)','Region IV-B (MIMAROPA)','Region V (Bicol Region)','Region VI (Western Visayas)','Region VII (Central Visayas)','Region VIII (Eastern Visayas)','Region IX (Zamboanga Peninsula)','Region X (Northern Mindanao)','Region XI (Davao Region)','Region XII (Soccsksargen)','Region XIII (Caraga)','ARMM (Autonomous Region in Muslim Mindanao)']
    if request.args:
        #print request.form['malaria_selection']
        #print request.form['region_selection']
        #print request.form['date_start']
        #print request.form['date_end']
        malariaSelected = request.args.get('malaria_selection')
        regionSelected = request.args.get('region_selection')
        malariaIndex = malariaList.index(malariaSelected)
        regionIndex = regionList.index(regionSelected)
        
        date_start = request.args.get('date_start')
        date_end = request.args.get('date_end')
        sort_by = request.args.get('sort_by')
        order = request.args.get('order')
        # here
        caseList=''
        if date_start != 'The Beginning' :
            a=request.args.get('date_start')
            b=a.split('/')
            dt=datetime.date(int(b[2]),int(b[0]),int(b[1]))
            a=request.args.get('date_end')
            b=a.split('/')
            dte=datetime.date(int(b[2]),int(b[0]),int(b[1]))
        else :
            dt=datetime.date(1000,1,1)
            dte=datetime.date(9000,12,31)
        #print sort_by
        #print order
        sortby=''
        if sort_by== 'date':
            sortby='date'
        elif sort_by== 'location':
            sortby='address'
        elif sort_by== 'diagnosis':
            sortby='human_diagnosis'
        else:
            sortby='id'
        param= "\"case\"."+sortby+" "+order
        print param
        if regionIndex == 0 and malariaIndex == 0:
                caseList= Case.query.filter(Case.date>=dt,Case.date<=dte).order_by(param)
                #print param
          
        elif regionIndex == 0:
                caseList = Case.query.filter(Case.human_diagnosis == malariaSelected,Case.date>=dt,Case.date<=dte).order_by(param)       
        elif malariaIndex == 0:      
                caseList = Case.query.filter(Case.address.contains(regionSelected),Case.date>=dt,Case.date<=dte).order_by(param)
        else:
            caseList = Case.query.filter(Case.address.contains(regionSelected),Case.human_diagnosis == malariaSelected,Case.date>=dt,Case.date<=dte).order_by(param)
    else:
        # Default values
        malariaIndex = 0
        regionIndex = 0
        date_start = "The Beginning"
        date_end = "This Day"
        sort_by = "date"
        order = "desc"
        caseList = Case.query.order_by(Case.date.desc())

    # Pagination
    caseList = [i for i in caseList]
    pagination = Pagination(page, Pagination.PER_PAGE, len(caseList))
    caseList = caseList[(page-1)*Pagination.PER_PAGE : ((page-1)*Pagination.PER_PAGE) + Pagination.PER_PAGE]
    
    return render_template("records.html", caseList = caseList, pagination = pagination, malariaList = malariaList, regionList = regionList, malariaIndex = malariaIndex, regionIndex = regionIndex, date_start = date_start, date_end = date_end, sort_by = sort_by, order = order, user = current_user)

'''   
@app.route('/records/')
@login_required
def records():
    # Malaria Case Filters
    print request.args.get('malaria_selection')
    print request.args.get('region_selection')
    print request.args.get('date_start')
    print request.args.get('date_end')
    # Table sorter
    print request.args.get('sort_by') # date, location, diagnosis
    print request.args.get('order') # asc, desc
    if request.args:
        print 'Arguments present'
    else:
        print 'No arguments given'
    malariaList = ['Any Malaria Species','Falciparum','Vivax','Ovale','Malariae','Knowlesi','No Malaria']
    regionList = ['The Philippines','NCR (National Capital Region)','CAR (Cordillera Administrative Region)','Region I (Ilocos Region)','Region II (Cagayan Valley)','Region III (Central Luzon)','Region IV-A (CALABARZON)','Region IV-B (MIMAROPA)','Region V (Bicol Region)','Region VI (Western Visayas)','Region VII (Central Visayas)','Region VIII (Eastern Visayas)','Region IX (Zamboanga Peninsula)','Region X (Northern Mindanao)','Region XI (Davao Region)','Region XII (Soccsksargen)','Region XIII (Caraga)','ARMM (Autonomous Region in Muslim Mindanao)']
    if request.args:
        #print request.form['malaria_selection']
        #print request.form['region_selection']
        #print request.form['date_start']
        #print request.form['date_end']
        malariaSelected = request.args.get('malaria_selection')
        regionSelected = request.args.get('region_selection')
        malariaIndex = malariaList.index(malariaSelected)
        regionIndex = regionList.index(regionSelected)
        
        date_start = request.args.get('date_start')
        date_end = request.args.get('date_end')
        sort_by = request.args.get('sort_by')
        order = request.args.get('order')
        # here
        caseList=''
        if date_start != 'The Beginning' :
            a=request.args.get('date_start')
            b=a.split('/')
            dt=datetime.date(int(b[2]),int(b[0]),int(b[1]))
            a=request.args.get('date_end')
            b=a.split('/')
            dte=datetime.date(int(b[2]),int(b[0]),int(b[1]))
        else :
            dt=datetime.date(1000,1,1)
            dte=datetime.date(9000,12,31)
      #  print b
        if regionIndex ==0 and malariaIndex == 0:
            caseList= Case.query.filter(Case.date>=dt,Case.date<=dte).order_by(Case.date)
        elif regionIndex == 0:
            caseList = Case.query.filter(Case.human_diagnosis == malariaSelected,Case.date>=dt,Case.date<=dte).order_by(Case.date)
        elif malariaIndex == 0:
            caseList = Case.query.filter(Case.address.contains(regionSelected),Case.date>=dt,Case.date<=dte).order_by(Case.date)
        else:
            caseList = Case.query.filter(Case.address.contains(regionSelected),Case.human_diagnosis == malariaSelected,Case.date>=dt,Case.date<=dte).order_by(Case.date)
    else:
        malariaIndex = 0
        regionIndex = 0
        date_start = "The Beginning"
        date_end = "This Day"
        sort_by = "date"
        order = "desc"
        caseList = Case.query.order_by(Case.date.desc())
        
    return render_template("records.html", list = caseList, malariaList = malariaList, regionList = regionList, malariaIndex = malariaIndex, regionIndex = regionIndex, date_start = date_start, date_end = date_end, sort_by = sort_by, order = order, user = current_user)
'''
@app.route('/map/')
def maps():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    zoom = request.args.get('zoom')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    print str(lat)
    print str(lng)
    print str(zoom)
    print str(date_start)
    print str(date_end)
    if not (lat and lng and zoom and date_start and date_end):
        return redirect('/map/?lat=10.422988&lng=120.629883&zoom=7&date_start=Last 30 Days&date_end=Today')
    cl1 = Case.query.filter(Case.human_diagnosis == "Falciparum")
    cl2= []
    for i in cl1:
        cl2.append(str(i.lat)+','+str(i.lng))
    # Falciparum, vivax, malariae, ovale, no malaria
    list1 = cl2
    cl2= []
    cl1 = Case.query.filter(Case.human_diagnosis == "Vivax")
    for i in cl1:
        cl2.append(str(i.lat)+','+str(i.lng))
    list2 = cl2
    cl2= []
    cl1 = Case.query.filter(Case.human_diagnosis == "Malariae")
    for i in cl1:
        cl2.append(str(i.lat)+','+str(i.lng))
    list3 = cl2
    cl2= []
    cl1 = Case.query.filter(Case.human_diagnosis == "Ovale")
    for i in cl1:
        cl2.append(str(i.lat)+','+str(i.lng))
    list4 = cl2
    cl2= []
    cl1 = Case.query.filter(Case.human_diagnosis == "No Malaria")
    for i in cl1:
        cl2.append(str(i.lat)+','+str(i.lng))
    list5 = cl2
    return render_template("map.html", lat = lat, lng = lng, zoom = zoom, list1 = list1, list2 = list2, list3 = list3, list4 = list4, list5 = list5, date_start = date_start, date_end = date_end, user = current_user)

@app.route('/case/<int:id>/',  methods = ['GET', 'POST'])
def case(id):
    case = Case.query.get(id)
    #case.images = [str(i % 4 + 1) + '.png' for i in xrange(50)]
    images = []
    for img in case.images:
        images.append('pic/' + str(img.id))
    #case.images = images
    if request.method == 'POST':
        reportString = 'Patient ID: ' + str(case.id) + '<br>' + 'Date: ' + case.date.strftime('%B %d, %Y') + '<br>' + 'Age: ' + str(case.age) + '<br>' + 'Address: ' + case.address + '<br>' + 'Diagnosis: ' + case.human_diagnosis + '<br>' + 'Images: '
        if request.form:
            for i in range (0, len(images)):
                if str('checkbox_' + str(i)) in request.form:
                    reportString += str(images[i]) + ' '
        
        return reportString
    return render_template("case.html", case = case, user = current_user, images=images)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect("index")
    
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
    
@app.route('/login/',  methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error = False
    if form.validate_on_submit():
        #flash('Login Data: Username: ' + form.username.data + ' Password: ' + form.password.data)
        #return redirect('/index')
        
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username,password=password).first()
        if user:
            login_user(user)
            return redirect("/dashboard")
        else:
            return redirect("/index")
    else:
        error = True
        
    return redirect("/index")

# test view for experimentation    
@app.route('/test/',  methods = ['GET', 'POST'])
def test():
    if request.method == 'POST':
        if request.form and 'checker1' in request.form and 'checker2' in request.form:
            return request.form['checker1'] + ' ' + request.form['checker2']
        else:
            return 'off'
        
    return '''<html><head><title></title><link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen"><link href="/static/css/eyecon-datepicker.css" rel="stylesheet"></head><body><form action="" method="post"><input type="checkbox" name="checker1"><input type="checkbox" name="checker2"><input type="submit" value="Submit"></form><input type="text" id="dp1"><input type="text" id="dp2"> </body><script src="/static/js/jquery.js"></script><script src="/static/js/bootstrap.min.js"></script><script src="/static/js/eyecon-datepicker.js"></script><script>
    var checkin = $('#dp1').datepicker({
    onRender: function(date) {
            return date.valueOf();
            },
    autoclose: true,
    todayHighlight: true,
    });
    alert(checkin.date)
    $('#dp2').datepicker({
    startDate: checkin.date.valueOf(),
    autoclose: true,
    todayHighlight: true
    });
    </script></html>''' + str(range(0,10))


# API

UPLOAD_FOLDER = os.path.join(os.getcwd().replace('\\','/'), 'upload/')
REMOVE_TEMP = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/send/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # get file from form
        f = request.files['file']
        # if form is not empty
        if f:
            # temporarily save uploaded archive in folder with same name as archive filename
            filename = secure_filename(f.filename)
            folder = (app.config['UPLOAD_FOLDER'] + filename).replace('.zip', '')
            os.makedirs(folder)
            f.save(os.path.join(folder, filename))

            # extract uploaded archive to folder and delete original archive
            with open(os.path.join(folder, filename), 'r') as f:
                z = zipfile.ZipFile(f)
                z.extractall(folder)
            if REMOVE_TEMP:
                os.remove(f.name)

            # get encrypted AES key (128-bit SHA-1 of plaintext password) from XML file and decrypt using RSA private key
            with open(os.path.join(folder, 'accountData.xml'), 'r') as f:
                enc_aes_key = f.read()
            a = enc_aes_key.index('<pass>')
            b = enc_aes_key.index('</pass>')
            enc_aes_key = base64.b64decode(enc_aes_key[a+6:b])
            private_key = RSA.importKey(Key.query.first().private_key)
            aes_key = private_key.decrypt(enc_aes_key)

            # decrypt image archive using decrypted AES key
            with open(os.path.join(folder, 'cipherZipFile.zip'), 'r') as f:
                enc_img_zip = f.read()
                cipher = AES.new(aes_key, AES.MODE_ECB, 'dummy_parameter')
                msg = cipher.decrypt(enc_img_zip)

            # store decrypted image archive on disk
            with open(os.path.join(folder, 'decrypted.zip'), 'w') as f:
                f.write(msg)
            if REMOVE_TEMP:
                os.remove(os.path.join(folder, 'cipherZipFile.zip'))

            # extract decrypted image archive and store in database
            with open(os.path.join(folder, 'decrypted.zip'), 'r') as f:
                z = zipfile.ZipFile(f)
                z.extractall(folder)
            if REMOVE_TEMP:
                os.remove(f.name)

            # make case using XML data
            tree = ET.parse(os.path.join(folder, 'textData.xml'))
            root = tree.getroot()
            mapping = {}
            for child in root:
                mapping[child.tag] = child.text
            month, day, year = map(int, mapping['date-created'].split('/'))
            hours, minutes, seconds = map(int, mapping['time-created'].split(':'))
            latitude = float(mapping['latitude'])
            longitude = float(mapping['longitude'])
            species = mapping['species'].replace('Plasmodium ', '').capitalize()

            dt = datetime.datetime(year, month, day, hours, minutes, seconds)
            case = Case(date=dt,age=20,address="Address",human_diagnosis=species,lat=latitude,lng=longitude)
            db.session.add(case)
            db.session.commit() #TODO: commit optimization

            # store images in database
            for img_file in glob.glob(os.path.join(folder, "*.jpg")):
                img = Image(img_file, case)
                db.session.add(img)
                db.session.commit()

            return 'Success!'


    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/api/text/', methods=['POST'])
def upload_file2():
    if request.method == 'POST':
        print request.form['message']
        return 'got the message: %s' % request.form['message']

@app.route('/api/key/', methods=['GET'])
def update_key():
    return "009b32240dca3fcdce3ed04018fc9c0c7758a3f2e2bef63a79f0fc4f4a418d605307a946d08a620273f6dca9bef7e2ef3351385a79a3c3812f99955854a1c4c221e7b7a7b584696541ad4d9b5bed84f9071dd933914f290cc77090f23c9165a095ba574fa39a6652a2cbcce27ad9927556dc300176689569d197b5dcbd0cd7afc9"
    # TODO: change to dynamic POST (reliant on account credentials)
    key = Key.query.first()
    public_key = key.public_key
    return public_key

@app.route('/api/db/', methods=['GET','POST'])
def update_db():
    # if sent date < modified date
    # return 'no change'
    #return redirect(url_for('static', filename='db.db'))

    return """U1FMaXRlIGZvcm1hdCAzAAQAAQEAQCAgAAAABwAAAA0AAAAAAAAAAAAAAAYAAAAEAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAC3iJQUAAAABA/sAAAAADAP7AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKBg0AAAABA5IAA5IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0AAAADA9IAA+4D4wPSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8DAwAlTWljcm9zY29waXN0CQIDABlEb2N0b3IQAQMAJ0FkbWluaXN0cmF0b3IKAAAAAwPTAAPvA+QD0wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAMlAU1pY3Jvc2NvcGlzdAMKAxkBRG9jdG9yAhADJwlBZG1pbmlzdHJhdG9yDQAAAAMDAQADsgNPAwEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwDCgAhAV8XBwEAADIwMDctMDEtMDUYTkNSIChOYXRpb25hbCBDYXBpdGFsIFJlZ2lvbikgUXVlem9uIENpdHlPdmFsZUAtVwo9cKPXeWECCgAhAXEhBwcAADIwMTAtMDUtMTUSQ0FSIChDb3JkaWxsZXJhIEFkbWluaXN0cmF0aXZlIFJlZ2lvbikgQmFndWlvIENpdHlGYWxjaXBhcnVtQDBrhR64UexAXiZmZmZmZkwBCgAhAV8XBwEAADIwMDUtMDgtMjYUTkNSIChOYXRpb25hbCBDYXBpdGFsIFJlZ2lvbikgTWFuaWxhIENpdHlWaXZheEAtKPXCj1wpeQ0AAAAEA7EAA+kD2QPGA7EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwMTAWxvbAQJAxcBMTIzNDUDCQMXAXF3ZXJ0AgwDHwlnZW5pdXMxMjMNAAAAAwKxAAKxA64D1wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIF6BwcXFRUBg1d0YWJsZXVzZXJ1c2VyCENSRUFURSBUQUJMRSB1c2VyICgKCWlkIElOVEVHRVIgTk9UIE5VTEwsIAoJdXNlcm5hbWUgVkFSQ0hBUig4MCksIAoJcGFzc3dvcmQgVkFSQ0hBUigxMjApLCAKCXVzZXJ0eXBlX2lkIElOVEVHRVIsIAoJUFJJTUFSWSBLRVkgKGlkKSwgCglVTklRVUUgKHVzZXJuYW1lKSwgCglVTklRVUUgKHBhc3N3b3JkKSwgCglGT1JFSUdOIEtFWSh1c2VydHlwZV9pZCkgUkVGRVJFTkNFUyB1c2VydHlwZSAoaWQpCiknCAYXOxUBAGluZGV4c3FsaXRlX2F1dG9pbmRleF91c2VyXzF1c2VyCScJBhc7FQEAaW5kZXhzcWxpdGVfYXV0b2luZGV4X3VzZXJfMnVzZXILAAAAAFlnSno5dHlwdnZmaTd6TlJPRnA1bzhPQkw1bVZXRlNoeE1JaDU3ZW50WVJwWlVHdFRadGI3WVQ1QngzWk01RlAKS1F6SGNKRHlQSkZsb0pXNlYwK2ptbVpTb3N2TTRuclprblZXM0RBQmRtaVZhZEdYdGR5OUROZXZ5UUlEQVFBQgpBb0dBRjdKOVRObkFDbFhldzMrMkVRUm01dVpUQ21oVERsZjVmTEdhRGRXYWw4VzEyc1FrWGF6L2dPT0Y2Q2x2CndtZ1I1dW42N3EzeDBVMEtYNEtBVWI4d2dTMndsa1dZbFQwNjIrbUU3Y1lLWmgwN1p4Q0Z5K3lyZk02cVJydkEKSEpQYTYwVFRBUVRSWFNlb1g5RHJXSGxkK0pWS21sNzR2VjNvUVNUaGRnajcwZDBDUVFDMUVpNDhkaGZtQ3VyWQpzVlBqSFI2U3gwVVJxdEh2Wk1ISnJXMWVNYTBYMFFIU3M5aVNYRlptUUdENXFwclFCak5tTXJRZTh6ZDRVd3RvCnRQTW5QU3hqQWtFQTIycmQ3ZGVHbGFXYWFUb3NNRjEyaWt6TWQxS1A0MklLK0JXTUloNkhmb1hjeGo3SDFwUTcKUzdvU05ncXFJb2pnR0xaZkljOWJLZmEwc1NwNkdFK2M0d0pCQUtkMnZSUm1GQXhLSkpGc3o2ekpEYkdxWXBMSQpiWWorb3N1bmZmTVQ5b2FFWXk4LzdoalBGWWxVR1Z4UEVRYzc5T1djRjBKWXB3QzlyVnVWbnh5M1V3a0NRUUN3Cm5DazhPeUd5TEZUSVpER1RVSGVNeEZwRHBTbjZQVDFWQ0lyK0g1S3lMVzlTQnRCMWtHVFdCRlNLT1RWT2pOdk0KS0djVVlNSWhXZG1CVFE1dnFRMC9Ba0F4MlhjVjkwVi82aTg5RjJTRWxUM09jUXNqem5QSjU4VHVwUDVDa3I2bAozaThTWSsvcGlwNHpQVjAvZ2RTMjFWYmFPRXZ3eGFWT1VjbTFhbk5tQm1ScwotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLU1JR2ZNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0R05BRENCaVFLQmdRQ2JNaVFOeWovTnpqN1FRQmo4bkF4M1dLUHk0cjcyT25udy9FOUtRWTFnVXdlcFJ0Q0tZZ0p6OXR5cHZ2Zmk3ek5ST0ZwNW84T0JMNW1WV0ZTaHhNSWg1N2VudFlScFpVR3RUWnRiN1lUNUJ4M1pNNUZQS1F6SGNKRHlQSkZsb0pXNlYwK2ptbVpTb3N2TTRuclprblZXM0RBQmRtaVZhZEdYdGR5OUROZXZ5UUlEQVFBQgAAAAAAAAAAAAAAAAAAAA=="""

    temp = []
    for entry in User.query.all():
        username = entry.username
        password = sha.new(entry.password).hexdigest()
        temp.append(username + ',' + password)
    return '\n'.join(temp)

@app.route('/api/apk/', methods=['GET','POST'])
def update_apk():
    # if sent version < current version
    # return 'no change'
    return redirect(url_for('static', filename='apk.apk'))

@app.route('/pic/<int:picture_id>/', methods=['GET'])
def fetch_image(picture_id):
    x = Image.query.get(picture_id)
    response = make_response(x.im)
    response.headers['Content-Type'] = 'image/jpeg'
    return response
