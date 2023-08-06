/* -== file: buffer.hpp ==- */
/*******************************************************************************
* Copyright 2006-2021 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

#ifndef _ONEAPI_MKL_VM_BUFFER_HPP_
#define _ONEAPI_MKL_VM_BUFFER_HPP_ 1

#include <cstdint>
#include <complex>
#include <exception>

#include <CL/sycl.hpp>

#include "oneapi/mkl/vm/decls.hpp"


namespace oneapi {
namespace mkl {
namespace vm {

// abs:
// abs: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// abs: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event abs(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// acos:
// acos: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// acos: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acos(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// acosh:
// acosh: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// acosh: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acosh(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// acospi:
// acospi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event acospi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acospi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// acospi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event acospi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event acospi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// add:
// add: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// add: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event add(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// arg:
// arg: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event arg(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event arg(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// arg: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event arg(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event arg(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// asin:
// asin: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// asin: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asin(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// asinh:
// asinh: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// asinh: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event asinh(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// asinpi:
// asinpi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event asinpi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asinpi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// asinpi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event asinpi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event asinpi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// atan:
// atan: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// atan2:
// atan2: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event atan2(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan2(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan2: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event atan2(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan2(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// atan2pi:
// atan2pi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event atan2pi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan2pi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan2pi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event atan2pi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atan2pi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// atanh:
// atanh: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// atanh: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event atanh(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// atanpi:
// atanpi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event atanpi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atanpi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atanpi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event atanpi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event atanpi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// cbrt:
// cbrt: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cbrt(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event cbrt(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// cbrt: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cbrt(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event cbrt(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// cdfnorm:
// cdfnorm: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorm(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorm(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// cdfnorm: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorm(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorm(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// cdfnorminv:
// cdfnorminv: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorminv(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorminv(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// cdfnorminv: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorminv(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cdfnorminv(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// ceil:
// ceil: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event ceil(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event ceil(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// ceil: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event ceil(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event ceil(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// cis:
// cis: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cis(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cis(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// cis: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cis(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cis(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// conj:
// conj: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event conj(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event conj(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// conj: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event conj(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event conj(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// copysign:
// copysign: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event copysign(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event copysign(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// copysign: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event copysign(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event copysign(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// cos:
// cos: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// cos: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cos(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// cosd:
// cosd: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cosd(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosd(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// cosd: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cosd(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosd(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// cosh:
// cosh: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// cosh: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cosh(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// cospi:
// cospi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event cospi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cospi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// cospi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event cospi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event cospi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// div:
// div: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// div: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event div(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// erf:
// erf: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event erf(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event erf(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// erf: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event erf(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event erf(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// erfc:
// erfc: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event erfc(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event erfc(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// erfc: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event erfc(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event erfc(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// erfcinv:
// erfcinv: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event erfcinv(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event erfcinv(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// erfcinv: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event erfcinv(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event erfcinv(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// erfinv:
// erfinv: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event erfinv(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event erfinv(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// erfinv: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event erfinv(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event erfinv(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// exp:
// exp: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// exp: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// exp10:
// exp10: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event exp10(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp10(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// exp10: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event exp10(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp10(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// exp2:
// exp2: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event exp2(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp2(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// exp2: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event exp2(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event exp2(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// expint1:
// expint1: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event expint1(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event expint1(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// expint1: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event expint1(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event expint1(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// expm1:
// expm1: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event expm1(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event expm1(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// expm1: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event expm1(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event expm1(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// fdim:
// fdim: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event fdim(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event fdim(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fdim: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event fdim(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event fdim(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// floor:
// floor: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event floor(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event floor(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// floor: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event floor(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event floor(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// fmax:
// fmax: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event fmax(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event fmax(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmax: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event fmax(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event fmax(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// fmin:
// fmin: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event fmin(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event fmin(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmin: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event fmin(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event fmin(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// fmod:
// fmod: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event fmod(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event fmod(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// fmod: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event fmod(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event fmod(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// frac:
// frac: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event frac(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event frac(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// frac: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event frac(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event frac(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// hypot:
// hypot: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event hypot(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event hypot(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// hypot: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event hypot(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event hypot(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// inv:
// inv: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event inv(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event inv(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// inv: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event inv(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event inv(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// invcbrt:
// invcbrt: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event invcbrt(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event invcbrt(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// invcbrt: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event invcbrt(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event invcbrt(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// invsqrt:
// invsqrt: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event invsqrt(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event invsqrt(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// invsqrt: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event invsqrt(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event invsqrt(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// lgamma:
// lgamma: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event lgamma(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event lgamma(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// lgamma: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event lgamma(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event lgamma(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// linearfrac:
// linearfrac: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event linearfrac(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, float c, float d, float e, float f, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event linearfrac(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, double c, double d, double e, double f, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// linearfrac: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event linearfrac(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, float c, float d, float e, float f, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event linearfrac(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, double c, double d, double e, double f, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// ln:
// ln: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// ln: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event ln(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// log10:
// log10: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// log10: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log10(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// log1p:
// log1p: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event log1p(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log1p(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// log1p: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event log1p(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log1p(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// log2:
// log2: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event log2(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log2(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// log2: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event log2(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event log2(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// logb:
// logb: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event logb(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event logb(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// logb: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event logb(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event logb(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// maxmag:
// maxmag: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event maxmag(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event maxmag(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// maxmag: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event maxmag(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event maxmag(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// minmag:
// minmag: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event minmag(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event minmag(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// minmag: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event minmag(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event minmag(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// modf:
// modf: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event modf(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, sycl::buffer<float, 1> & z, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event modf(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, sycl::buffer<double, 1> & z, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// modf: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event modf(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, sycl::buffer<float, 1> & z, oneapi::mkl::slice sz, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event modf(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, sycl::buffer<double, 1> & z, oneapi::mkl::slice sz, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// mul:
// mul: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// mul: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mul(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// mulbyconj:
// mulbyconj: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event mulbyconj(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mulbyconj(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// mulbyconj: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event mulbyconj(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event mulbyconj(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// nearbyint:
// nearbyint: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event nearbyint(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event nearbyint(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// nearbyint: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event nearbyint(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event nearbyint(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// nextafter:
// nextafter: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event nextafter(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event nextafter(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// nextafter: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event nextafter(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event nextafter(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// pow:
// pow: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// pow: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// pow2o3:
// pow2o3: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event pow2o3(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event pow2o3(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// pow2o3: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event pow2o3(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event pow2o3(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// pow3o2:
// pow3o2: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event pow3o2(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow3o2(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// pow3o2: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event pow3o2(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event pow3o2(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// powr:
// powr: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event powr(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powr(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// powr: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event powr(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powr(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// powx:
// powx: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, float b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, double b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, std::complex<float> b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, std::complex<double> b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// powx: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, float b, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, double b, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, std::complex<float> b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event powx(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, std::complex<double> b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// remainder:
// remainder: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event remainder(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event remainder(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// remainder: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event remainder(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event remainder(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// rint:
// rint: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event rint(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event rint(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// rint: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event rint(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event rint(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// round:
// round: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event round(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event round(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// round: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event round(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event round(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// sin:
// sin: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// sin: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sin(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// sincos:
// sincos: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sincos(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, sycl::buffer<float, 1> & z, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sincos(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, sycl::buffer<double, 1> & z, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// sincos: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sincos(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, sycl::buffer<float, 1> & z, oneapi::mkl::slice sz, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sincos(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, sycl::buffer<double, 1> & z, oneapi::mkl::slice sz, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// sind:
// sind: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sind(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sind(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// sind: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sind(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sind(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// sinh:
// sinh: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// sinh: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinh(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// sinpi:
// sinpi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sinpi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinpi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// sinpi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sinpi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sinpi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// sqr:
// sqr: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sqr(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event sqr(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// sqr: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sqr(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event sqr(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// sqrt:
// sqrt: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// sqrt: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sqrt(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// sub:
// sub: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & b, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & b, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & b, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & b, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// sub: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & b, oneapi::mkl::slice sb, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & b, oneapi::mkl::slice sb, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event sub(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & b, oneapi::mkl::slice sb, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// tan:
// tan: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});

// tan: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<float> > eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tan(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<std::complex<double> > eh = {});



// tand:
// tand: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event tand(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tand(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// tand: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event tand(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tand(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// tanh:
// tanh: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<float>, 1> & a, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, std::int64_t n, sycl::buffer<std::complex<double>, 1> & a, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// tanh: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, sycl::buffer<std::complex<float>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<float>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event tanh(sycl::queue & queue, sycl::buffer<std::complex<double>, 1> & a, oneapi::mkl::slice sa, sycl::buffer<std::complex<double>, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);



// tanpi:
// tanpi: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event tanpi(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tanpi(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// tanpi: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event tanpi(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tanpi(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// tgamma:
// tgamma: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event tgamma(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tgamma(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});

// tgamma: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event tgamma(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<float> eh = {});
__ONEAPI_MKL_VM_EXPORT sycl::event tgamma(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined, oneapi::mkl::vm::error_handler<double> eh = {});



// trunc:
// trunc: indexing: linear
__ONEAPI_MKL_VM_EXPORT sycl::event trunc(sycl::queue & queue, std::int64_t n, sycl::buffer<float, 1> & a, sycl::buffer<float, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event trunc(sycl::queue & queue, std::int64_t n, sycl::buffer<double, 1> & a, sycl::buffer<double, 1> & y, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// trunc: indexing: strided
__ONEAPI_MKL_VM_EXPORT sycl::event trunc(sycl::queue & queue, sycl::buffer<float, 1> & a, oneapi::mkl::slice sa, sycl::buffer<float, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
__ONEAPI_MKL_VM_EXPORT sycl::event trunc(sycl::queue & queue, sycl::buffer<double, 1> & a, oneapi::mkl::slice sa, sycl::buffer<double, 1> & y, oneapi::mkl::slice sy, oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);




} // namespace vm
} // namespace mkl
} // namespace oneapi
#endif // ifndef _ONEAPI_MKL_VM_BUFFER_HPP_
