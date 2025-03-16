
(cl:in-package :asdf)

(defsystem "radiation_pub_new-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "radiation" :depends-on ("_package_radiation"))
    (:file "_package_radiation" :depends-on ("_package"))
  ))