(ns day_12
  (:require [clojure.string :as str]))

(defn read-grid
  [data]
  (->> data
       str/split-lines
       (mapv #(mapv int %))))

(defn find-positions
  [grid]
  (let [coords 
        (for [r (range (count grid))
              c (range (count (first grid)))]
          [r c])]
    (->> coords
         (map #(case (get-in grid %)
                 83 {:start %}
                 69 {:goal %}
                 nil))
         (filter identity)
         (into {}))))

(defn replace-position-values
  [grid {:keys [start goal]}]
  (-> grid
      (assoc-in start (int \a))
      (assoc-in goal (int \z))))

(defn parse-input
  [filename]
  (let [grid (read-grid filename)
        positions (find-positions grid)]
    (into {:grid (replace-position-values grid positions)}
          positions)))

(defn get-neighbours 
  [grid [x y :as pos]]
  (let [min-h (dec (get-in grid pos))]
    (->> [[(dec x) y]
          [(inc x) y]
          [x (dec y)]
          [x (inc y)]] 
         (filter #(if-let [new-h (get-in grid %)]
                    (<= min-h new-h))))))

(defn bfs-search
  [goal-fn {:keys [grid goal] :as world}]
  (loop [queue [{:d 0 :pos goal}] visited #{}]
    (if-not (empty? queue)
      (let [[{:keys [d pos]} & rest] queue]
        (cond
          (goal-fn world pos)
          d

          (visited pos)
          (recur (vec rest) (conj visited pos))

          :else
          (recur (->> (get-neighbours grid pos)
                      (filter #(not (visited %)))
                      (map (fn [p] {:d (inc d) :pos p}))
                      (into (vec rest)))
                 (conj visited pos))))
      nil)))

(defn goal-reached-part-1?
  [{:keys [start]} pos]
  (= pos start))

(defn goal-reached-part-2?
  [{grid :grid} pos]
  (= (get-in grid pos) (int \a)))

(defn part-1
  [filename]
  (->> filename
       slurp
       parse-input
       (bfs-search goal-reached-part-1?)))

(defn part-2
  [filename]
  (->> filename
       slurp
       parse-input
       (bfs-search goal-reached-part-2?)))

(part-1 "../inputs/day_12_test.txt")
(part-1 "../inputs/day_12.txt")

(part-2 "../inputs/day_12_test.txt")
(part-2 "../inputs/day_12.txt")
