
__all__ = ['plot_colorful']
__whatami__ = 'Utility for plotting colorful grade histograms.'
__author__ = 'Danny Goldstein <dgold@berkeley.edu>'


def plot_colorful(grade_array, grade_boundaries, plotfile_name,
                  title='Student Grades', x_tight=False, **plot_kwargs):
    """Plot a histogram of student grades, color-coded by letter grade,
    and save it as a pdf.

    Parameters
    ----------
    grade_array : array-like, 1-d
         Array of raw scores.
    grade_boundaries : dict
         Dictionary mapping letter grades to a range of raw
         scores. Use None to specify an unbounded endpoint.

         Example:

         {'A':(45, None),
          'B':(40, 45),
          'C':(35, 40),
          'D':(30, 35),
          'F':(None, 30)}
    plotfile_name: str
        Name of file in which to write the plot.
    title: str
        Plot title.
    x_tight: Boolean
        If true, make the x limits on the plot hug the data.
    plot_kwargs:
        Keyword arguments to be passed to the matplotlib `hist` function.

    """

    import numpy as np
    import matplotlib.pyplot as plt
    try:
        import seaborn as sns
        sns.set_style('ticks')
        sb = True
    except ImportError:
        sb = False
    from itertools import chain

    grade_array = np.asarray(grade_array)

    # Take histogram bins to be between 0 and the maximum of the grade
    # array in steps of 1.

    gmax = np.ceil(grade_array.max())
    gmin = np.floor(grade_array.min())
    bins = np.linspace(0, gmax, gmax + 1).tolist()

    num_bounds = [val for val in list(chain(*grade_boundaries.values()))
                  if val is not None]

    for bound in num_bounds:
        if bound not in bins:
            bins.append(bound)

    bins = np.asarray(bins)
    bins.sort()

    # Draw the figure.

    fig, ax = plt.subplots(figsize=(8, 5))
    n, bins, patches = ax.hist(grade_array, bins=bins, **plot_kwargs)

    # Color the histogram patches based on the passed grade
    # boundaries, and compute the legend labels.

    legend_labels = list()
    legend_handles = list()

    color_cycle = ax._get_lines.color_cycle
    iterlist = sorted(grade_boundaries.keys())

    for letter_grade in iterlist:
        intvl = grade_boundaries[letter_grade]

        high = intvl[1] if intvl[1] is not None else np.inf
        low = intvl[0] if intvl[0] is not None else -np.inf

        # Count the number of students in the interval.
        cond = np.logical_and(grade_array < high, grade_array >= low)
        ng = grade_array[cond].size

        # Compute the legend label.
        label = '%s (%s - %s): %d' % (letter_grade,
                                      '' if intvl[0] is None else intvl[0],
                                      '' if intvl[1] is None else intvl[1],
                                      ng)

        # Color the patches.
        color = next(color_cycle)
        to_color = [patch for i, patch in enumerate(patches)
                    if (bins[i] >= low) and (bins[i + 1] <= high)]

        for patch in to_color:
            patch.set_facecolor(color)

        if len(to_color) > 0:
            legend_labels.append(label)
            legend_handles.append(to_color[0])

    # Create plot labels.

    ax.set_title(title)
    ax.set_xlabel('Score')
    ax.set_xlim(-.1 * gmax if not x_tight else .9 * gmin, 1.1 * gmax)
    ax.legend(legend_handles, legend_labels, loc='best', frameon=False)
    if sb:
        sns.despine()
        sns.set_context('talk')
    fig.tight_layout()
    fig.savefig(plotfile_name, format='pdf')
