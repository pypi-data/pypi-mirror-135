//
// This module defines the vanilla ReliefF variant for multiclass problems.
// For each sample it finds a neighbor from every other class.

#ifndef RELIEFF_H
#define RELIEFF_H

#include <cstddef> // size_t
#include <map>
#include <utility>
#include <vector>

#include "AbstractRelief.h"
#include "Utils.h"

using metric::metric_enum;
using std::map;
using std::pair;
using std::vector;

class ReliefF : public AbstractRelief {
public:
    using AbstractRelief::AbstractRelief;

protected:
    void _verify_labels(const Labels& y);
    void _process_sample(size_t id, const Dataset& X, const Labels& y, vector<double>& scores);

private:
    map<Label, double> __prior_p;
};

#endif