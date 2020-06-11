from statistictests import ChiSquare
import numpy

"""
This file should be used to keep all necessary code that is used for the verification section in part 6
of the programming assignment. It contains task 6.2.1.
"""

def task_6_2_1():
    """
    This task is used to verify the implementation of the chi square test.
    First, 100 samples are drawn from a normal distribution. Afterwards the chi square test is run on them to see,
    whether they follow the original or another given distribution.
    """
    # TODO Task 6.2.1: Your code goes here
    alpha = .1
    values = []
    numpy.random.seed(0)
    for _ in range(100):
        values.append(numpy.random.normal(15, 2))
    
    for bins in [40, 30, 10 ,5]:
        emp_n, emp_x = numpy.histogram(values, bins=bins, range=(0,50))
        cs = ChiSquare(emp_n=emp_n, emp_x=emp_x)
        [c1, c2] = cs.test_distribution(alpha, 15, 2)
        print "No. bins: "+str(bins)
        print "Calculated chi2 value: "+str(c1)+"\nchi2 value from table: "+str(c2)
        print "Result: "+str(c2 > c1)+"\n"
        emp_n = []
        emp_x = []
    pass


if __name__ == '__main__':
    task_6_2_1()