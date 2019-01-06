from nltk.cluster.kmeans import KMeansClusterer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler  # For scaling dataset
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns
import nltk
from nltk.cluster.util import cosine_distance
sns.set()  # for plot styling

df = pd.read_csv('teacher.csv', encoding='utf-8')
df_copy = df
dictionary = df_copy.to_dict()

course_dict = {}  # will be adictionary of lists, key is teacher_id and val is list of courses
# will use that to convert to pandas dataframe
course_list = []  # temp storage for courses for a single teacher
total_course_list = []  # all unique courses offered by all teachers

for teacher, courses in dictionary['course_name'].items():
    #print('course is ',courses)
    if isinstance(courses, str):
        line = courses.split(',')
        for course in line:
            course_list.append(course)
            if course not in total_course_list:
                total_course_list.append(course)
        # + 1 since original data starts at 1, so 1-29
        course_dict[teacher+1] = course_list
        course_list = []
    else:
        print('bad course, skipping')
        print('teacher for non  alid course: ', teacher)
        course_dict[teacher+1] = ['-1']
        course_list = []

skill_list_total = []
temp_skill_list = []
skill_dict = {}

for teacher, skills in dictionary['selected_skills_keywords'].items():
    if isinstance(skills, str):
        line = skills.split(',')
        for skill in line:
            temp_skill_list.append(skill)
            if skill not in skill_list_total:
                skill_list_total.append(skill)
        skill_dict[teacher+1] = temp_skill_list  # add to dict
        temp_skill_list = []
    else:
        skill_dict[teacher+1] = 0  # as placeholder

big_data_list = []
big_skill_dict_list = []


def make_big_dataframe(total_list, dictionary, big_list):
    for i in range(1, 30):
        # print('dictionary at i: \n')
        small_dict = make_small_dict(total_list, dictionary[i])
        # convert to dataframe and append to overall
        big_list.append(small_dict)
    return pd.DataFrame(big_list)

#print ('course dict num keys: ', len(course_dict))

# NEW PLAN: MAke 28 small dataframes and append them all together lmao
# this isn't about performance its about testing
# ternary in python, 1 if teacher has course 0 if not


def make_small_dict(total_course_list, cur_courses):
    new_dict = {}
    for course in total_course_list:
        new_dict[course] = 1 if course in cur_courses else 0
    return new_dict


big_data_frame = make_big_dataframe(
    total_course_list, course_dict, big_data_list)
big_data_skills = make_big_dataframe(
    skill_list_total, skill_dict, big_skill_dict_list)

# appends df to another df, column by column. result is union of dataframes


def add_columns_but_slowly(df_to_slice, df):
    for column in df_to_slice:
        df[column] = df_to_slice[column]
    return df


big_data_all = add_columns_but_slowly(big_data_frame, big_data_skills)

big_data_copy = big_data_all
# Scaling of data
ss = StandardScaler()
ss.fit_transform(big_data_copy)

# K means Clustering


def doKmeans(X, nclust=2):
    model = KMeans(nclust)
    model.fit(X)
    clust_labels = model.predict(X)
    cent = model.cluster_centers_
    return (clust_labels, cent)

# clust_labels, cent = doKmeans(big_data_all, 2)
# kmeans = pd.DataFrame(clust_labels)
# big_data_copy.insert((big_data_copy.shape[1]),'kmeans',kmeans)

# print(kmeans)

# #Plot the clusters obtained using k means
# fig = plt.figure()
# ax = fig.add_subplot(111)


# scatter = ax.scatter(big_data_copy['Accounting'],big_data_copy['3D Printing'],
#                       c=kmeans[0],s=50)

# plt.colorbar(scatter)

# this one is not working out...dataframe might not be correct format
NUM_CLUSTERS = 10
kclusterer = KMeansClusterer(
    NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(big_data_copy, assign_clusters=True)


'''NEW PLAN, thanks Evan
    ONE HOT ENCODIGN BUT WITH ADDED UP VECTROS
    ex:
        Math 1 Art 2 Math 3 CS 50
    Joe     1   0       0    0
    Bob     0   0       1    0
    Smith   1   0       0    0
    Bob     0   1       0    0
    Smith   0   0       0    1

    groupByIndividual alphabetical is fine probably, jsut 
    want them to be same name next to each other

        Math 1 Art 2 Math 3 CS 50
    Joe     1   0       0    0
    Bob     0   0       1    0
    Bob     0   1       0    0
    Smith   0   0       0    1
    Smith   1   0       0    0

    Then add up the vectors 

    Math 1 Art 2 Math 3 CS 50
    Joe     1   0       0    0
    Bob     0   1       1    0
    Smith   1   0       0    1

    1. same as before, need all professors as records and all classes as columns: Pass 1
    2.  For each record: if len(courses)> 1, create additional record for those courses: Pass 2
    3.  When finished processing records of same professor, add up all vectors to achieve final binary vector: pass 2
    4. KMeans on final dataframe of binaries
    5. Decode kMeans to determine ?course recommendations?/ it might just be 
        How do I decode tho? Some kind of dicionary? Is that built in or do i make it?
        And if it is builtin, how does me adding vectors together change that? 
        I feel like it has to be custom

'''
'''1. How do I interprer k means results. Do I need to pyplot? on jupyter notebooks
    2. Assuming I like my reuslts, how do decode/inverse transform. 
    This isn't one hot encoding, so argmax won't work. Either create additional column that contains
    values that are 1's for each teacher, then find the correct string somehow...
    This entials a 156 byte string with that many characters, many of which are 0s.
    Koind of seems like I should treat like a sparse array of characters, hwhere
    i keep track of index of 1's in a single list. Then have a dictionary of lists that I can
    use to go back to original content? So during the encoding process, if I 
    encode a 1, add that index to a list and insert that list as an entry in a dictionary
    Then finally, figure out if i need an additional dictionary mapping integers to column names,
    or if iloc or some built in relative locationing in the columns in dataframe work '''

'''TLDR: how does one hot encoding lead to kmeans? i have no idea, euclidean distance makes no
    sense in this context.'''
