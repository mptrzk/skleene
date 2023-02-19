(defun mlet-gen (clauses body)
  (let* ((first-clause (car clauses))
         (other-clauses (cdr clauses))
         (vars (if (atom (car first-clause))
                   (list (car first-clause))
                   (car first-clause)))
         (expr (cadr first-clause)))
    `(multiple-value-bind ,vars ,expr 
       ,@(if other-clauses 
             (list (mlet-gen other-clauses body)) 
             body)))) 

(mlet-gen '(((a b) (f 2))
            (d (g 3)))
          '((foo a b) (bar c d)))

(defmacro mlet (clauses &body body)
  (mlet-gen clauses body))

(mlet (((a b) (floor 1.2))
       (c (floor 4.9)))
      (list a b c))

(defun dump (expr)
  (format t "~a~%" expr)
  expr)


(defun re-ran (lo hi str)
  (if (zerop (length str))
      (values nil "")
      (if (and (char>= (aref str 0) lo)
               (char<= (aref str 0) hi)) 
          (values (subseq str 0 1) (subseq str 1))
          (values nil str))))

(defun re-alt (exprs str)
  (if exprs
      (mlet (((val rst) (re (car exprs) str)))
        (if val
            (values val rst)
            (re-alt (cdr exprs) str)))
      (values nil
              str)))

(defun re-seq (exprs str acc)
  (if exprs
      (mlet (((val rst) (re (car exprs) str)))
        (if val
            (re-seq (cdr exprs) rst (concatenate 'string acc val))
            (values nil rst)))
      (values acc str)))

(defun re-rep (expr n str i acc)
  (mlet (((val rst) (re expr str)))
    (if val
        (re-rep expr n rst (+ i 1) (concatenate 'string acc val))
        (values (if (>= i n) acc) rst))))

(defun re-not (expr str)
  (if (re expr str)
      (values nil str)
      (if (zerop (length str))
          (values "" "")
          (values (subseq str 0 1)
                  (subseq str 1)))))

(defparameter *re-defs*
  '((alpha-c . (alt (ran #\a #\z)
                  (ran #\A #\Z))) 
    (num-c . (ran #\0 #\9))
    (alphanum-c . (alt alpha-c num-c))))

(defun re (expr str)
  (cond ((characterp expr) (re-ran expr expr str))
        ((listp expr)
         (case (car expr)
           (ran (re-ran (cadr expr) (caddr expr) str))
           (alt (re-alt (cdr expr) str))
           (seq (re-seq (cdr expr) str ""))  
           (rep (re-rep (cadr expr) (caddr expr) str 0 ""))
           (not (re-not (cadr expr) str)))) 
        ((symbolp expr)
         (let ((rec (assoc expr *re-defs*)))
           (if rec
               (re (cdr rec) str)
               (error "invalid definition"))))
        (t (error "invalid expression"))))

(assert (equal (re #\a "") nil))
(assert (equal (re #\a "a") "a"))
(assert (equal (re #\a "ba") nil))
(re #\a "d")
(re #\a "ad")

(re '(ran #\a #\c) "b")
(re '(alt #\a #\b) "e")
(re '(alt (ran #\a #\c) #\ó) "b")
(re '(seq #\a #\b) "abcd")
(re '(rep (seq #\a #\b) 0) "ababcd")
(re '(not (seq #\a #\b)) "ababcd")
(re '(not (seq #\a #\b)) "agabcd")
(re '(not (seq #\a #\b)) "fababcd")

(re '(seq (ran #\a #\z) 
          (rep (alt (ran #\a #\z)
                    (ran #\0 #\9))
               0))
    "1a")

(re 'num-c "22")

