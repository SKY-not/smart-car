; Auto-generated. Do not edit!


(cl:in-package radiation_pub_new-msg)


;//! \htmlinclude radiation.msg.html

(cl:defclass <radiation> (roslisp-msg-protocol:ros-message)
  ((radiation
    :reader radiation
    :initarg :radiation
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass radiation (<radiation>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <radiation>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'radiation)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name radiation_pub_new-msg:<radiation> is deprecated: use radiation_pub_new-msg:radiation instead.")))

(cl:ensure-generic-function 'radiation-val :lambda-list '(m))
(cl:defmethod radiation-val ((m <radiation>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader radiation_pub_new-msg:radiation-val is deprecated.  Use radiation_pub_new-msg:radiation instead.")
  (radiation m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <radiation>) ostream)
  "Serializes a message object of type '<radiation>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'radiation))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'radiation))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <radiation>) istream)
  "Deserializes a message object of type '<radiation>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'radiation) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'radiation)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<radiation>)))
  "Returns string type for a message object of type '<radiation>"
  "radiation_pub_new/radiation")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'radiation)))
  "Returns string type for a message object of type 'radiation"
  "radiation_pub_new/radiation")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<radiation>)))
  "Returns md5sum for a message object of type '<radiation>"
  "ae3ed639d310a116f0319906c7d3e096")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'radiation)))
  "Returns md5sum for a message object of type 'radiation"
  "ae3ed639d310a116f0319906c7d3e096")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<radiation>)))
  "Returns full string definition for message of type '<radiation>"
  (cl:format cl:nil "float64[] radiation~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'radiation)))
  "Returns full string definition for message of type 'radiation"
  (cl:format cl:nil "float64[] radiation~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <radiation>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'radiation) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <radiation>))
  "Converts a ROS message object to a list"
  (cl:list 'radiation
    (cl:cons ':radiation (radiation msg))
))
