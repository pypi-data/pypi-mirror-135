#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int64.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/int64.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/max.hpp>
#include <pythonic/include/builtins/min.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/ceil.hpp>
#include <pythonic/include/numpy/float64.hpp>
#include <pythonic/include/numpy/floor.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/le.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/max.hpp>
#include <pythonic/builtins/min.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/ceil.hpp>
#include <pythonic/numpy/float64.hpp>
#include <pythonic/numpy/floor.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/le.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__hypotests_pythran
{
  struct _compute_outer_prob_inside_method
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef double __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type4;
      typedef long __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ceil{})>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type8;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type9;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>::type __type10;
      typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type10>(), std::declval<__type9>()))>::type __type12;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type12>::type>::type>::type __type13;
      typedef typename __combined<__type9,__type13>::type __type14;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type15;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type14>(), std::declval<__type15>()))>::type __type16;
      typedef decltype(pythonic::operator_::div(std::declval<__type8>(), std::declval<__type16>())) __type17;
      typedef decltype(std::declval<__type7>()(std::declval<__type17>())) __type18;
      typedef decltype(std::declval<__type6>()(std::declval<__type18>())) __type19;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type12>::type>::type>::type __type21;
      typedef typename __combined<__type10,__type21>::type __type22;
      typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type5>())) __type23;
      typedef decltype(std::declval<__type4>()(std::declval<__type19>(), std::declval<__type23>())) __type24;
      typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type24>()))>::type __type25;
      typedef std::integral_constant<long,0> __type26;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type25>::type>::type __type28;
      typedef indexable_container<__type26, typename std::remove_reference<__type28>::type> __type29;
      typedef typename __combined<__type25,__type29>::type __type30;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type30>::type>::type>::type __type31;
      typedef decltype(pythonic::operator_::mul(std::declval<__type5>(), std::declval<__type31>())) __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type32>(), std::declval<__type5>())) __type33;
      typedef decltype(std::declval<__type4>()(std::declval<__type33>(), std::declval<__type23>())) __type36;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type37;
      typedef typename pythonic::assignable<decltype(std::declval<__type3>()(std::declval<__type36>(), std::declval<__type37>()))>::type __type38;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type39;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type22>(), std::declval<__type15>()))>::type __type43;
      typedef decltype(pythonic::operator_::add(std::declval<__type14>(), std::declval<__type5>())) __type45;
      typedef decltype(std::declval<__type39>()(std::declval<__type5>(), std::declval<__type45>())) __type46;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type46>::type::iterator>::value_type>::type __type47;
      typedef decltype(pythonic::operator_::mul(std::declval<__type43>(), std::declval<__type47>())) __type48;
      typedef decltype(pythonic::operator_::add(std::declval<__type48>(), std::declval<__type8>())) __type50;
      typedef decltype(pythonic::operator_::div(std::declval<__type50>(), std::declval<__type16>())) __type52;
      typedef decltype(std::declval<__type7>()(std::declval<__type52>())) __type53;
      typedef decltype(std::declval<__type6>()(std::declval<__type53>())) __type54;
      typedef typename pythonic::assignable<decltype(std::declval<__type4>()(std::declval<__type54>(), std::declval<__type23>()))>::type __type57;
      typedef typename __combined<__type31,__type57>::type __type58;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type25>::type>::type>::type __type59;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::sub(std::declval<__type31>(), std::declval<__type59>()))>::type __type63;
      typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type59>(), std::declval<__type63>()))>::type __type64;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type64>::type>::type __type65;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type66;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::floor{})>::type>::type __type67;
      typedef decltype(pythonic::operator_::sub(std::declval<__type48>(), std::declval<__type8>())) __type72;
      typedef decltype(pythonic::operator_::div(std::declval<__type72>(), std::declval<__type16>())) __type74;
      typedef decltype(std::declval<__type67>()(std::declval<__type74>())) __type75;
      typedef decltype(std::declval<__type6>()(std::declval<__type75>())) __type76;
      typedef decltype(pythonic::operator_::add(std::declval<__type76>(), std::declval<__type5>())) __type77;
      typedef typename __combined<__type77,__type5>::type __type78;
      typedef decltype(std::declval<__type66>()(std::declval<__type78>(), std::declval<__type5>())) __type79;
      typedef decltype(std::declval<__type4>()(std::declval<__type79>(), std::declval<__type22>())) __type81;
      typedef typename pythonic::assignable<typename __combined<__type65,__type81>::type>::type __type82;
      typedef typename __combined<__type59,__type82>::type __type83;
      typedef decltype(pythonic::operator_::sub(std::declval<__type58>(), std::declval<__type83>())) __type84;
      typedef decltype(std::declval<__type39>()(std::declval<__type84>())) __type85;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type85>::type::iterator>::value_type>::type __type86;
      typedef indexable<__type86> __type87;
      typedef typename __combined<__type38,__type87>::type __type88;
      typedef typename pythonic::assignable<double>::type __type89;
      typedef typename __combined<__type38,__type2>::type __type90;
      typedef decltype(pythonic::operator_::add(std::declval<__type86>(), std::declval<__type83>())) __type93;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type64>::type>::type>::type __type94;
      typedef decltype(pythonic::operator_::sub(std::declval<__type93>(), std::declval<__type94>())) __type95;
      typedef decltype(std::declval<__type90>()[std::declval<__type95>()]) __type96;
      typedef decltype(pythonic::operator_::mul(std::declval<__type96>(), std::declval<__type47>())) __type98;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type86>(), std::declval<__type83>()))>::type __type102;
      typedef decltype(pythonic::operator_::mul(std::declval<__type89>(), std::declval<__type102>())) __type103;
      typedef decltype(pythonic::operator_::add(std::declval<__type98>(), std::declval<__type103>())) __type104;
      typedef decltype(pythonic::operator_::add(std::declval<__type47>(), std::declval<__type102>())) __type107;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type104>(), std::declval<__type107>()))>::type __type108;
      typedef typename __combined<__type89,__type108>::type __type109;
      typedef container<typename std::remove_reference<__type109>::type> __type110;
      typedef typename __combined<__type88,__type2,__type110,__type87,__type5>::type __type111;
      typedef decltype(pythonic::operator_::sub(std::declval<__type84>(), std::declval<__type5>())) __type115;
      typedef decltype(std::declval<__type111>()[std::declval<__type115>()]) __type116;
      typedef __type0 __ptype0;
      typedef __type1 __ptype1;
      typedef typename pythonic::returnable<typename __combined<__type2,__type116>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& m, argument_type1&& n, argument_type2&& g, argument_type3&& h) const
    ;
  }  ;
  struct _a_ij_Aij_Dij2
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::assignable<long>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type4;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type0>())) __type6;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
      typedef typename pythonic::lazy<__type7>::type __type8;
      typedef decltype(std::declval<__type4>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type11;
      typedef typename pythonic::lazy<__type11>::type __type12;
      typedef decltype(std::declval<__type4>()(std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type10>(), std::declval<__type14>())) __type15;
      typedef decltype(std::declval<__type0>()[std::declval<__type15>()]) __type16;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type17;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type18;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type19;
      typedef typename __combined<__type19,__type0>::type __type20;
      typedef pythonic::types::contiguous_slice __type21;
      typedef decltype(std::declval<__type20>()(std::declval<__type21>(), std::declval<__type21>())) __type22;
      typedef decltype(std::declval<__type18>()(std::declval<__type22>())) __type23;
      typedef decltype(pythonic::operator_::add(std::declval<__type23>(), std::declval<__type23>())) __type26;
      typedef typename pythonic::assignable<typename __combined<__type0,__type0>::type>::type __type27;
      typedef decltype(std::declval<__type27>()(std::declval<__type21>(), std::declval<__type21>())) __type28;
      typedef decltype(std::declval<__type18>()(std::declval<__type28>())) __type29;
      typedef decltype(pythonic::operator_::add(std::declval<__type29>(), std::declval<__type29>())) __type32;
      typedef decltype(pythonic::operator_::sub(std::declval<__type26>(), std::declval<__type32>())) __type33;
      typedef decltype(std::declval<__type17>()(std::declval<__type33>())) __type34;
      typedef decltype(pythonic::operator_::mul(std::declval<__type16>(), std::declval<__type34>())) __type35;
      typedef decltype(pythonic::operator_::add(std::declval<__type2>(), std::declval<__type35>())) __type36;
      typedef typename __combined<__type2,__type36>::type __type37;
      typedef __type0 __ptype4;
      typedef __type0 __ptype5;
      typedef typename pythonic::returnable<typename __combined<__type37,__type35>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& A) const
    ;
  }  ;
  struct _Q
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::assignable<long>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type0>())) __type5;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type5>::type>::type __type6;
      typedef typename pythonic::lazy<__type6>::type __type7;
      typedef decltype(std::declval<__type3>()(std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type __type9;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type5>::type>::type __type10;
      typedef typename pythonic::lazy<__type10>::type __type11;
      typedef decltype(std::declval<__type3>()(std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type13>())) __type14;
      typedef decltype(std::declval<__type0>()[std::declval<__type14>()]) __type15;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type16;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type17;
      typedef pythonic::types::contiguous_slice __type18;
      typedef decltype(std::declval<__type17>()(std::declval<__type18>(), std::declval<__type18>())) __type19;
      typedef decltype(std::declval<__type16>()(std::declval<__type19>())) __type20;
      typedef decltype(pythonic::operator_::add(std::declval<__type20>(), std::declval<__type20>())) __type23;
      typedef decltype(pythonic::operator_::mul(std::declval<__type15>(), std::declval<__type23>())) __type24;
      typedef decltype(pythonic::operator_::add(std::declval<__type1>(), std::declval<__type24>())) __type25;
      typedef typename __combined<__type1,__type25>::type __type26;
      typedef __type0 __ptype6;
      typedef typename pythonic::returnable<typename __combined<__type26,__type24>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& A) const
    ;
  }  ;
  struct _P
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::assignable<long>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type0>())) __type5;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type5>::type>::type __type6;
      typedef typename pythonic::lazy<__type6>::type __type7;
      typedef decltype(std::declval<__type3>()(std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type __type9;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type5>::type>::type __type10;
      typedef typename pythonic::lazy<__type10>::type __type11;
      typedef decltype(std::declval<__type3>()(std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type9>(), std::declval<__type13>())) __type14;
      typedef decltype(std::declval<__type0>()[std::declval<__type14>()]) __type15;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type16;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type17;
      typedef pythonic::types::contiguous_slice __type18;
      typedef decltype(std::declval<__type17>()(std::declval<__type18>(), std::declval<__type18>())) __type19;
      typedef decltype(std::declval<__type16>()(std::declval<__type19>())) __type20;
      typedef decltype(pythonic::operator_::add(std::declval<__type20>(), std::declval<__type20>())) __type23;
      typedef decltype(pythonic::operator_::mul(std::declval<__type15>(), std::declval<__type23>())) __type24;
      typedef decltype(pythonic::operator_::add(std::declval<__type1>(), std::declval<__type24>())) __type25;
      typedef typename __combined<__type1,__type25>::type __type26;
      typedef __type0 __ptype7;
      typedef typename pythonic::returnable<typename __combined<__type26,__type24>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    inline
    typename type<argument_type0>::result_type operator()(argument_type0&& A) const
    ;
  }  ;
  struct _Dij
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef pythonic::types::contiguous_slice __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>(), std::declval<__type2>())) __type3;
      typedef decltype(std::declval<__type0>()(std::declval<__type3>())) __type4;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type4>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
    ;
  }  ;
  struct _Aij
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef pythonic::types::contiguous_slice __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>(), std::declval<__type2>())) __type3;
      typedef decltype(std::declval<__type0>()(std::declval<__type3>())) __type4;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type4>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  inline
  typename _compute_outer_prob_inside_method::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type _compute_outer_prob_inside_method::operator()(argument_type0&& m, argument_type1&& n, argument_type2&& g, argument_type3&& h) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>::type __type0;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type2;
    typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type0>(), std::declval<__type2>()))>::type __type4;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type>::type __type5;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type>::type __type6;
    typedef long __type7;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type8;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type9;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ceil{})>::type>::type __type10;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type11;
    typedef typename __combined<__type2,__type5>::type __type12;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type13;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type12>(), std::declval<__type13>()))>::type __type14;
    typedef decltype(pythonic::operator_::div(std::declval<__type11>(), std::declval<__type14>())) __type15;
    typedef decltype(std::declval<__type10>()(std::declval<__type15>())) __type16;
    typedef decltype(std::declval<__type9>()(std::declval<__type16>())) __type17;
    typedef typename __combined<__type0,__type6>::type __type18;
    typedef decltype(pythonic::operator_::add(std::declval<__type18>(), std::declval<__type7>())) __type19;
    typedef decltype(std::declval<__type8>()(std::declval<__type17>(), std::declval<__type19>())) __type20;
    typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type20>()))>::type __type21;
    typedef std::integral_constant<long,0> __type22;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type21>::type>::type __type24;
    typedef indexable_container<__type22, typename std::remove_reference<__type24>::type> __type25;
    typedef std::integral_constant<long,1> __type26;
    typedef typename __combined<__type21,__type25>::type __type27;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type27>::type>::type __type28;
    typedef indexable_container<__type26, typename std::remove_reference<__type28>::type> __type29;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type21>::type>::type>::type __type30;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type27>::type>::type>::type __type32;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type18>(), std::declval<__type13>()))>::type __type35;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type36;
    typedef decltype(pythonic::operator_::add(std::declval<__type12>(), std::declval<__type7>())) __type38;
    typedef decltype(std::declval<__type36>()(std::declval<__type7>(), std::declval<__type38>())) __type39;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type39>::type::iterator>::value_type>::type __type40;
    typedef decltype(pythonic::operator_::mul(std::declval<__type35>(), std::declval<__type40>())) __type41;
    typedef decltype(pythonic::operator_::add(std::declval<__type41>(), std::declval<__type11>())) __type43;
    typedef decltype(pythonic::operator_::div(std::declval<__type43>(), std::declval<__type14>())) __type45;
    typedef decltype(std::declval<__type10>()(std::declval<__type45>())) __type46;
    typedef decltype(std::declval<__type9>()(std::declval<__type46>())) __type47;
    typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type47>(), std::declval<__type19>()))>::type __type50;
    typedef typename __combined<__type32,__type50>::type __type51;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::sub(std::declval<__type51>(), std::declval<__type30>()))>::type __type53;
    typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type30>(), std::declval<__type53>()))>::type __type54;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type54>::type>::type __type55;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type56;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::floor{})>::type>::type __type57;
    typedef decltype(pythonic::operator_::sub(std::declval<__type41>(), std::declval<__type11>())) __type62;
    typedef decltype(pythonic::operator_::div(std::declval<__type62>(), std::declval<__type14>())) __type64;
    typedef decltype(std::declval<__type57>()(std::declval<__type64>())) __type65;
    typedef decltype(std::declval<__type9>()(std::declval<__type65>())) __type66;
    typedef decltype(pythonic::operator_::add(std::declval<__type66>(), std::declval<__type7>())) __type67;
    typedef typename __combined<__type67,__type7>::type __type68;
    typedef decltype(std::declval<__type56>()(std::declval<__type68>(), std::declval<__type7>())) __type69;
    typedef decltype(std::declval<__type8>()(std::declval<__type69>(), std::declval<__type18>())) __type71;
    typedef typename pythonic::assignable<typename __combined<__type55,__type71>::type>::type __type72;
    typedef typename __combined<__type30,__type72>::type __type75;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::sub(std::declval<__type51>(), std::declval<__type75>()))>::type __type76;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type __type77;
    typedef decltype(pythonic::operator_::mul(std::declval<__type7>(), std::declval<__type51>())) __type79;
    typedef decltype(pythonic::operator_::add(std::declval<__type79>(), std::declval<__type7>())) __type80;
    typedef decltype(std::declval<__type8>()(std::declval<__type80>(), std::declval<__type19>())) __type83;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type84;
    typedef typename pythonic::assignable<decltype(std::declval<__type77>()(std::declval<__type83>(), std::declval<__type84>()))>::type __type85;
    typedef decltype(pythonic::operator_::sub(std::declval<__type51>(), std::declval<__type75>())) __type88;
    typedef decltype(std::declval<__type36>()(std::declval<__type88>())) __type89;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type89>::type::iterator>::value_type>::type __type90;
    typedef indexable<__type90> __type91;
    typedef typename __combined<__type85,__type91>::type __type92;
    typedef double __type93;
    typedef typename pythonic::assignable<double>::type __type94;
    typedef typename __combined<__type85,__type93>::type __type95;
    typedef decltype(pythonic::operator_::add(std::declval<__type90>(), std::declval<__type75>())) __type98;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type54>::type>::type>::type __type99;
    typedef decltype(pythonic::operator_::sub(std::declval<__type98>(), std::declval<__type99>())) __type100;
    typedef decltype(std::declval<__type95>()[std::declval<__type100>()]) __type101;
    typedef decltype(pythonic::operator_::mul(std::declval<__type101>(), std::declval<__type40>())) __type103;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type90>(), std::declval<__type75>()))>::type __type107;
    typedef decltype(pythonic::operator_::mul(std::declval<__type94>(), std::declval<__type107>())) __type108;
    typedef decltype(pythonic::operator_::add(std::declval<__type103>(), std::declval<__type108>())) __type109;
    typedef decltype(pythonic::operator_::add(std::declval<__type40>(), std::declval<__type107>())) __type112;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type109>(), std::declval<__type112>()))>::type __type113;
    typedef typename __combined<__type94,__type113>::type __type114;
    typedef container<typename std::remove_reference<__type114>::type> __type115;
    typename pythonic::assignable<typename __combined<__type0,__type6>::type>::type n_ = n;
    typename pythonic::assignable<typename __combined<__type2,__type5>::type>::type m_ = m;
    if (pythonic::operator_::lt(m_, n_))
    {
      typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(n_, m_))>::type __tuple0 = pythonic::types::make_tuple(n_, m_);
      m_ = std::get<0>(__tuple0);
      n_ = std::get<1>(__tuple0);
    }
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(m_, g))>::type mg = pythonic::operator_::functor::floordiv()(m_, g);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(n_, g))>::type ng = pythonic::operator_::functor::floordiv()(n_, g);
    typename pythonic::assignable<typename __combined<__type21,__type25,__type29>::type>::type __tuple1 = pythonic::types::make_tuple(0L, pythonic::builtins::functor::min{}(pythonic::builtins::functor::int_{}(pythonic::numpy::functor::ceil{}(pythonic::operator_::div(h, mg))), pythonic::operator_::add(n_, 1L)));
    typename pythonic::assignable<typename __combined<__type30,__type72>::type>::type minj = std::get<0>(__tuple1);
    typename pythonic::assignable<typename __combined<__type32,__type50>::type>::type maxj = std::get<1>(__tuple1);
    typename pythonic::assignable<typename __combined<__type53,__type76>::type>::type curlen = pythonic::operator_::sub(maxj, minj);
    typename pythonic::assignable<typename __combined<__type92,__type93,__type115,__type91,__type7>::type>::type A = pythonic::numpy::functor::ones{}(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::mul(2L, maxj), 2L), pythonic::operator_::add(n_, 1L)), pythonic::numpy::functor::float64{});
    A[pythonic::types::contiguous_slice(minj,maxj)] = 0.0;
    {
      long  __target140098692588256 = pythonic::operator_::add(m_, 1L);
      for (long  i=1L; i < __target140098692588256; i += 1L)
      {
        typename pythonic::assignable_noescape<decltype(pythonic::types::make_tuple(minj, curlen))>::type __tuple2 = pythonic::types::make_tuple(minj, curlen);
        typename pythonic::assignable_noescape<decltype(std::get<0>(__tuple2))>::type lastminj = std::get<0>(__tuple2);
        minj = pythonic::builtins::functor::min{}(pythonic::builtins::functor::max{}(pythonic::operator_::add(pythonic::builtins::functor::int_{}(pythonic::numpy::functor::floor{}(pythonic::operator_::div(pythonic::operator_::sub(pythonic::operator_::mul(ng, i), h), mg))), 1L), 0L), n_);
        maxj = pythonic::builtins::functor::min{}(pythonic::builtins::functor::int_{}(pythonic::numpy::functor::ceil{}(pythonic::operator_::div(pythonic::operator_::add(pythonic::operator_::mul(ng, i), h), mg))), pythonic::operator_::add(n_, 1L));
        {
          typename pythonic::assignable<typename __combined<__type94,__type113>::type>::type val;
          if (pythonic::operator_::le(maxj, minj))
          {
            return 1.0;
          }
          else
          {
            val = (((bool)pythonic::operator_::eq(minj, 0L)) ? typename __combined<decltype(0.0), decltype(1.0)>::type(0.0) : typename __combined<decltype(0.0), decltype(1.0)>::type(1.0));
            {
              long  __target140098689242256 = pythonic::operator_::sub(maxj, minj);
              for (long  jj=0L; jj < __target140098689242256; jj += 1L)
              {
                typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(jj, minj))>::type j = pythonic::operator_::add(jj, minj);
                val = pythonic::operator_::div(pythonic::operator_::add(pythonic::operator_::mul(A[pythonic::operator_::sub(pythonic::operator_::add(jj, minj), lastminj)], i), pythonic::operator_::mul(val, j)), pythonic::operator_::add(i, j));
                A[jj] = val;
              }
            }
            curlen = pythonic::operator_::sub(maxj, minj);
            if (pythonic::operator_::gt(std::get<1>(__tuple2), curlen))
            {
              A[pythonic::types::contiguous_slice(pythonic::operator_::sub(maxj, minj),pythonic::operator_::add(pythonic::operator_::sub(maxj, minj), pythonic::operator_::sub(std::get<1>(__tuple2), curlen)))] = 1L;
            }
          }
        }
      }
    }
    return A[pythonic::operator_::sub(pythonic::operator_::sub(maxj, minj), 1L)];
  }
  template <typename argument_type0 >
  inline
  typename _a_ij_Aij_Dij2::type<argument_type0>::result_type _a_ij_Aij_Dij2::operator()(argument_type0&& A) const
  {
    typedef typename pythonic::assignable<long>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type2;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type4;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
    typedef typename pythonic::lazy<__type5>::type __type6;
    typedef decltype(std::declval<__type2>()(std::declval<__type6>())) __type7;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type2>()(std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type12>())) __type13;
    typedef decltype(std::declval<__type1>()[std::declval<__type13>()]) __type14;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type15;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type16;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type17;
    typedef typename __combined<__type17,__type1>::type __type19;
    typedef pythonic::types::contiguous_slice __type20;
    typedef decltype(std::declval<__type19>()(std::declval<__type20>(), std::declval<__type20>())) __type21;
    typedef decltype(std::declval<__type16>()(std::declval<__type21>())) __type22;
    typedef decltype(pythonic::operator_::add(std::declval<__type22>(), std::declval<__type22>())) __type25;
    typedef typename pythonic::assignable<typename __combined<__type1,__type1>::type>::type __type27;
    typedef decltype(std::declval<__type27>()(std::declval<__type20>(), std::declval<__type20>())) __type28;
    typedef decltype(std::declval<__type16>()(std::declval<__type28>())) __type29;
    typedef decltype(pythonic::operator_::add(std::declval<__type29>(), std::declval<__type29>())) __type32;
    typedef decltype(pythonic::operator_::sub(std::declval<__type25>(), std::declval<__type32>())) __type33;
    typedef decltype(std::declval<__type15>()(std::declval<__type33>())) __type34;
    typedef decltype(pythonic::operator_::mul(std::declval<__type14>(), std::declval<__type34>())) __type35;
    typedef decltype(pythonic::operator_::add(std::declval<__type0>(), std::declval<__type35>())) __type36;
    typedef typename __combined<__type0,__type36>::type __type37;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type m = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type n = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::assignable<typename __combined<__type37,__type35>::type>::type count = 0L;
    {
      long  __target140098692575440 = m;
      for (long  i=0L; i < __target140098692575440; i += 1L)
      {
        {
          long  __target140098692412992 = n;
          for (long  j=0L; j < __target140098692412992; j += 1L)
          {
            typename pythonic::assignable<typename __combined<__type17,__type1>::type>::type __pythran_inline_AijA2 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Aiji2 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Aijj2 = j;
            typename pythonic::assignable<typename pythonic::assignable<typename __combined<__type1,__type1>::type>::type>::type __pythran_inline_DijA3 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Diji3 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Dijj3 = j;
            count += pythonic::operator_::mul(A.fast(pythonic::types::make_tuple(i, j)), pythonic::numpy::functor::square{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_AijA2(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aiji2),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aijj2))), pythonic::numpy::functor::sum{}(__pythran_inline_AijA2(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aiji2, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aijj2, 1L),pythonic::builtins::None)))), pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_DijA3(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Diji3, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Dijj3))), pythonic::numpy::functor::sum{}(__pythran_inline_DijA3(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Diji3),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Dijj3, 1L),pythonic::builtins::None)))))));
          }
        }
      }
    }
    return count;
  }
  template <typename argument_type0 >
  inline
  typename _Q::type<argument_type0>::result_type _Q::operator()(argument_type0&& A) const
  {
    typedef typename pythonic::assignable<long>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type2;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type4;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
    typedef typename pythonic::lazy<__type5>::type __type6;
    typedef decltype(std::declval<__type2>()(std::declval<__type6>())) __type7;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type2>()(std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type12>())) __type13;
    typedef decltype(std::declval<__type1>()[std::declval<__type13>()]) __type14;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type15;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type16;
    typedef pythonic::types::contiguous_slice __type17;
    typedef decltype(std::declval<__type16>()(std::declval<__type17>(), std::declval<__type17>())) __type18;
    typedef decltype(std::declval<__type15>()(std::declval<__type18>())) __type19;
    typedef decltype(pythonic::operator_::add(std::declval<__type19>(), std::declval<__type19>())) __type22;
    typedef decltype(pythonic::operator_::mul(std::declval<__type14>(), std::declval<__type22>())) __type23;
    typedef decltype(pythonic::operator_::add(std::declval<__type0>(), std::declval<__type23>())) __type24;
    typedef typename __combined<__type0,__type24>::type __type25;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type m = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type n = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::assignable<typename __combined<__type25,__type23>::type>::type count = 0L;
    {
      long  __target140098692578608 = m;
      for (long  i=0L; i < __target140098692578608; i += 1L)
      {
        {
          long  __target140098692576880 = n;
          for (long  j=0L; j < __target140098692576880; j += 1L)
          {
            typename pythonic::assignable_noescape<decltype(A)>::type __pythran_inline_DijA1 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Diji1 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Dijj1 = j;
            count += pythonic::operator_::mul(A.fast(pythonic::types::make_tuple(i, j)), pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_DijA1(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Diji1, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Dijj1))), pythonic::numpy::functor::sum{}(__pythran_inline_DijA1(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Diji1),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Dijj1, 1L),pythonic::builtins::None)))));
          }
        }
      }
    }
    return count;
  }
  template <typename argument_type0 >
  inline
  typename _P::type<argument_type0>::result_type _P::operator()(argument_type0&& A) const
  {
    typedef typename pythonic::assignable<long>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type2;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type4;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
    typedef typename pythonic::lazy<__type5>::type __type6;
    typedef decltype(std::declval<__type2>()(std::declval<__type6>())) __type7;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type2>()(std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type12>())) __type13;
    typedef decltype(std::declval<__type1>()[std::declval<__type13>()]) __type14;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type15;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type16;
    typedef pythonic::types::contiguous_slice __type17;
    typedef decltype(std::declval<__type16>()(std::declval<__type17>(), std::declval<__type17>())) __type18;
    typedef decltype(std::declval<__type15>()(std::declval<__type18>())) __type19;
    typedef decltype(pythonic::operator_::add(std::declval<__type19>(), std::declval<__type19>())) __type22;
    typedef decltype(pythonic::operator_::mul(std::declval<__type14>(), std::declval<__type22>())) __type23;
    typedef decltype(pythonic::operator_::add(std::declval<__type0>(), std::declval<__type23>())) __type24;
    typedef typename __combined<__type0,__type24>::type __type25;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type m = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A)))>::type n = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, A));
    typename pythonic::assignable<typename __combined<__type25,__type23>::type>::type count = 0L;
    {
      long  __target140098692679424 = m;
      for (long  i=0L; i < __target140098692679424; i += 1L)
      {
        {
          long  __target140098692390576 = n;
          for (long  j=0L; j < __target140098692390576; j += 1L)
          {
            typename pythonic::assignable_noescape<decltype(A)>::type __pythran_inline_AijA0 = A;
            typename pythonic::assignable_noescape<decltype(i)>::type __pythran_inline_Aiji0 = i;
            typename pythonic::assignable_noescape<decltype(j)>::type __pythran_inline_Aijj0 = j;
            count += pythonic::operator_::mul(A.fast(pythonic::types::make_tuple(i, j)), pythonic::operator_::add(pythonic::numpy::functor::sum{}(__pythran_inline_AijA0(pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aiji0),pythonic::types::contiguous_slice(pythonic::builtins::None,__pythran_inline_Aijj0))), pythonic::numpy::functor::sum{}(__pythran_inline_AijA0(pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aiji0, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::operator_::add(__pythran_inline_Aijj0, 1L),pythonic::builtins::None)))));
          }
        }
      }
    }
    return count;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _Dij::type<argument_type0, argument_type1, argument_type2>::result_type _Dij::operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
  {
    return pythonic::operator_::add(pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::operator_::add(i, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,j))), pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::builtins::None,i),pythonic::types::contiguous_slice(pythonic::operator_::add(j, 1L),pythonic::builtins::None))));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _Aij::type<argument_type0, argument_type1, argument_type2>::result_type _Aij::operator()(argument_type0&& A, argument_type1&& i, argument_type2&& j) const
  {
    return pythonic::operator_::add(pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::builtins::None,i),pythonic::types::contiguous_slice(pythonic::builtins::None,j))), pythonic::numpy::functor::sum{}(A(pythonic::types::contiguous_slice(pythonic::operator_::add(i, 1L),pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::operator_::add(j, 1L),pythonic::builtins::None))));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__hypotests_pythran::_compute_outer_prob_inside_method::type<npy_int64, npy_int64, npy_int64, npy_int64>::result_type _compute_outer_prob_inside_method0(npy_int64&& m, npy_int64&& n, npy_int64&& g, npy_int64&& h) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_compute_outer_prob_inside_method()(m, n, g, h);
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
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _a_ij_Aij_Dij20(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
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
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _a_ij_Aij_Dij21(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
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
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _a_ij_Aij_Dij22(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
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
typename __pythran__hypotests_pythran::_a_ij_Aij_Dij2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _a_ij_Aij_Dij23(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_a_ij_Aij_Dij2()(A);
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
typename __pythran__hypotests_pythran::_Q::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _Q0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Q()(A);
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
typename __pythran__hypotests_pythran::_Q::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _Q1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Q()(A);
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
typename __pythran__hypotests_pythran::_Q::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _Q2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Q()(A);
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
typename __pythran__hypotests_pythran::_Q::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _Q3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Q()(A);
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
typename __pythran__hypotests_pythran::_P::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>::result_type _P0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_P()(A);
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
typename __pythran__hypotests_pythran::_P::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>::result_type _P1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_P()(A);
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
typename __pythran__hypotests_pythran::_P::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type _P2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_P()(A);
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
typename __pythran__hypotests_pythran::_P::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>::result_type _P3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_P()(A);
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
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, long, long>::result_type _Dij0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, long, long>::result_type _Dij1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long, long>::result_type _Dij2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Dij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long, long>::result_type _Dij3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Dij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>, long, long>::result_type _Aij0(pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>, long, long>::result_type _Aij1(pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long, long>::result_type _Aij2(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
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
typename __pythran__hypotests_pythran::_Aij::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long, long>::result_type _Aij3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& A, long&& i, long&& j) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hypotests_pythran::_Aij()(A, i, j);
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
__pythran_wrap__compute_outer_prob_inside_method0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    
    char const* keywords[] = {"m", "n", "g", "h",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<npy_int64>(args_obj[0]) && is_convertible<npy_int64>(args_obj[1]) && is_convertible<npy_int64>(args_obj[2]) && is_convertible<npy_int64>(args_obj[3]))
        return to_python(_compute_outer_prob_inside_method0(from_python<npy_int64>(args_obj[0]), from_python<npy_int64>(args_obj[1]), from_python<npy_int64>(args_obj[2]), from_python<npy_int64>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij20(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij20(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij21(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij21(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij22(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij22(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__a_ij_Aij_Dij23(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_a_ij_Aij_Dij23(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Q0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_Q0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Q1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_Q1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Q2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_Q2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Q3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_Q3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__P0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_P0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__P1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_P1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__P2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]))
        return to_python(_P2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__P3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    
    char const* keywords[] = {"A",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]))
        return to_python(_P3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Dij3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Dij3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij0(from_python<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<long,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__Aij3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"A", "i", "j",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(_Aij3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall__compute_outer_prob_inside_method(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__compute_outer_prob_inside_method0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_compute_outer_prob_inside_method", "\n""    - _compute_outer_prob_inside_method(int64, int64, int64, int64)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__a_ij_Aij_Dij2(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij20(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij21(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij22(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__a_ij_Aij_Dij23(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_a_ij_Aij_Dij2", "\n""    - _a_ij_Aij_Dij2(int[:,:])\n""    - _a_ij_Aij_Dij2(float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__Q(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__Q0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Q1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Q2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Q3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_Q", "\n""    - _Q(int[:,:])\n""    - _Q(float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__P(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__P0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__P1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__P2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__P3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_P", "\n""    - _P(int[:,:])\n""    - _P(float[:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__Dij(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__Dij0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Dij1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Dij2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Dij3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_Dij", "\n""    - _Dij(int[:,:], int, int)\n""    - _Dij(float[:,:], int, int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall__Aij(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__Aij0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Aij1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Aij2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__Aij3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_Aij", "\n""    - _Aij(int[:,:], int, int)\n""    - _Aij(float[:,:], int, int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "_compute_outer_prob_inside_method",
    (PyCFunction)__pythran_wrapall__compute_outer_prob_inside_method,
    METH_VARARGS | METH_KEYWORDS,
    "\n""Count the proportion of paths that do not stay strictly inside two\n""diagonal lines.\n""\n""Supported prototypes:\n""\n""- _compute_outer_prob_inside_method(int64, int64, int64, int64)\n""\n""Parameters\n""----------\n""m : integer\n""    m > 0\n""n : integer\n""    n > 0\n""g : integer\n""    g is greatest common divisor of m and n\n""h : integer\n""    0 <= h <= lcm(m,n)\n""\n""Returns\n""-------\n""p : float\n""    The proportion of paths that do not stay inside the two lines.\n""\n""The classical algorithm counts the integer lattice paths from (0, 0)\n""to (m, n) which satisfy |x/m - y/n| < h / lcm(m, n).\n""The paths make steps of size +1 in either positive x or positive y\n""directions.\n""We are, however, interested in 1 - proportion to computes p-values,\n""so we change the recursion to compute 1 - p directly while staying\n""within the \"inside method\" a described by Hodges.\n""\n""We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.\n""Hodges, J.L. Jr.,\n""\"The Significance Probability of the Smirnov Two-Sample Test,\"\n""Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.\n""\n""For the recursion for 1-p see\n""Viehmann, T.: \"Numerically more stable computation of the p-values\n""for the two-sample Kolmogorov-Smirnov test,\" arXiv: 2102.08037\n""\n"""},{
    "_a_ij_Aij_Dij2",
    (PyCFunction)__pythran_wrapall__a_ij_Aij_Dij2,
    METH_VARARGS | METH_KEYWORDS,
    "A term that appears in the ASE of Kendall's tau and Somers' D.\n""\n""    Supported prototypes:\n""\n""    - _a_ij_Aij_Dij2(int[:,:])\n""    - _a_ij_Aij_Dij2(float[:,:])"},{
    "_Q",
    (PyCFunction)__pythran_wrapall__Q,
    METH_VARARGS | METH_KEYWORDS,
    "Twice the number of discordant pairs, excluding ties.\n""\n""    Supported prototypes:\n""\n""    - _Q(int[:,:])\n""    - _Q(float[:,:])"},{
    "_P",
    (PyCFunction)__pythran_wrapall__P,
    METH_VARARGS | METH_KEYWORDS,
    "Twice the number of concordant pairs, excluding ties.\n""\n""    Supported prototypes:\n""\n""    - _P(int[:,:])\n""    - _P(float[:,:])"},{
    "_Dij",
    (PyCFunction)__pythran_wrapall__Dij,
    METH_VARARGS | METH_KEYWORDS,
    "Sum of lower-left and upper-right blocks of contingency table.\n""\n""    Supported prototypes:\n""\n""    - _Dij(int[:,:], int, int)\n""    - _Dij(float[:,:], int, int)"},{
    "_Aij",
    (PyCFunction)__pythran_wrapall__Aij,
    METH_VARARGS | METH_KEYWORDS,
    "Sum of upper-left and lower right blocks of contingency table.\n""\n""    Supported prototypes:\n""\n""    - _Aij(int[:,:], int, int)\n""    - _Aij(float[:,:], int, int)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_hypotests_pythran",            /* m_name */
    "",         /* m_doc */
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
PYTHRAN_MODULE_INIT(_hypotests_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_hypotests_pythran)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_hypotests_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.10.0",
                                      "2022-01-19 17:24:59.668760",
                                      "8a8a897c62326e8955a076d95a5044bdd7451daf1a5eb8acfd530567669b81e9");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif