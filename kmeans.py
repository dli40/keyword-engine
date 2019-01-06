from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

df = pd.read_csv('teacher.csv', encoding='utf-8')
df_copy = df
dictionary = df_copy.to_dict()

course_dict= {}  # will be adictionary of lists, key is teacher_id and val is list of courses
# will use that to convert to pandas dataframe

course_list = [] #temp storage for courses for a single teacher
total_course_list = [] #all unique courses offered by all teachers

for teacher, courses in dictionary['course_name'].items():
    #print('course is ',courses)
    if isinstance(courses,str):
        line = courses.split(',')
        for course in line:
            course_list.append(course)
        total_course_list.append(course_list)
        course_dict[teacher+1] = course_list #+ 1 since original data starts at 1, so 1-29
        course_list = []
    else:
        print('bad course, skipping')
        print('teacher for non  alid course: ', teacher)
        course_dict[teacher+1] = ['-1']
        course_list =[]

big_data_list = []

def make_big_dataframe(total_course_list):
    for i in range(1, 30):  # this is teachers, v bad i knowmake_small_dict(total_course_list, cur)
        small_dict = make_small_dict(total_course_list, course_dict[i])
        # convert to dataframe and append to overall
        big_data_list.append(small_dict)
    return pd.DataFrame(big_data_list)

def get_unique_same_order(list):  # for now does exact matching, so spaces matter
    new_list = []
    for courses in list:
        for course in courses:
            if course not in new_list:
                new_list.append(course)
    return new_list

#print ('course dict num keys: ', len(course_dict))
total_course_list = get_unique_same_order(total_course_list)

# NEW PLAN: MAke 28 small dataframes and append them all together lmao
# this isn't about performance its about testing
# ternary in python, 1 if teacher has course 0 if not

def make_small_dict(total_course_list, cur_courses):
    new_dict = {}
    for course in total_course_list:
        new_dict[course] = 1 if course in cur_courses else 0
    return new_dict

big_data_frame = make_big_dataframe(total_course_list)
#print(big_data_frame)

df_std = stats.zscore(big_data_frame[total_course_list])
kmeans = KMeans(n_clusters=24)
kmeans.fit_predict(df_std)
# centroids = kmeans.cluster_centers_
labels = kmeans.labels_

df_copy['clusters'] = labels

# print('these are my centroids: ', centroids)
print('learned labels is: ', labels)