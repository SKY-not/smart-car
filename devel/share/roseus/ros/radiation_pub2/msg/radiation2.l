;; Auto-generated. Do not edit!


(when (boundp 'radiation_pub2::radiation2)
  (if (not (find-package "RADIATION_PUB2"))
    (make-package "RADIATION_PUB2"))
  (shadow 'radiation2 (find-package "RADIATION_PUB2")))
(unless (find-package "RADIATION_PUB2::RADIATION2")
  (make-package "RADIATION_PUB2::RADIATION2"))

(in-package "ROS")
;;//! \htmlinclude radiation2.msg.html


(defclass radiation_pub2::radiation2
  :super ros::object
  :slots (_radiation2 ))

(defmethod radiation_pub2::radiation2
  (:init
   (&key
    ((:radiation2 __radiation2) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _radiation2 __radiation2)
   self)
  (:radiation2
   (&optional __radiation2)
   (if __radiation2 (setq _radiation2 __radiation2)) _radiation2)
  (:serialization-length
   ()
   (+
    ;; float64[] _radiation2
    (* 8    (length _radiation2)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _radiation2
     (write-long (length _radiation2) s)
     (dotimes (i (length _radiation2))
       (sys::poke (elt _radiation2 i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _radiation2
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _radiation2 (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _radiation2 i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get radiation_pub2::radiation2 :md5sum-) "9a7d2ef45bfc6a980a446dc09330c970")
(setf (get radiation_pub2::radiation2 :datatype-) "radiation_pub2/radiation2")
(setf (get radiation_pub2::radiation2 :definition-)
      "float64[] radiation2

")



(provide :radiation_pub2/radiation2 "9a7d2ef45bfc6a980a446dc09330c970")


