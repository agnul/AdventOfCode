(ns day_05
  (:require [clojure.string :as str]))

(defn push-crate
  [crate stack]
  (if-not (= crate \space)
    (conj stack crate)
    stack))

(defn read-stack
  [input column mod]
  (loop [offset column stack ()]
    (if (< offset (count input))
      (recur (+ offset mod) (push-crate (nth input offset) stack))
      (reverse stack))))

(defn read-stacks
  [input]
  (let [line-length (str/index-of input \newline) 
        mod (+ 1 line-length)]
    ; start with a dummy stack at position zero
    ; so we don't have to fix indexes in instructions
    (loop [i 1 stacks '((\0))]
      (if (< i line-length)
        (recur (+ i 4) (conj stacks (read-stack input i mod)))
        (reverse stacks)))))

(defn read-input
  [filename]
  (let [[stacks instructions] (str/split (slurp filename) #"\n\n")]
    {:stacks (read-stacks stacks)
     :instructions (->> instructions
                        (re-seq #"\d+")
                        (map parse-long)
                        (partition 3))}))

(defn move-one-crate
  [stacks from to]
  (let [from-stack (nth stacks from)
        to-stack (nth stacks to)
        crate (first from-stack)]
    (replace {from-stack (rest from-stack)
              to-stack (conj to-stack crate)} stacks)))

(defn with-crate-master-9000
  [stacks times from to]
  (loop [i 0 res stacks]
    (if (< i times)
      (recur (inc i) (move-one-crate res from to))
      res)))

(defn with-crate-master-9001
  [stacks cnt from to]
  (let [from-stack (nth stacks from)
        to-stack (nth stacks to)
        crates (take cnt from-stack)]
    (replace {from-stack (drop cnt from-stack)
              to-stack (into to-stack (reverse crates))} stacks)))

(defn move-stacks-in
  [filename move-fn]
  (let [{:keys [stacks instructions]}
        (read-input filename)]
    (loop [moves instructions res stacks]
      (if-not (empty? moves)
        (recur (rest moves) (apply move-fn res (first moves)))
        res))))

(defn top-of-stacks
  [stacks]
  (->> stacks
       (map first)
       (drop 1)
       (apply str)))

(defn part-1
  [filename]
  (top-of-stacks (move-stacks-in filename with-crate-master-9000)))

(defn part-2
  [filename]
  (top-of-stacks (move-stacks-in filename with-crate-master-9001)))

(part-1 "../inputs/day_05_test.txt")
(part-2 "../inputs/day_05_test.txt")

(part-1 "../inputs/day_05.txt")
(part-2 "../inputs/day_05.txt")
