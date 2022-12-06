(ns day_06)

(defn has-received-marker?
  [stream offset size]
  (let [packet (subs stream (- offset size) offset)]
    (and
     (> offset size)
     (= (count packet) (count (set packet))))))

(defn find-marker
  [stream size]
  (loop [offset size]
    (cond
      (has-received-marker? stream offset size) offset
      (> offset (count stream))                 nil
      :else                                     (recur (inc offset)))))

(find-marker (slurp "../inputs/day_06.txt") 4)
(find-marker (slurp "../inputs/day_06.txt") 14)