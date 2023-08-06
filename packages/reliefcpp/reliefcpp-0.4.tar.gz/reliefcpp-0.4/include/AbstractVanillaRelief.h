//
// This module defines the abstract vanilla Relief variant.
// For each sample it picks a random
// near miss and a random near hit if the variant is Relief
// or averages the near misses and hits if the variant is ReliefK.

#ifndef ABSTRACTVANILLARELIEF_H
#define ABSTRACTVANILLARELIEF_H

#include <cstddef> // size_t
#include <utility> // pair
#include <vector>

#include "AbstractRelief.h"
#include "Operations.h"
#include "Utils.h"
#include "exceptions.h"

using metric::metric_enum;
using std::pair;
using std::vector;

class AbstractVanillaRelief : public AbstractRelief {
public:
    AbstractVanillaRelief(size_t n_iter, size_t n_jobs, size_t n_neighbors, metric_enum name);
    virtual ~AbstractVanillaRelief() { }

protected:
    void _process_sample(size_t id, const Dataset& X, const Labels& y, vector<double>& scores);
    virtual Datapoint _process_neighbors(size_t id, const Dataset& X, const vector<size_t>& indices) = 0;

private:
    const size_t __n_neighbors;
    vector<size_t> __extract_id_from_pair(const vector<pair<double, size_t>>& v);
};

#endif // ABSTRACTVANILLARELIEF_H