#ifndef PYTHON_INTERFACE_H
#define PYTHON_INTERFACE_H

#define PY_SSIZE_T_CLEAN
#include "numpy/arrayobject.h"
#include "numpy/ndarrayobject.h" // seg fault if not included
#include "numpy/ndarraytypes.h"
#include <Python.h>
#include <cstddef> // size_t
#include <exception>
#include <string>
#include <vector>

using std::size_t;
using std::string;
using std::vector;

#include "AbstractRelief.h"
#include "AbstractVanillaRelief.h"
#include "Relief.h"
#include "ReliefK.h"
#include "ReliefF.h"
#include "Utils.h"

enum variant {
    v_relief = 0,
    v_reliefK = 1,
    v_reliefF = 2
};

PyObject* capsule_AbstractRelief(AbstractRelief* relief);
AbstractRelief* decapsule_AbstractRelief(PyObject* py_relief);
void del_AbstractRelief(PyObject* py_relief);

AbstractRelief* create_Relief(size_t n_iter, size_t n_jobs, size_t n_neighbors, metric::metric_enum name, size_t type);

template <class T>
vector<T> create_1D_vector_from_array(PyObject* py_array);
template <class T>
vector<vector<T>> create_2D_vector_from_array(PyObject* py_array);
template <class T>
PyObject* create_array_from_1D_vector(const vector<T>& v, int type_num = PyArray_DOUBLE);
template <class T>
PyObject* create_array_from_2D_vector(const vector<vector<T>>& v, int type_num = PyArray_DOUBLE);

#ifdef __cplusplus
extern "C" {
#endif

static PyObject* _new_Relief(PyObject* self, PyObject* args, PyObject* keywds);
static PyObject* _Relief_fit(PyObject* self, PyObject* args, PyObject* keywds);
static PyObject* _Relief_transform(PyObject* self, PyObject* args, PyObject* keywds);
static PyObject* _Relief_get_scores(PyObject* self, PyObject* args, PyObject* keywds);

static PyMethodDef r_methods[] = {
    { "_new_Relief", (PyCFunction)_new_Relief, METH_VARARGS | METH_KEYWORDS, "" },
    { "_Relief_fit", (PyCFunction)_Relief_fit, METH_VARARGS | METH_KEYWORDS, "" },
    { "_Relief_transform", (PyCFunction)_Relief_transform, METH_VARARGS | METH_KEYWORDS, "" },
    { "_Relief_get_scores", (PyCFunction)_Relief_get_scores, METH_VARARGS | METH_KEYWORDS, "" },

    { NULL }
};

static struct PyModuleDef rmodule = {
    PyModuleDef_HEAD_INIT,
    "_c_relief",
    NULL,
    -1,
    r_methods
};

PyMODINIT_FUNC PyInit__c_relief(void)
{
    import_array();
    return PyModule_Create(&rmodule);
}

#ifdef __cplusplus
}
#endif

#endif // PYTHON_INTERFACE_H