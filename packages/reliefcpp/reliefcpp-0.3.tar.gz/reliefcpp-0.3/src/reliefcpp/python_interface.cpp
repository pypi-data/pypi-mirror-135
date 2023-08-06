#include "python_interface.h"

PyObject* capsule_AbstractRelief(AbstractRelief* relief)
{
    PyObject* py_relief = PyCapsule_New(relief, "relief.AbstractRelief.AbstractRelief", del_AbstractRelief);
    return py_relief;
}

AbstractRelief* decapsule_AbstractRelief(PyObject* py_relief)
{
    AbstractRelief* relief = (AbstractRelief*)PyCapsule_GetPointer(py_relief, "relief.AbstractRelief.AbstractRelief");
    return relief;
}

void del_AbstractRelief(PyObject* py_relief)
{
    AbstractRelief* relief = decapsule_AbstractRelief(py_relief);
    delete relief;
}

AbstractRelief* create_Relief(size_t n_iter, size_t n_jobs, size_t n_neighbors, metric::metric_enum name, size_t type)
{
    AbstractRelief* relief = NULL;
    if (type == v_relief)
        relief = new Relief(n_iter, n_jobs, n_neighbors, name);
    else if (type == v_reliefK)
        relief = new ReliefK(n_iter, n_jobs, n_neighbors, name);
    else if (type == v_reliefF)
        relief = new ReliefF(n_iter, n_jobs, name);
    else
        throw Exception("Couldn't find variant.");
    return relief;
}

template <class T>
vector<T> create_1D_vector_from_array(PyObject* py_array)
{
    int ndim = PyArray_NDIM(py_array);
    if (ndim != 1)
        throw Exception("Not a 1D array.");
    npy_intp* dims = PyArray_DIMS(py_array);
    int array_size = (int)dims[0];
    vector<T> v(array_size);
    for (int i = 0; i < array_size; ++i)
        v[i] = *(T*)PyArray_GETPTR1(py_array, i);
    return v;
}

template <class T>
vector<vector<T>> create_2D_vector_from_array(PyObject* py_array)
{
    int ndim = PyArray_NDIM(py_array);
    if (ndim != 2)
        throw Exception("Not a 2D array.");
    npy_intp* dims = PyArray_DIMS(py_array);
    int dim1 = (int)dims[0];
    int dim2 = (int)dims[1];
    vector<vector<T>> v(dim1, vector<T>(dim2));
    for (int i = 0; i < dim1; ++i)
        for (int j = 0; j < dim2; ++j)
            v[i][j] = *(T*)PyArray_GETPTR2(py_array, i, j);
    return v;
}

template <class T>
PyObject* create_array_from_1D_vector(const vector<T>& v, int type_num)
{
    if (!v.empty()) {
        npy_intp dim = static_cast<npy_intp>(v.size());
        npy_intp dims[1] = { dim };
        PyObject* py_array = PyArray_SimpleNew(1, dims, type_num);

        T* py_array_ptr = (T*)PyArray_DATA(py_array);
        std::copy(v.begin(), v.end(), py_array_ptr);
        return py_array;
    } else {
        npy_intp dims[1] = { 0 };
        return PyArray_ZEROS(1, dims, type_num, 0);
    }
}

template <class T>
PyObject* create_array_from_2D_vector(const vector<vector<T>>& v, int type_num)
{
    if (!v.empty()) {
        size_t dim1 = v.size();
        size_t dim2 = v[0].size();
        npy_intp dims[2] = { static_cast<npy_intp>(dim1), static_cast<npy_intp>(dim2) };
        PyObject* py_array = PyArray_SimpleNew(2, dims, type_num);

        T* py_array_ptr = (T*)PyArray_DATA(py_array);
        for (size_t i = 0; i < dim1; ++i) {
            if (v[i].size() != dim2) {
                Py_DECREF(py_array);
                throw Exception("Found non-uniform vectors. Cannot convert to numpy.");
            }
            std::copy(v[i].begin(), v[i].end(), py_array_ptr + i * dim2);
        }
        return py_array;
    } else {
        npy_intp dims[2] = { 0, 0 };
        return PyArray_ZEROS(2, dims, type_num, 0);
    }
}

#ifdef __cplusplus
extern "C" {
#endif

PyObject* _new_Relief(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* py_n_iter = NULL;
    PyObject* py_n_jobs = NULL;
    PyObject* py_n_neighbors = NULL;
    PyObject* py_metric_name = NULL;
    PyObject* py_type = NULL;

    static const char* kwlist[] = { "n_iter", "n_jobs", "n_neighbors", "metric", "type", NULL };
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "OOOOO", (char**)kwlist,
            &py_n_iter, &py_n_jobs, &py_n_neighbors, &py_metric_name, &py_type))
        return NULL;

    try {
        size_t n_iter = PyLong_AsSize_t(PyNumber_Long(py_n_iter));
        size_t n_jobs = PyLong_AsSize_t(PyNumber_Long(py_n_jobs));
        size_t n_neighbors = PyLong_AsSize_t(PyNumber_Long(py_n_neighbors));
        size_t metric_name_i = PyLong_AsSize_t(PyNumber_Long(py_metric_name));
        size_t type = PyLong_AsSize_t(PyNumber_Long(py_type));
        metric::metric_enum metric_name = static_cast<metric::metric_enum>(metric_name_i);

        AbstractRelief* relief = create_Relief(n_iter, n_jobs, n_neighbors, metric_name, type);
        PyObject* py_relief = capsule_AbstractRelief(relief);
        return py_relief;
    } catch (std::exception const& e) {
        string s = "Could not construct relief: " + string(e.what());
        PyErr_SetString(PyExc_BaseException, s.c_str());
        return NULL;
    }
}

PyObject* _Relief_fit(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* py_relief = NULL;
    PyObject* py_X = NULL;
    PyObject* py_y = NULL;
    static const char* kwlist[] = { "relief", "X", "y", NULL };

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "OOO", (char**)kwlist, &py_relief, &py_X, &py_y))
        return NULL;

    try {
        // Error Handling
        if (py_X == Py_None) {
            py_X = NULL; // Needed so that Py_XDECREF is skipped
            throw Exception("data object cannot be None.");
        }
        if (py_y == Py_None) {
            py_y = NULL; // Needed so that Py_XDECREF is skipped
            throw Exception("labels cannot be None.");
        }

        py_X = PyArray_FROMANY(py_X, NPY_DOUBLE, 2, 2, NPY_ARRAY_IN_ARRAY);
        if (!py_X)
            return NULL;
        py_y = PyArray_FROMANY(py_y, NPY_INT, 1, 1, NPY_ARRAY_IN_ARRAY | NPY_ARRAY_FORCECAST);
        if (!py_y) {
            Py_DECREF(py_X);
            return NULL;
        }
        AbstractRelief* relief = decapsule_AbstractRelief(py_relief);

        auto X = create_2D_vector_from_array<double>(py_X);
        auto y_int = create_1D_vector_from_array<int>(py_y);
        vector<size_t> y(y_int.begin(), y_int.end()); // Convert to size_t

        relief->fit(X, y);

        Py_DECREF(py_X);
        Py_DECREF(py_y);
        Py_INCREF(Py_None);
        return Py_None;
    } catch (std::exception const& e) {
        Py_XDECREF(py_X);
        Py_XDECREF(py_y);
        string s = "Could not fit data: " + string(e.what());
        PyErr_SetString(PyExc_BaseException, s.c_str());
        return NULL;
    }
}

PyObject* _Relief_transform(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* py_relief = NULL;
    PyObject* py_X = NULL;
    static const char* kwlist[] = { "relief", "X", NULL };

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "OO", (char**)kwlist, &py_relief, &py_X))
        return NULL;

    try {
        // Error Handling
        if (py_X == Py_None) {
            py_X = NULL; // Needed so that Py_XDECREF is skipped
            throw Exception("data object cannot be None.");
        }
        py_X = PyArray_FROMANY(py_X, NPY_DOUBLE, 2, 2, NPY_ARRAY_IN_ARRAY);
        if (!py_X)
            return NULL;
        AbstractRelief* relief = decapsule_AbstractRelief(py_relief);
        auto X = create_2D_vector_from_array<double>(py_X);
        auto X_new = relief->transform(X);
        // Convert to numpy and return
        PyObject* py_X_new = create_array_from_2D_vector<double>(X_new, PyArray_DOUBLE);
        Py_DECREF(py_X);
        return py_X_new;
    } catch (std::exception const& e) {
        Py_XDECREF(py_X);
        string s = "Could not transform data: " + string(e.what());
        PyErr_SetString(PyExc_BaseException, s.c_str());
        return NULL;
    }
}

PyObject* _Relief_get_scores(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* py_relief = NULL;
    static const char* kwlist[] = { "relief", NULL };

    if (!PyArg_ParseTupleAndKeywords(args, keywds, "O", (char**)kwlist, &py_relief))
        return NULL;

    try {
        AbstractRelief* relief = decapsule_AbstractRelief(py_relief);
        auto scores = relief->get_scores();
        // Convert to numpy and return
        return create_array_from_1D_vector<double>(scores, PyArray_DOUBLE);
    } catch (std::exception const& e) {
        string s = "Could not get scores: " + string(e.what());
        PyErr_SetString(PyExc_BaseException, s.c_str());
        return NULL;
    }
}

#ifdef __cplusplus
}
#endif