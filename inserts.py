# 1 - imports
from datetime import date, datetime
from utils.base import Base, session_factory, engine
from utils.db import User, TempInstance, Request, Template 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

session = session_factory()
# 2 - create a new session
Base.metadata.drop_all(engine)
print('dropped database')
session.commit()

# 3 - generate database schema
Base.metadata.create_all(engine)

# 4 - create users
# jyxu = User(net_id='jyxu')
# 5 - create template

try: 
    with open('templates/bufferoverrun.html') as f: 
        content = f.read()
    bufferoverrun = Template(html=content, name="COS 217: Buffer Overrun")

    with open('templates/tsp.html') as g: 
        content = g.read()
    tsp = Template(html=content, name="COS 126: Travelling Salesperson")
except Exception as e:
    bufferoverrun = Template(html="error happened", name='error')
    tsp = Template(html="error happened", name='error')
    print("inserts.py: unable to open file")

# 6 - create a request
# print("creating a request")
# jyxu_bob = Request(sender_id='jyxu', receiver_id=bob.net_id)
# session.flush()
# print("printing request jyxu_bob ", jyxu_bob)

# inst1 = TempInstance(template=bufferoverrun, dueDate=datetime.now(), owner=jyxu, partner_id="", request=jyxu_bob, savedState="")

# print("printing jyxu_bob's request temp instance: ", jyxu_bob.instance)
# # 7 - create an instance


# # updateRequest(inst1.instance_id, jyxu_bob)
# print("jyxu_bob's request temp instance: ", jyxu_bob.instance)

# 8 - persists data
# session.add(jyxu)
session.add(bufferoverrun)
session.add(tsp)
# session.add(jyxu_bob)

# 10 - commit and close session
session.commit()
# print("#----------------------------------------------------------------------------------------------------")
# print("printing bob ", bob)
# print(bufferoverrun)
# # print("check if request and instances are linked: ", inst1.request)
# #----------------------------------------------------------------------------------------------------
# print("#----------------------------------------------------------------------------------------------------")
# print("testing get user".upper())
# # print('getting user jyxu', getUser('jyxu'))
# print('getting user bob', getUser('bob'))
# print("#----------------------------------------------------------------------------------------------------")
# print("testing get all templates".upper())
# templates = getAllTemplates()
# for template in templates:
#     print("template: ", template)
# print("#----------------------------------------------------------------------------------------------------")
# print("testing get all instances".upper())
# instances = getAllInstances('bob')

# print("printing all of bob's instances")
# for inst in instances:
#     print("template: ", template)
#     print("due date is ", getDueDate(inst.instance_id))
# print("#----------------------------------------------------------------------------------------------------")
# print("testing get all request".upper())
# requests = getAllRequests('jyxu')

# print("printing all of jyxu's instances")
# for req in requests:
#     print("request: ", req)
# print("#----------------------------------------------------------------------------------------------------")

# addPartner(inst1.instance_id, 'bob')
# print(getPartner(inst1.instance_id, 'jyxu'))
# print(inst1.partner_id)
session.close()

