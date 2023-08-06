This package implements the Relief [KiraRendell]_ algorithm for
feature selection and some of its variants. It is written in C++
and exposed to Python as a C++ extension.

Variants
________
More precisely it implements the following variants

:Relief:
    This is the vanilla Relief algorithm. Given a data matrix of shape
    (n_samples, n_features) and a binary label vector :math:`y`, it computes
    for every sample :math:`s`, a neighborhood of hits and a neighborhood of misses.
    It then randomly picks one sample from each neighborhood, call these
    :math:`s_{nh}` and :math:`s_{nm}`, for near-hit and near-miss, respectively.
    The score for feature :math:`i` is updated via the following formula

    .. math::
        S[i] = S[i] - (s^i - s_{nh}^i)^2 + (s^i - s_{nm}^i)^2

    assuming some proper normalization is performed on the features.

    If dealing with multiclass problems, the near-miss neighborhood is
    constructed with points from all classes different than :math:`y(s)`.

:ReliefK:
    This is similar to *Relief* above, except that instead of picking a point
    at random from the neighborhood, it averages the contribution of every
    neighbor. More precisely, assuming the number of neighbors is :math:`k`,

    .. math::
        S[i] = S[i] - \frac{1}{k}\sum_j(s^i - s_{nh_j}^i)^2 \\
            + \frac{1}{k}\sum_j(s^i - s_{nm_j}^i)^2

:ReliefF:
    When dealing with multiclass problems it may be more appropriate to pick
    a neighbor from each differing class. *ReliefF* [Kononenko]_ does
    precisely this and averages the contributions of every point.

Installation
____________
Install this package via pip

    $ pip install reliefcpp

Use
___
The `reliefcpp` package contains `Relief`, `ReliefK`, and `ReliefF` classes.
The implement `fit`, `transform` and `fit_transform` methods, as well as a
`scores` property.

.. code-block:: python

    import numpy as np
    import reliefcpp

    n_samples = 2000
    n_features = 400
    n_classes = 5
    X = np.random.random((n_samples, n_features))
    y = np.random.randint(0, n_classes, n_samples)

    rf = reliefcpp.ReliefF(n_iter=1000, n_jobs=8)
    rf.fit(X, y)

    scores = rf.scores
    X_new = rf.transform(X) # Will return a matrix of same shape as X, but with its features reordered

MNIST Example
_____________
Running ReliefF on the MNIST digit dataset, yields the following feature (pixel)
importances:

.. image:: img/MNISTscores.png
  :width: 400
  :alt: MNIST pixel scores


References
__________

.. [KiraRendell] **Kira, K., Rendell, L. A.** (1992). *The Feature Selection Problem: Traditional Methods and a New Algorithm*.

.. [Kononenko] **Kononenko, I.** (1994). *Estimating Attributes: Analysis and Extensions of RELIEF*