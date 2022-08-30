#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 18:49:40 2018

@author: szczurpi

Program checks if there are possible schedules for students for a given
start and finish term, given all constraints.
This works by mapping a term number to each course, given all constraints.
It assigns a negative term number if course is not taken (e.g. elective that is not needed)

ASSUMPTION: term numbers start with 1
"""
import pandas as pd
import numpy as np
from constraint import *

def create_term_list(terms, years=4):
    '''Create a list of term indexes for years in the future'''
    all_terms = []
    for year in range(years):
        for term in terms:    
            all_terms.append(year*6+term)
    return all_terms
    
def map_to_term_label(term_num):
    '''Returns the label of a term, given its number'''
    term_num_to_label_map = {
            0: 'Fall 1',
            1: 'Fall 2',
            2: 'Spring 1',
            3: 'Spring 2',
            4: 'Summer 1',
            5: 'Summer 2',
    }
    if (term_num < 1):
        return 'Not Taken'
    else:
        return 'Year ' + str((term_num - 1) // 6 + 1) + ' ' + term_num_to_label_map[(term_num - 1) % 6]

def prereq(a, b):
    '''Used for encoding prerequisite constraints, a is a prerequisite for b'''
    if a > 0 and b > 0: # Taking both prereq a and course b
        return a < b
    elif a > 0 and b < 0: # Taking prereq a, but not course b
        return True
    elif a < 0 and b > 0: #  Taking course b, but not prereq a
        return False
    else:
        return True # Not taking prereq a or course b

def get_possible_course_list(start, finish):
    '''Returns a possible course schedule, assuming student starts in start term
       finishes in finish term'''
    problem = Problem()
    
    # Read course_offerings file
    course_offerings = pd.read_excel('csp_course_rotations.xlsx', sheet_name='course_rotations')
    course_prereqs = pd.read_excel('csp_course_rotations.xlsx', sheet_name='prereqs')

    # Foundation course terms
    foundation_courses = course_offerings[course_offerings.Type=='foundation']
    for r,row in foundation_courses.iterrows():
        problem.addVariable(row.Course, create_term_list(list(row[row==1].index)))
    
    # Core course terms
    core_courses = course_offerings[course_offerings.Type=='core']
    for r,row in core_courses.iterrows():
        problem.addVariable(row.Course, create_term_list(list(row[row==1].index)))
    
    # CS Electives course terms (-x = elective not taken)
    elective_courses = course_offerings[course_offerings.Type=='elective']
    n = -1
    for r,row in elective_courses.iterrows():
        l = create_term_list(list(row[row==1].index))
        l.append(n)
        problem.addVariable(row.Course, l)
        n = n - 1
    
    # Capstone
    capstone_courses = course_offerings[course_offerings.Type=='capstone']
    for r,row in capstone_courses.iterrows():
        problem.addVariable(row.Course, create_term_list(list(row[row==1].index)))
    
    # Guarantee no repeats of courses
    problem.addConstraint(AllDifferentConstraint())
    
    # Control start and finish terms
    MAX_YEARS = 4
    START_TERM = start
    FINISH_TERM = finish
    LAST_TERM = (MAX_YEARS+1)*6
    problem.addConstraint(SomeInSetConstraint([START_TERM]))
    problem.addConstraint(NotInSetConstraint(list(range(START_TERM))))
    problem.addConstraint(NotInSetConstraint(list(np.arange(FINISH_TERM+1,LAST_TERM))))
    
    # Control electives - exactly 3 courses must be chosen
    NUM_ELECTIVES = 8
    ELECTIVES_NEEDED = 3
    problem.addConstraint(SomeInSetConstraint(list(np.arange(-NUM_ELECTIVES,0)),n=NUM_ELECTIVES-ELECTIVES_NEEDED,exact=True))
    
    # Prereqs    
    for r,row in course_prereqs.iterrows():
        problem.addConstraint(prereq, [row.prereq, row.course])
    
    # Generate a possible solution
    sol = problem.getSolutions()
    print(len(sol))
    if (len(sol) > 0):
        s = pd.Series(sol[0])
        return s.sort_values().map(map_to_term_label)
    else:
        return None

# Check for possible schedules for all start terms
for start in [1]:
    print('START TERM = ' + map_to_term_label(start))
    s = get_possible_course_list(start,start+13)
    if s is None:
        print('NO POSSIBLE SCHEDULE!')
    else:
        s2 = pd.Series(s.index.values, index=s)
        print(s2.to_string())
    print()

