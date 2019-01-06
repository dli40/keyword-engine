# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
import firebase_admin  # firebase crap
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection(u'teachers').get()

id_count =1
with open('courseNames.txt','w') as outfile:
    for doc in docs:
        temp_dict = doc.to_dict()
        try:
            classes = temp_dict['classes']
            outfile.write(str(id_count))
            outfile.write(': {')
            for classroom in classes:
                outfile.write((classroom['coursename']))
                outfile.write(', ')
        except KeyError:
            outfile.write('bad course\n')
            id_count+=1
            continue
        id_count+=1
        outfile.write('}\n')

print('DONE PRINTING\n')

id_count =1
with open ('tIndustry.txt', 'w') as outfile:
    for doc in docs:
        temp_dict = doc.to_dict()
        try:
            classes = temp_dict['selected_industry_keywords']
            outfile.write(str(id_count))
            outfile.write(': {')
            for classroom in classes:
                outfile.write(classroom)
                outfile.write(', ')
        except KeyError:
            outfile.write('bad course\n')
            id_count+=1
            continue
        id_count+=1
        outfile.write('}\n')
print('DONE PRINTING DATA\n')


id_count =1
with open('tSkills.txt','w') as outfile:
    for doc in docs:
        temp_dict = doc.to_dict()
        try:
            classes = temp_dict['selected_skills_keywords']
            outfile.write(str(id_count))
            outfile.write(': {')
            for classroom in classes:
                outfile.write(classroom)
                outfile.write(', ')
        except KeyError:
            outfile.write('bad course get for id ')
            id_count+=1
            continue
        id_count+=1
        outfile.write('}\n')

print('DONE PRINTING\n')