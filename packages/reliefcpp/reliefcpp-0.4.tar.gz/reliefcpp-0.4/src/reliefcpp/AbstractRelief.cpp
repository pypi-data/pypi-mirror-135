#include "AbstractRelief.h"

std::mutex g_scores_lock; // Lock the update of scores from each thread

AbstractRelief::AbstractRelief(size_t n_iter, size_t n_jobs, metric_enum name)
    : _n_iter(n_iter)
    , _n_jobs(n_jobs)
    , __metric_name(name)
{
    if (n_iter < 1)
        throw Exception("Must have at least one iteration.");
    if (n_jobs > std::thread::hardware_concurrency())
        throw Exception("Number of jobs is greater than number of cores.");
    if (n_jobs < 1)
        throw Exception("Number of jobs must be positive.");
}

void AbstractRelief::fit(const Dataset& X, const Labels& y)
{
    if (X.size() < _n_iter)
        throw Exception("Number of iterations cannot be greater than number of samples.");
    if (X.size() != y.size())
        throw Exception("Number of samples must equal number of labels.");

    _n_samples = X.size();
    if (_n_samples < 2)
        throw Exception("At least 2 samples must be provided.");
    _n_features = X[0].size();
    if (_n_features < 1)
        throw Exception("At least 1 feature must be provided.");

    this->_verify_labels(y); // Check if binary or multiclass, etc

    // Build a vector of indices that will determine the order in which
    // we process samples
    vector<size_t> indices(_n_samples);
    std::iota(indices.begin(), indices.end(), 0);
    utils::shuffle(indices.begin(), indices.end());
    // Reset scores vector
    _scores.resize(_n_features);
    std::fill(_scores.begin(), _scores.end(), 0);
    // If a single job, run a single loop
    if (_n_jobs <= 1) {
        // Main loop
        for (size_t i = 0; i < _n_iter; ++i) {
            this->_process_sample(indices[i], X, y, _scores);
            // Check for SIGTERM
            if (PyErr_CheckSignals() != 0)
                throw Exception("Interrupted");
        }
    } else {
        if (_n_jobs > _n_iter)
            throw Exception("Number of jobs greater than number of iterations.");
        // Fancy ceil
        size_t points_per_thread = (_n_iter + _n_jobs - 1) / _n_jobs;
#ifdef DEBUG
        cout << "Using " << points_per_thread << " points per thread.\n";
#endif
        vector<std::thread> threads(_n_jobs);
        // std::thread threads[_n_jobs];
        size_t begin = 0; // Starting point for thread
        size_t thread_id = 0;
        // Main loop
        // Split batches of data into separate threads
        while (begin < _n_iter) {
#ifdef DEBUG
            cout << "Starting thread " << thread_id << "\n";
#endif
            size_t ulimit = static_cast<size_t>(std::min(begin + points_per_thread, _n_iter));
            threads[thread_id++] = std::thread(&AbstractRelief::_fit_batch, this, std::cref(X), std::cref(y),
                std::cref(indices), begin, ulimit, thread_id);
            begin += points_per_thread;
        }

        for (size_t i = 0; i < thread_id; ++i)
            threads[i].join();
    }
    _scores /= _n_iter; // Normalize to ensure in range [0, 1]
}

void AbstractRelief::_fit_batch(
    const Dataset& X, const Labels& y, const vector<size_t>& indices,
    size_t begin, size_t end, size_t thread_id)
{
#ifdef DEBUG
    cout << "Thread " << thread_id << " using " << end - begin << " points.\n";
    size_t counter = 0;
#endif
    vector<double> scores(_n_features);
    for (size_t i = begin; i < end; ++i) {
        this->_process_sample(indices[i], X, y, scores);
        if (PyErr_CheckSignals() != 0)
            throw Exception("Interrupted");
#ifdef DEBUG
        ++counter;
        if (counter % 1000 == 0)
            cout << "Thread " << thread_id << " done " << counter << "\n";
#endif
    }
    // Update the scores safely
    for (size_t j = 0; j < _n_features; ++j) {
        g_scores_lock.lock();
        _scores[j] += scores[j];
        g_scores_lock.unlock();
    }
#ifdef DEBUG
    cout << "Ending thread " << thread_id << "\n";
#endif
}

Dataset AbstractRelief::transform(const Dataset& X) const
{
    if (_scores.empty())
        throw Exception("Please run `fit` first.");

    auto indices = argsort(_scores);
    std::reverse(indices.begin(), indices.end());

    size_t n_points = X.size();
    size_t n_features = indices.size();

    Dataset X_new(n_points, Datapoint(n_features));
    for (size_t i = 0; i < n_points; ++i)
        for (size_t j = 0; j < n_features; ++j)
            X_new[i][j] = X[i][indices[j]];

    return X_new;
}

double AbstractRelief::dist(const Datapoint& d1, const Datapoint& d2) const
{
    return metric::compute(d1, d2, __metric_name);
}

size_t AbstractRelief::get_n_iter() const
{
    return _n_iter;
}

size_t AbstractRelief::get_n_jobs() const
{
    return _n_jobs;
}

vector<double> AbstractRelief::get_scores() const
{
    return _scores;
}