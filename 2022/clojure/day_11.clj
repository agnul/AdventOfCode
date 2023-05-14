(ns day_11
  (:require [clojure.string :as str]))

(defn calc-big-num
  [input]
  (->> input
       (re-seq #"by (\d+)")
       (map #(parse-long (second %)))
       (apply *)))

(defn stress-reducer
  [monkey]
  (update monkey :update (partial comp #(quot % 3))))

(defn parse-update
  [line]
  (let [[a op b] (drop 4 (str/split line #"\s+"))
        op-fn (condp = op
                "+" +
                "*" *)]
    (fn [x]
      (letfn [(eval [arg] (if (= "old" arg) x (parse-long arg)))]
        (apply op-fn (map eval [a b]))))))

(defn parse-destination
  [lines]
  (let [[modulo on-true on-false]
        (->> lines (map #(re-find #"\d+" %)) (map parse-long))]
    (fn [x] (if (zero? (rem x modulo)) on-true on-false))))

(defn parse-monkey
  [big-num lines]
  (let [[_ items op & destination]
        (str/split-lines lines)]
    {:items (mapv parse-long (re-seq #"\d+" items))
     :update (comp #(mod % big-num) (parse-update op))
     :destination (parse-destination destination)
     :inspections 0}))

(defn parse-input
  [input]
  (let [big-num (calc-big-num input)]
    (as-> input m
      (str/split m #"\n\n")
      (mapv #(parse-monkey big-num %) m))))

(defn take-turn
  [monkeys i]
  (loop [monkeys monkeys]
    (let [monkey (monkeys i)
          item (first (:items monkey))]
      (if item
        (let [new-item ((:update monkey) item)
              destination ((:destination monkey) new-item)]
          (recur (-> monkeys
                     (update-in [i :items] subvec 1)
                     (update-in [i :inspections] inc)
                     (update-in [destination :items] conj new-item))))
        monkeys))))

(defn play-round
  [monkeys]
  (reduce take-turn monkeys (range (count monkeys)))) 

(defn part-1
  [filename] 
  (->> filename
       slurp 
       parse-input
       (mapv stress-reducer)
       (iterate play-round)
       (drop 20)
       first
       (map :inspections)
       (sort >)
       (take 2)
       (apply *)))

(defn part-2
  [filename]
  (->> filename
       slurp
       parse-input
       (iterate play-round)
       (drop 10000)
       first
       (map :inspections)
       (sort >)
       (take 2)
       (apply *)))

(part-1 "../inputs/day_11_test.txt")
(part-1 "../inputs/day_11.txt")

(part-2 "../inputs/day_11_test.txt")
(part-2 "../inputs/day_11.txt")
