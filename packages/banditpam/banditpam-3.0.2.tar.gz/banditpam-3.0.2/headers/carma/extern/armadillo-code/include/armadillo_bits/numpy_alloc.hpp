#ifndef INCLUDE_ARMADILLO_BITS_NUMPY_ALLOC_HPP_
#define INCLUDE_ARMADILLO_BITS_NUMPY_ALLOC_HPP_

#define NPY_NO_DEPRECATED_API NPY_1_14_API_VERSION
#include <numpy/arrayobject.h>
#include <numpy/ndarraytypes.h>

#ifdef ARMA_EXTRA_DEBUG
#include <iostream>
#endif

namespace arma {

inline void* npy_malloc(std::size_t bytes) {
    if (PyArray_API == NULL) {
        _import_array();
    }
#ifdef ARMA_EXTRA_DEBUG
    std::cerr << "Using numpy allocator" << "\n";
#endif  // ARMA_EXTRA_DEBUG
    return PyDataMem_NEW(bytes);
}

inline void npy_free(void* ptr) {
    if (PyArray_API == NULL) {
        _import_array();
    }
#ifdef ARMA_EXTRA_DEBUG
    std::cerr << "Using numpy deallocator" << "\n";
#endif  // ARMA_EXTRA_DEBUG
    PyDataMem_FREE(ptr);
}

} // namespace arma
#endif  // INCLUDE_ARMADILLO_BITS_NUMPY_ALLOC_HPP_
