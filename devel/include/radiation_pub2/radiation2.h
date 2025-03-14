// Generated by gencpp from file radiation_pub2/radiation2.msg
// DO NOT EDIT!


#ifndef RADIATION_PUB2_MESSAGE_RADIATION2_H
#define RADIATION_PUB2_MESSAGE_RADIATION2_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace radiation_pub2
{
template <class ContainerAllocator>
struct radiation2_
{
  typedef radiation2_<ContainerAllocator> Type;

  radiation2_()
    : radiation2()  {
    }
  radiation2_(const ContainerAllocator& _alloc)
    : radiation2(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> _radiation2_type;
  _radiation2_type radiation2;





  typedef boost::shared_ptr< ::radiation_pub2::radiation2_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::radiation_pub2::radiation2_<ContainerAllocator> const> ConstPtr;

}; // struct radiation2_

typedef ::radiation_pub2::radiation2_<std::allocator<void> > radiation2;

typedef boost::shared_ptr< ::radiation_pub2::radiation2 > radiation2Ptr;
typedef boost::shared_ptr< ::radiation_pub2::radiation2 const> radiation2ConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::radiation_pub2::radiation2_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::radiation_pub2::radiation2_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::radiation_pub2::radiation2_<ContainerAllocator1> & lhs, const ::radiation_pub2::radiation2_<ContainerAllocator2> & rhs)
{
  return lhs.radiation2 == rhs.radiation2;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::radiation_pub2::radiation2_<ContainerAllocator1> & lhs, const ::radiation_pub2::radiation2_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace radiation_pub2

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::radiation_pub2::radiation2_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::radiation_pub2::radiation2_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::radiation_pub2::radiation2_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::radiation_pub2::radiation2_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::radiation_pub2::radiation2_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::radiation_pub2::radiation2_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::radiation_pub2::radiation2_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9a7d2ef45bfc6a980a446dc09330c970";
  }

  static const char* value(const ::radiation_pub2::radiation2_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9a7d2ef45bfc6a98ULL;
  static const uint64_t static_value2 = 0x0a446dc09330c970ULL;
};

template<class ContainerAllocator>
struct DataType< ::radiation_pub2::radiation2_<ContainerAllocator> >
{
  static const char* value()
  {
    return "radiation_pub2/radiation2";
  }

  static const char* value(const ::radiation_pub2::radiation2_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::radiation_pub2::radiation2_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64[] radiation2\n"
;
  }

  static const char* value(const ::radiation_pub2::radiation2_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::radiation_pub2::radiation2_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.radiation2);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct radiation2_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::radiation_pub2::radiation2_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::radiation_pub2::radiation2_<ContainerAllocator>& v)
  {
    s << indent << "radiation2[]" << std::endl;
    for (size_t i = 0; i < v.radiation2.size(); ++i)
    {
      s << indent << "  radiation2[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.radiation2[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // RADIATION_PUB2_MESSAGE_RADIATION2_H
