//
// This module defines the base class for all Relief variants.
// It implements `fit` and `transform` methods and a virtual method
// `_process_sample` that defines how scores are updated given a single sample.
//
// The `fit` operation is multithreaded.

#ifndef ABSTRACTRELIEF_H
#define ABSTRACTRELIEF_H

#include <Python.h>
#include <algorithm> // shuffle
#include <cstddef> // size_t
#include <functional> // cref
#include <mutex> // mutex
#include <numeric> // iota
#include <thread>
#include <vector>

#include "Operations.h"
#include "Utils.h"
#include "exceptions.h"

#ifdef DEBUG
#include <iostream>
using std::cout;
#endif

using std::vector;
using metric::metric_enum;

using Datapoint = vector<double>;
using Dataset = vector<Datapoint>;
using Label = size_t;
using Labels = vector<Label>;

class AbstractRelief {
public:
    AbstractRelief(size_t n_iter, size_t n_jobs, metric_enum name);
    virtual ~AbstractRelief() {};

    void fit(const Dataset& X, const Labels& y);
    // This method returns a Dataset of same shape as X
    // but with its features ordered according to their scores.
    // To keep only k features, in Python a user can do X_new[:, :k].
    Dataset transform(const Dataset& X) const;

    size_t get_n_iter() const;
    size_t get_n_jobs() const;
    double dist(const Datapoint& d1, const Datapoint& d2) const;
    vector<double> get_scores() const;

protected:
    // This method checks if the labels y conform with that Relief's
    // label standard. E.g., vanilla Relief requires binary labels.
    virtual void _verify_labels(const Labels& y) {};
    // This method processes a single sample and updates
    // scores accordingly. No need for locks here, since the update
    // for scores occurs within a single thread.
    virtual void _process_sample(size_t id, const Dataset& X, const Labels& y, vector<double>& scores) = 0;
    // This method is run in a new thread and processes a batch of samples.
    void _fit_batch(const Dataset& X, const Labels& y, const vector<size_t>& indices,
        size_t begin, size_t end, size_t thread_id);

private:
    vector<double> _scores;
    const size_t _n_iter;
    const size_t _n_jobs;
    const metric_enum __metric_name;
    size_t _n_samples;
    size_t _n_features;
};

#endif // ABSTRACTRELIEF_H