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
      (mlet (((val rst) (re-1 (car exprs) str)))
        (if val
            (values val rst)
            (re-alt (cdr exprs) str)))
      (values nil
              str)))

(defun re-seq (exprs str acc)
  (if exprs
      (mlet (((val rst) (re-1 (car exprs) str)))
        (if val
            (re-seq (cdr exprs) rst (concatenate 'string acc val))
            (values nil rst)))
      (values acc str)))

(defun re-rep (expr n str i acc)
  (mlet (((val rst) (re-1 expr str)))
    (if val
        (re-rep expr n rst (+ i 1) (concatenate 'string acc val))
        (values (if (>= i n) acc) rst))))

(defun re-not (expr str)
  (if (re-1 expr str)
      (values nil str)
      (if (zerop (length str))
          (values "" "")
          (values (subseq str 0 1)
                  (subseq str 1)))))

(defun re-1 (expr str)
  (cond ((characterp expr) (re-ran expr expr str))
        ((listp expr)
         (case (car expr)
           (ran (re-ran (cadr expr) (caddr expr) str))
           (alt (re-alt (cdr expr) str))
           (seq (re-seq (cdr expr) str ""))  
           (rep (re-rep (cadr expr) (caddr expr) str 0 ""))
           (not (re-not (cadr expr) str))))
        (t (error "invalid expression"))))

(assert (equal (re-1 #\a "") nil))
(assert (equal (re-1 #\a "a") "a"))
(assert (equal (re-1 #\a "ba") nil))
(re-1 #\a "d")
(re-1 #\a "ad")

(re-1 '(ran #\a #\c) "b")
(re-1 '(alt #\a #\b) "e")
(re-1 '(alt (ran #\a #\c) #\ó) "b")
(re-1 '(seq #\a #\b) "abcd")
(re-1 '(rep (seq #\a #\b) 0) "ababcd")
(re-1 '(not (seq #\a #\b) 0) "ababcd")
(re-1 '(not (seq #\a #\b) 0) "agabcd")
(re-1 '(not (seq #\a #\b) 0) "fababcd")

