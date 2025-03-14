
(cl:in-package :asdf)

(defsystem "radiation_pub2-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "radiation2" :depends-on ("_package_radiation2"))
    (:file "_package_radiation2" :depends-on ("_package"))
  ))