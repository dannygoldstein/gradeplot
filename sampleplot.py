#!/usr/bin/env python

import numpy as np
from gradeplot import plot_colorful

grade_bounds = {'A': (45, None),
                'B': (40, 45),
                'C': (35, 40),
                'D': (30, 35),
                'F': (None, 30)}

grades = np.random.normal(37, 5, 500)

fig = plot_colorful(grades, grade_bounds)
fig.savefig('test.pdf')
