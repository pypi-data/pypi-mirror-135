# LabTools3
Set of Python analysis tools for physics labs. It contains the "package" directory which is the Python package with a setup.py script for installation and
a "doc" directory containing the Sphinx documentation. The repository starts with version 0.2.9 of LabTools.
Version 1.0.2:  has mostly some big fixes.

Version 1.1.0:  now includes 2D-histograms and some bug fixes.

Version 1.1.1:  includes 3D lego plot for *histo2d*. Note that at the moment surface and lego plots are only in linear scale possible.

Version 1.1.2:  non-linear fitting is now based on *scipy.optimize.least_squares* so parameter bounds can be used.

Version 1.1.3.1:  (same as 1.1.3) updated the *rebin* function for 1D histograms, by default it now returns a new histogram (*replace = False*). Also added the options to have the mean calculated for combined bins instead of the sum (*use_mean = True*). Fixed a bug in *project_x* and *project_y* functions for 2D histograms.

Version 1.1.3.2: minor bug fixes

Version 1.1.3.3: histogram axis labels are preserved in rebinning and projection actions (for 2d histogram)

Version 1.1.3.4: minor bug fixes

Version 1.1.3.5: corrected problen with add_data

Version 1.1.3.6: added features to fitting: *plot* attribute to plot the fit, the fit results is plotted by default (controlled with the *plot_fit* kwarg). The fit object are callable, returning the value of the fit function using the current values of the fit parameters. New attribute to datafile: *adata_comment_index*, a list of indices pointing to comment lines.
 
