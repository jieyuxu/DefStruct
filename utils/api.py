from utils.db import User, TempInstance, Template, Request
from utils.base import session_factory, engine
from datetime import datetime, timedelta
from sqlalchemy import or_, and_
from flask_sqlalchemy_session import current_session

sess = current_session
#------------------------------------------------------------------------------------------

def getUser(net_id):
    user = sess.query(User)\
            .filter(User.net_id == net_id)\
            .first()

    if user is None:
        user = User(net_id= net_id)
        sess.add(user)
        sess.commit()

    return user

# get list of template objects -- to display in library
def getAllTemplates():
    templates = sess.query(Template).all()
    return templates

def getAllInstances(net_id):
    tempinstances = sess.query(TempInstance) \
            .filter(or_(TempInstance.owner_id == net_id, TempInstance.partner_id == net_id)) \
            .all()
    return tempinstances

# get user's requests
def getAllRequests(net_id): 
    requests = sess.query(Request)\
            .filter(Request.sender_id == net_id)\
            .all()
    
    return requests

def getTempInstance(instance_id):
    instance = sess.query(TempInstance)\
            .filter(TempInstance.instance_id == instance_id)\
            .first()
    return instance 

def getInstanceFromRequest(request_id):
    instance = sess.query(TempInstance)\
        .filter(TempInstance.request_id == request_id)\
        .first()
    return instance

def getHTML(template_id):
    template = sess.query(Template)\
            .filter(Template.temp_id == template_id)\
            .first()
    return template.html

def getState(instance_id):
    instance = getTempInstance(instance_id)
    return instance.savedState

def getTemplate(instance_id):
    instance = getTempInstance(instance_id)
    return instance.template

def getPartner(instance_id, net_id):
    instance = getTempInstance(instance_id)

    owner = instance.owner_id
    partner = instance.partner_id 

    if net_id == owner:
        return partner
    
    return owner

def getSentRequests(net_id):
    requests = sess.query(Request)\
            .filter(Request.sender_id == net_id)
    return requests

def getAwaitingRequests(net_id):
    requests = sess.query(Request)\
            .filter(Request.receiver_id == net_id)
    return requests

def getRequestByID(request_id):
    req = sess.query(Request)\
            .filter(Request.request_id == request_id).one()
    return req

def getDueDate(instance_id):
    instance = getTempInstance(instance_id)
    return instance.dueDate 

def ownsTemplate(net_id, template_id):
    instance = sess.query(TempInstance)\
            .filter(and_(or_(TempInstance.owner_id == net_id, TempInstance.partner_id == net_id)),\
            TempInstance.template_id == template_id)\
    # for testing
    # print(instance)
    if instance.count() > 0:
        return True 
    return False 

def deleteInstance(instance_id):
    instance = sess.query(TempInstance)\
        .filter(TempInstance.instance_id == instance_id).one()
    sess.delete(instance)
    sess.commit()
    count = sess.query(TempInstance)\
        .filter(TempInstance.instance_id == instance_id).count()
    return count == 0 

def deleteRequest(request_id):
    request = sess.query(Request)\
        .filter(Request.request_id == request_id).one()
    sess.delete(request)
    sess.commit()
    count = sess.query(Request)\
        .filter(Request.request_id == request_id).count()
    return count == 0
    
def addNewInstance(net_id, template_id):
    html = getHTML(template_id)
    newInst = TempInstance(owner_id=net_id, template_id=template_id, partner_id="", savedState=html, dueDate=datetime.now())
    sess.add(newInst)
    sess.commit()
    return newInst 
    
def addNewRequest(sender_id, receiver_id): 
    request = Request(sender_id=sender_id, receiver_id=receiver_id)
    sess.add(request)
    sess.commit()
    return request

def addPartner(instance_id, partner_id):
    instance = getTempInstance(instance_id)
    instance.partner_id = partner_id
    sess.commit()

def containsUser(net_id):
    count = sess.query(User)\
        .filter(User.net_id == net_id).count()
    if count == 0:
        return False
    return True 

def setRequest(instance_id, request_id):
    instance = getTempInstance(instance_id)
    instance.request_id = request_id
    # testing
    print(instance.request_id)
    sess.commit()
    return instance

def updateState(instance_id, html):
    try:
        instance = getTempInstance(instance_id)
        instance.savedState = html
        sess.commit()
        return True
    except Exception as e:
        print(e)
        return False
#------------------------------------------------------------------------------------------
# returns True if success, False if fail
# def addPartner(instance_id, partner_id):
#     instance = getTempInstance(instance_id)

#     if instance.partner_id == "":
#         instance.partner_id = partner_id
#         # get request to delete it
#         request = session.query(Request)\
#             .filter(Request.temp_instance == instance)\
#             .first()
#         session.delete(request)
        
#         return True

#     return False 

# def hasPartner(instance_id):
#     instance = session.query(TempInstance)\
#             .filter(TempInstance.instance_id == instance_id)\
#             .first()