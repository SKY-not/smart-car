; Auto-generated. Do not edit!


(cl:in-package radiation_pub2-msg)


;//! \htmlinclude radiation2.msg.html

(cl:defclass <radiation2> (roslisp-msg-protocol:ros-message)
  ((radiation2
    :reader radiation2
    :initarg :radiation2
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass radiation2 (<radiation2>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <radiation2>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'radiation2)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name radiation_pub2-msg:<radiation2> is deprecated: use radiation_pub2-msg:radiation2 instead.")))

(cl:ensure-generic-function 'radiation2-val :lambda-list '(m))
(cl:defmethod radiation2-val ((m <radiation2>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader radiation_pub2-msg:radiation2-val is deprecated.  Use radiation_pub2-msg:radiation2 instead.")
  (radiation2 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <radiation2>) ostream)
  "Serializes a message object of type '<radiation2>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'radiation2))))
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
   (cl:slot-value msg 'radiation2))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <radiation2>) istream)
  "Deserializes a message object of type '<radiation2>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'radiation2) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'radiation2)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<radiation2>)))
  "Returns string type for a message object of type '<radiation2>"
  "radiation_pub2/radiation2")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'radiation2)))
  "Returns string type for a message object of type 'radiation2"
  "radiation_pub2/radiation2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<radiation2>)))
  "Returns md5sum for a message object of type '<radiation2>"
  "9a7d2ef45bfc6a980a446dc09330c970")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'radiation2)))
  "Returns md5sum for a message object of type 'radiation2"
  "9a7d2ef45bfc6a980a446dc09330c970")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<radiation2>)))
  "Returns full string definition for message of type '<radiation2>"
  (cl:format cl:nil "float64[] radiation2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'radiation2)))
  "Returns full string definition for message of type 'radiation2"
  (cl:format cl:nil "float64[] radiation2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <radiation2>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'radiation2) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <radiation2>))
  "Converts a ROS message object to a list"
  (cl:list 'radiation2
    (cl:cons ':radiation2 (radiation2 msg))
))
