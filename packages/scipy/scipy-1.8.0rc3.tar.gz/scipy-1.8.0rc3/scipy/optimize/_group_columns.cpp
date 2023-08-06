#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int32.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/int32.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/intp.hpp>
#include <pythonic/include/numpy/ndarray/fill.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/ge.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/not_.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/intp.hpp>
#include <pythonic/numpy/ndarray/fill.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/ge.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/not_.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__group_columns
{
  struct group_sparse
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type3>()))>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
      typedef decltype(std::declval<__type5>()(std::declval<__type1>())) __type7;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
      typedef indexable<__type8> __type9;
      typedef typename __combined<__type4,__type9>::type __type10;
      typedef typename pythonic::assignable<long>::type __type11;
      typedef container<typename std::remove_reference<__type11>::type> __type12;
      typedef typename __combined<__type10,__type12,__type9,__type12>::type __type13;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type13>())) __type14;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type14>::type>::type __type15;
      typedef decltype(std::declval<__type5>()(std::declval<__type15>())) __type16;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
      typedef indexable<__type17> __type18;
      typedef typename __combined<__type10,__type18>::type __type19;
      typedef typename pythonic::returnable<typename __combined<__type19,__type12,__type9,__type12,__type18>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& m, argument_type1&& n, argument_type2&& indices, argument_type3&& indptr) const
    ;
  }  ;
  struct group_dense
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type3>()))>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
      typedef decltype(std::declval<__type5>()(std::declval<__type1>())) __type7;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
      typedef indexable<__type8> __type9;
      typedef typename __combined<__type4,__type9>::type __type10;
      typedef typename pythonic::assignable<long>::type __type11;
      typedef container<typename std::remove_reference<__type11>::type> __type12;
      typedef typename __combined<__type10,__type12,__type9,__type12>::type __type13;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type13>())) __type14;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type14>::type>::type __type15;
      typedef decltype(std::declval<__type5>()(std::declval<__type15>())) __type16;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
      typedef indexable<__type17> __type18;
      typedef typename __combined<__type10,__type18>::type __type19;
      typedef typename pythonic::returnable<typename __combined<__type19,__type12,__type9,__type12,__type18>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& m, argument_type1&& n, argument_type2&& A) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename group_sparse::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type group_sparse::operator()(argument_type0&& m, argument_type1&& n, argument_type2&& indices, argument_type3&& indptr) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type2;
    typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type3>()))>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
    typedef decltype(std::declval<__type5>()(std::declval<__type1>())) __type7;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
    typedef indexable<__type8> __type9;
    typedef typename __combined<__type4,__type9>::type __type10;
    typedef typename pythonic::assignable<long>::type __type11;
    typedef long __type12;
    typedef decltype(pythonic::operator_::add(std::declval<__type11>(), std::declval<__type12>())) __type13;
    typedef typename __combined<__type11,__type13>::type __type14;
    typedef typename __combined<__type14,__type12>::type __type15;
    typedef container<typename std::remove_reference<__type15>::type> __type16;
    typedef typename __combined<__type10,__type16,__type9,__type16>::type __type17;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type17>())) __type18;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type18>::type>::type __type19;
    typedef decltype(std::declval<__type5>()(std::declval<__type19>())) __type20;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type20>::type::iterator>::value_type>::type __type21;
    typedef indexable<__type21> __type22;
    typedef typename __combined<__type10,__type22>::type __type23;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type26;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type27;
    typedef typename pythonic::assignable<decltype(std::declval<__type26>()(std::declval<__type27>(), std::declval<__type2>()))>::type __type28;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type29;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type30;
    typedef decltype(std::declval<__type30>()[std::declval<__type8>()]) __type32;
    typedef decltype(pythonic::operator_::add(std::declval<__type8>(), std::declval<__type12>())) __type35;
    typedef decltype(std::declval<__type30>()[std::declval<__type35>()]) __type36;
    typedef decltype(std::declval<__type5>()(std::declval<__type32>(), std::declval<__type36>())) __type37;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type37>::type::iterator>::value_type>::type __type38;
    typedef decltype(std::declval<__type29>()[std::declval<__type38>()]) __type39;
    typedef indexable<__type39> __type40;
    typedef typename __combined<__type28,__type40>::type __type41;
    typedef decltype(std::declval<__type30>()[std::declval<__type21>()]) __type45;
    typedef decltype(pythonic::operator_::add(std::declval<__type21>(), std::declval<__type12>())) __type48;
    typedef decltype(std::declval<__type30>()[std::declval<__type48>()]) __type49;
    typedef decltype(std::declval<__type5>()(std::declval<__type45>(), std::declval<__type49>())) __type50;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type50>::type::iterator>::value_type>::type __type51;
    typedef decltype(std::declval<__type29>()[std::declval<__type51>()]) __type52;
    typedef indexable<__type52> __type53;
    typedef typename __combined<__type41,__type53>::type __type54;
    typedef container<typename std::remove_reference<__type12>::type> __type55;
    typename pythonic::assignable<typename __combined<__type23,__type16,__type9,__type16,__type22>::type>::type groups = pythonic::operator_::neg(pythonic::numpy::functor::ones{}(n, pythonic::numpy::functor::intp{}));
    typename pythonic::assignable<typename __combined<__type14,__type12>::type>::type current_group = 0L;
    typename pythonic::assignable<typename __combined<__type54,__type55,__type40,__type53>::type>::type union_ = pythonic::numpy::functor::empty{}(m, pythonic::numpy::functor::intp{});
    {
      long  __target140098694533712 = n;
      for (long  i=0L; i < __target140098694533712; i += 1L)
      {
        if (pythonic::operator_::ge(groups[i], 0L))
        {
          continue;
        }
        groups[i] = current_group;
        typename pythonic::lazy<decltype(true)>::type all_grouped = true;
        pythonic::numpy::ndarray::functor::fill{}(union_, 0L);
        {
          long  __target140098694536688 = indptr[pythonic::operator_::add(i, 1L)];
          for (long  k=indptr[i]; k < __target140098694536688; k += 1L)
          {
            union_[indices[k]] = 1L;
          }
        }
        {
          long  __target140098694537280 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, groups));
          for (long  j=0L; j < __target140098694537280; j += 1L)
          {
            if (pythonic::operator_::lt(groups[j], 0L))
            {
              all_grouped = false;
            }
            else
            {
              continue;
            }
            typename pythonic::lazy<decltype(false)>::type intersect = false;
            {
              long  __target140098694539680 = indptr[pythonic::operator_::add(j, 1L)];
              for (long  k_=indptr[j]; k_ < __target140098694539680; k_ += 1L)
              {
                if (pythonic::operator_::eq(union_[indices[k_]], 1L))
                {
                  intersect = true;
                  break;
                }
              }
            }
            if (pythonic::operator_::not_(intersect))
            {
              {
                long  __target140098694637504 = indptr[pythonic::operator_::add(j, 1L)];
                for (long  k__=indptr[j]; k__ < __target140098694637504; k__ += 1L)
                {
                  union_[indices[k__]] = 1L;
                }
              }
              groups[j] = current_group;
            }
          }
        }
        if (all_grouped)
        {
          break;
        }
        else
        {
          current_group += 1L;
        }
      }
    }
    return groups;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename group_dense::type<argument_type0, argument_type1, argument_type2>::result_type group_dense::operator()(argument_type0&& m, argument_type1&& n, argument_type2&& A) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::intp{})>::type>::type __type2;
    typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type3>()))>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type5;
    typedef decltype(std::declval<__type5>()(std::declval<__type1>())) __type7;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
    typedef indexable<__type8> __type9;
    typedef typename __combined<__type4,__type9>::type __type10;
    typedef typename pythonic::assignable<long>::type __type11;
    typedef long __type12;
    typedef decltype(pythonic::operator_::add(std::declval<__type11>(), std::declval<__type12>())) __type13;
    typedef typename __combined<__type11,__type13>::type __type14;
    typedef typename __combined<__type14,__type12>::type __type15;
    typedef container<typename std::remove_reference<__type15>::type> __type16;
    typedef typename __combined<__type10,__type16,__type9,__type16>::type __type17;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type17>())) __type18;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type18>::type>::type __type19;
    typedef decltype(std::declval<__type5>()(std::declval<__type19>())) __type20;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type20>::type::iterator>::value_type>::type __type21;
    typedef indexable<__type21> __type22;
    typedef typename __combined<__type10,__type22>::type __type23;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type26;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type27;
    typedef typename pythonic::assignable<decltype(std::declval<__type26>()(std::declval<__type27>(), std::declval<__type2>()))>::type __type28;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type29;
    typedef typename pythonic::assignable<decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, std::declval<__type29>()))>::type __type30;
    typedef decltype(std::declval<__type30>()[std::declval<__type21>()]) __type32;
    typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type32>())) __type33;
    typedef typename __combined<__type28,__type33>::type __type34;
    typedef decltype(std::declval<__type30>()[std::declval<__type8>()]) __type37;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::getattr(pythonic::types::attr::T{}, A))>::type B = pythonic::builtins::getattr(pythonic::types::attr::T{}, A);
    typename pythonic::assignable<typename __combined<__type23,__type16,__type9,__type16,__type22>::type>::type groups = pythonic::operator_::neg(pythonic::numpy::functor::ones{}(n, pythonic::numpy::functor::intp{}));
    typename pythonic::assignable<typename __combined<__type14,__type12>::type>::type current_group = 0L;
    typename pythonic::assignable<typename __combined<__type34,__type37,__type32>::type>::type union_ = pythonic::numpy::functor::empty{}(m, pythonic::numpy::functor::intp{});
    {
      long  __target140098690944064 = n;
      for (long  i=0L; i < __target140098690944064; i += 1L)
      {
        if (pythonic::operator_::ge(groups[i], 0L))
        {
          continue;
        }
        groups[i] = current_group;
        typename pythonic::lazy<decltype(true)>::type all_grouped = true;
        union_[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = B[i];
        {
          long  __target140098694512992 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, groups));
          for (long  j=0L; j < __target140098694512992; j += 1L)
          {
            if (pythonic::operator_::lt(groups[j], 0L))
            {
              all_grouped = false;
            }
            else
            {
              continue;
            }
            typename pythonic::lazy<decltype(false)>::type intersect = false;
            {
              long  __target140098694514528 = m;
              for (long  k=0L; k < __target140098694514528; k += 1L)
              {
                if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(union_[k], 0L); }, [&] () { return pythonic::operator_::gt(B[pythonic::types::make_tuple(j, k)], 0L); }))
                {
                  intersect = true;
                  break;
                }
              }
            }
            if (pythonic::operator_::not_(intersect))
            {
              union_ += B[j];
              groups[j] = current_group;
            }
          }
        }
        if (all_grouped)
        {
          break;
        }
        else
        {
          current_group += 1L;
        }
      }
    }
    return groups;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>::result_type group_sparse0(long&& m, long&& n, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indices, pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>::result_type group_sparse1(long&& m, long&& n, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indices, pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::ndarray<long,pythonic::types::pshape<long>>, pythonic::types::ndarray<long,pythonic::types::pshape<long>>>::result_type group_sparse2(long&& m, long&& n, pythonic::types::ndarray<long,pythonic::types::pshape<long>>&& indices, pythonic::types::ndarray<long,pythonic::types::pshape<long>>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_sparse::type<long, long, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>::result_type group_sparse3(long&& m, long&& n, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>&& indices, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>&& indptr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_sparse()(m, n, indices, indptr);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type group_dense0(long&& m, long&& n, pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type group_dense1(long&& m, long&& n, pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>::result_type group_dense2(long&& m, long&& n, pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__group_columns::group_dense::type<long, long, pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>>::result_type group_dense3(long&& m, long&& n, pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__group_columns::group_dense()(m, n, A);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_group_sparse0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3]))
        return to_python(group_sparse0(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<long,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_sparse1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]) && is_convertible<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3]))
        return to_python(group_sparse1(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[2]), from_python<pythonic::types::numpy_gexpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>,pythonic::types::normalized_slice>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_sparse2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[3]))
        return to_python(group_sparse2(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_sparse3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "indices", "indptr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[3]))
        return to_python(group_sparse3(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[2]))
        return to_python(group_dense0(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[2]))
        return to_python(group_dense1(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>(args_obj[2]))
        return to_python(group_dense2(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_group_dense3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"m", "n", "A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<long>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>>(args_obj[2]))
        return to_python(group_dense3(from_python<long>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<npy_int32,pythonic::types::pshape<long,long>>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_group_sparse(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_group_sparse0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_sparse1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_sparse2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_sparse3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "group_sparse", "\n""    - group_sparse(int, int, int[::], int[::])\n""    - group_sparse(int, int, int32[::], int32[::])\n""    - group_sparse(int, int, int[:], int[:])\n""    - group_sparse(int, int, int32[:], int32[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_group_dense(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_group_dense0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_dense1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_dense2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_group_dense3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "group_dense", "\n""    - group_dense(int, int, int[:,:])\n""    - group_dense(int, int, int32[:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "group_sparse",
    (PyCFunction)__pythran_wrapall_group_sparse,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - group_sparse(int, int, int[::], int[::])\n""    - group_sparse(int, int, int32[::], int32[::])\n""    - group_sparse(int, int, int[:], int[:])\n""    - group_sparse(int, int, int32[:], int32[:])"},{
    "group_dense",
    (PyCFunction)__pythran_wrapall_group_dense,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - group_dense(int, int, int[:,:])\n""    - group_dense(int, int, int32[:,:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_group_columns",            /* m_name */
    "\n""Pythran implementation of columns grouping for finite difference Jacobian\n""estimation. Used by ._numdiff.group_columns and based on the Cython version.\n""",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_group_columns)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_group_columns)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_group_columns",
                                         Methods,
                                         "\n""Pythran implementation of columns grouping for finite difference Jacobian\n""estimation. Used by ._numdiff.group_columns and based on the Cython version.\n"""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.10.0",
                                      "2022-01-19 17:24:56.024983",
                                      "bbd9c32ae0cc40f86da54c6bc74a72b8cc51ed42efd9d0a4f45d3648fc5482c3");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif