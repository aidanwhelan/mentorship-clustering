# mentorship-clustering.py
#
# This program will:
#     1) Receive a CSV of responses from a number of mentees
#     2) Receive a CSV of responses from a number of mentors
#     3) Create list objects of responses for each mentor and mentee
#     4) Use clustering algorithm with mentors as nodes and mentees as
#         neighbors
#             a) All mentors have K mentees
#             b) Mentors and mentees are asked the same N questions
#             c) All questions are scales
#             d) Distances are calculated in N dimensions
#
# May 26 2020
# Aidan Whelan

import numpy as np
import pandas as pd

# RECEIVE MENTEE CSV ##########################################################
mentee_df = pd.read_csv("")

# RECEIVE MENTOR CSV ##########################################################
mentor_df = pd.read_csv("")

# CREATE LISTS FOR MENTORS AND MENTEES ########################################
mentees = []
mentors = []

class Mentee(self,df,row):
    def __init__(self,df,row):
        self.name = df["Name"][row]
        self.id = row
        self.responses = []             #ADD: SURVEY RESPONSES
        for i in range(n):              #REPLACE: range(n) for range of response columns
            self.responses.append(df.loc[self.name, i])
        self.claimed = False

class Mentor(self,df,row):
    def __init__(self,df,row):
        self.name = df["Name"][row]
        self.id = row
        self.responses = []
        for i in range(n):              #REPLACE: range(n) for range of response columns
            self.responses.append(df.loc[self.name, i])
        self.distances = []
        self.neighbors = []

    # Instantiate all responders
for i in range(mentee_df.shape[0]):     # number of rows in mentee_df
    mentees.append(Mentee(mentee_df,i))

for i in range(mentor_df.shape[0]):     # number of rows in mentor_df
    mentors.append(Mentor(mentor_df,i))

# (CLUSTER) CALCULATE EUCLIDEAN DISTACE ###########################################
def multi_dim_Dist(val_list_A, val_list_B):  # fun(A,B) = sqrt(sum(A[i]-B[i])^2)
    sum = 0
    assert len(val_list_A) == len(val_list_B)   #check for same lengths
    length = len(val_list_A)
    for i in range(length):
        sum += (val_list_A[i]-val_list_B[i])**2
    diff = sum**(0.5)                           #distance between A and B
    return diff

    # Find distances between each mentor and mentee
for i in range(len(mentors)):
    for j in range(len(mentees)):
        mentors[i].distances.append(multi_dim_Dist(mentors[i].responses, mentees[i].responses))

# (CLUSTER) GET NEAREST NEIGHBORS #################################################
    # Iterate through mentees and find closest mentor
    # When closest mentor is found, assign mentee to mentor neighbors[]
    # When mentee is assigned, set mentee.claimed flag to True
num_mentees = mentee_df.shape[0]
num_mentors = mentor_df.shape[0]
mentees_per_mentor = num_mentees/num_mentors
for z in range(mentees_per_mentor):             # Loop evenly over mentors
    for i in range(len(mentors)):
        ind_sort = np.argsort(mentors[i].distances) # Find indeces of ordered shortest distances
        for j in range(len(ind_sort)):
            if(ind_sort[j]==j):
                if(mentees[j].claimed == False):
                    mentees[j].claimed = True
                    mentors[i].neighbors.append(mentees[j])
                    break
    # Each mentor should now have the same number of unique neighbors

# RETURN PAIRINGS #############################################################
for i in range(len(mentors)):
    for j in range(len(mentors[i].neighbors)):
        print("Mentor: " + mentors[i].name + "\t Mentee: " + mentors[i].neighbors[j].name)
