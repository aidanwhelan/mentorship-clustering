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
HEADER_OFFSET = 2

# RECEIVE MENTEE CSV ##########################################################
mentee_df = pd.read_csv("demoMENTEE-Data.csv")
mentee_names_IDs = list(mentee_df.columns)[17:19]      # Name and ID
mentee_question_cols = list(mentee_df.columns)[19:]    # Questionnaire answers
num_mentees = mentee_df.shape[0] - HEADER_OFFSET       # Number of mentees (minus header rows)

# RECEIVE MENTOR CSV ##########################################################
mentor_df = pd.read_csv("demoMENTOR-Data.csv")
mentor_names_IDs = list(mentor_df.columns)[17:19]      # Name and ID
mentor_question_cols = list(mentor_df.columns)[19:]    # Questionnaire answers
num_mentors = mentor_df.shape[0] - HEADER_OFFSET

# CREATE LISTS FOR MENTORS AND MENTEES ########################################
mentees = []
mentors = []

    # Define classes for mentors and mentees
class Mentee:
    def __init__(self,df,row):
        self.name = df[mentee_names_IDs[0]][row + HEADER_OFFSET]
        self.id = df[mentee_names_IDs[1]][row + HEADER_OFFSET]
        self.responses = []
        for i in mentee_question_cols:           # Iterate over question labels
            self.responses.append(float(df[i][row + HEADER_OFFSET]))   # Append
        self.claimed = False

class Mentor:
    def __init__(self,df,row):
        self.name = df[mentor_names_IDs[0]][row + HEADER_OFFSET]
        self.id = df[mentor_names_IDs[1]][row + HEADER_OFFSET]
        self.responses = []
        for i in mentor_question_cols:           # Iterate over question labels
            self.responses.append(float(df[i][row + HEADER_OFFSET]))   # Append
        self.distances = []
        self.neighbors = []

    # Instantiate all responders
for i in range(num_mentees):                     # Number of mentee responders
    mentees.append(Mentee(mentee_df,i))

for i in range(num_mentors):                     # Number of mentor responders
    mentors.append(Mentor(mentor_df,i))

# (CLUSTER) CALCULATE EUCLIDEAN DISTACE ###########################################
def multi_dim_Dist(val_list_A, val_list_B):  # fun(A,B) = sqrt(sum(A[i]-B[i])^2)
    sum = 0
    assert len(val_list_A) == len(val_list_B)   # Check for same lengths
    length = len(val_list_A)
    for i in range(length):
        sum += (val_list_A[i]-val_list_B[i])**2
    diff = sum**(0.5)                           # Distance between A and B
    return diff

    # Find distances between each mentor and mentee
for i in range(num_mentors):                    # Iterate over mentors
    for j in range(num_mentees):                # Iterate over mentees
        mentors[i].distances.append(multi_dim_Dist(mentors[i].responses, mentees[j].responses))

# (CLUSTER) GET NEAREST NEIGHBORS #################################################
    # Iterate through mentees and find closest mentor
    # When closest mentor is found, assign mentee to mentor neighbors[]
    # When mentee is assigned, set mentee.claimed flag to True
mentees_per_mentor = int(num_mentees/num_mentors)
for z in range(mentees_per_mentor):                 # Loop five times
    for i in range(num_mentors):                    # Once for each mentor (total 25 times)
        ind_sort = np.argsort(mentors[i].distances) # Ordered indices from least to greatest
        for j in ind_sort:                          # Iterate over ordered index list
            if(mentees[j].claimed == False):        # IF the first smallest distance is not claimed:
                    mentees[j].claimed = True       # Claim the mentee
                    mentors[i].neighbors.append(mentees[j]) # Add mentee to list of the mentor's neighbors
                    break                           # Break out of ind_sort loop

    # Each mentor should now have the same number of unique neighbors

# RETURN PAIRINGS #############################################################
for i in range(len(mentors)):                       # Iterate over number of mentors (5)
    for j in range(len(mentors[i].neighbors)):      #
        print("Mentor: " + mentors[i].name + "\t Mentee: " + mentors[i].neighbors[j].name)
