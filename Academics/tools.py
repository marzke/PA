# create decision variables
# x_ij = person-section

# create objective function
# maximize sum(preference_i * x_i)

# create constraints

#1: a person is only in one place at a time

# get sections
# check all i,j<i for section conflicts
# for each section conflict j,k set constraint x_j + x_k <= 1
# pairwise may not be most efficient but will always be right

#2 non-negativity
#x_i >= 0

#3 sections have a single instructor
# column sum = 1

#4 instructors have <= maximum number of sections requested (or allowed)
# row sum <= max