/*
    Copyright Intel Corporation.
    
    This software and the related documents are Intel copyrighted materials, and
    your use of them is governed by the express license under which they were
    provided to you (License). Unless the License provides otherwise, you may
    not use, modify, copy, publish, distribute, disclose or transmit this
    software or the related documents without Intel's prior written permission.
    
    This software and the related documents are provided as is, with no express
    or implied warranties, other than those that are expressly stated in the
    License.
*/
#pragma once
#include "oneapi/ccl/types.hpp"
#include "oneapi/ccl/type_traits.hpp"
#ifdef CCL_ENABLE_SYCL
#include <CL/sycl.hpp>
#endif

namespace native {
namespace detail {

#ifdef CCL_ENABLE_SYCL
size_t get_sycl_device_id(const cl::sycl::device& dev);
size_t get_sycl_subdevice_id(const cl::sycl::device& dev);
#endif

} // namespace detail
} // namespace native
