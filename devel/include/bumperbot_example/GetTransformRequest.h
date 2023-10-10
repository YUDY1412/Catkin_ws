// Generated by gencpp from file bumperbot_example/GetTransformRequest.msg
// DO NOT EDIT!


#ifndef BUMPERBOT_EXAMPLE_MESSAGE_GETTRANSFORMREQUEST_H
#define BUMPERBOT_EXAMPLE_MESSAGE_GETTRANSFORMREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace bumperbot_example
{
template <class ContainerAllocator>
struct GetTransformRequest_
{
  typedef GetTransformRequest_<ContainerAllocator> Type;

  GetTransformRequest_()
    : frame_id()
    , child_frame_id()  {
    }
  GetTransformRequest_(const ContainerAllocator& _alloc)
    : frame_id(_alloc)
    , child_frame_id(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _frame_id_type;
  _frame_id_type frame_id;

   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _child_frame_id_type;
  _child_frame_id_type child_frame_id;





  typedef boost::shared_ptr< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> const> ConstPtr;

}; // struct GetTransformRequest_

typedef ::bumperbot_example::GetTransformRequest_<std::allocator<void> > GetTransformRequest;

typedef boost::shared_ptr< ::bumperbot_example::GetTransformRequest > GetTransformRequestPtr;
typedef boost::shared_ptr< ::bumperbot_example::GetTransformRequest const> GetTransformRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::bumperbot_example::GetTransformRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::bumperbot_example::GetTransformRequest_<ContainerAllocator1> & lhs, const ::bumperbot_example::GetTransformRequest_<ContainerAllocator2> & rhs)
{
  return lhs.frame_id == rhs.frame_id &&
    lhs.child_frame_id == rhs.child_frame_id;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::bumperbot_example::GetTransformRequest_<ContainerAllocator1> & lhs, const ::bumperbot_example::GetTransformRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace bumperbot_example

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "366795225b50a63c28fbb7c3a9653ed1";
  }

  static const char* value(const ::bumperbot_example::GetTransformRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x366795225b50a63cULL;
  static const uint64_t static_value2 = 0x28fbb7c3a9653ed1ULL;
};

template<class ContainerAllocator>
struct DataType< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bumperbot_example/GetTransformRequest";
  }

  static const char* value(const ::bumperbot_example::GetTransformRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "#Request\n"
"string frame_id\n"
"string child_frame_id\n"
;
  }

  static const char* value(const ::bumperbot_example::GetTransformRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.frame_id);
      stream.next(m.child_frame_id);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetTransformRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::bumperbot_example::GetTransformRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::bumperbot_example::GetTransformRequest_<ContainerAllocator>& v)
  {
    s << indent << "frame_id: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.frame_id);
    s << indent << "child_frame_id: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.child_frame_id);
  }
};

} // namespace message_operations
} // namespace ros

#endif // BUMPERBOT_EXAMPLE_MESSAGE_GETTRANSFORMREQUEST_H
