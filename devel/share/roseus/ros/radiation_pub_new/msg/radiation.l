;; Auto-generated. Do not edit!


(when (boundp 'radiation_pub_new::radiation)
  (if (not (find-package "RADIATION_PUB_NEW"))
    (make-package "RADIATION_PUB_NEW"))
  (shadow 'radiation (find-package "RADIATION_PUB_NEW")))
(unless (find-package "RADIATION_PUB_NEW::RADIATION")
  (make-package "RADIATION_PUB_NEW::RADIATION"))

(in-package "ROS")
;;//! \htmlinclude radiation.msg.html


(defclass radiation_pub_new::radiation
  :super ros::object
  :slots (_radiation ))

(defmethod radiation_pub_new::radiation
  (:init
   (&key
    ((:radiation __radiation) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _radiation __radiation)
   self)
  (:radiation
   (&optional __radiation)
   (if __radiation (setq _radiation __radiation)) _radiation)
  (:serialization-length
   ()
   (+
    ;; float64[] _radiation
    (* 8    (length _radiation)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _radiation
     (write-long (length _radiation) s)
     (dotimes (i (length _radiation))
       (sys::poke (elt _radiation i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _radiation
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _radiation (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _radiation i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get radiation_pub_new::radiation :md5sum-) "ae3ed639d310a116f0319906c7d3e096")
(setf (get radiation_pub_new::radiation :datatype-) "radiation_pub_new/radiation")
(setf (get radiation_pub_new::radiation :definition-)
      "float64[] radiation

")



(provide :radiation_pub_new/radiation "ae3ed639d310a116f0319906c7d3e096")


