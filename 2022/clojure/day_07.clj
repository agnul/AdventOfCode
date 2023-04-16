(ns day_07
  (:require [clojure.string :as str]))

(defn mknode
  [line]
  (let [[size name] (str/split line #"\s+")]
    (if (= "dir" size)
      {:name name :size 0}
      {:name name :size (parse-long size) :children {}})))

(defn append
  [root cwd {:keys [name size]:as node}]
  (let [[dir & dirs] cwd
        parent (get-in root [:children dir])]
    (if-not (empty? cwd)
      (-> root
          (update :size + size)
          (assoc-in [:children dir] (append parent dirs node)))
      (-> root
          (update :size + size)
          (assoc-in [:children name] node)))))

(defn is-command?
  [line]
  (str/starts-with? line "$"))

(defn execute-cmd
  [state cmd-line]
  (let [[_ cmd arg] (str/split cmd-line #"\s+")]
    (if (= cmd "cd")
      (condp = arg
        "/"  (assoc state :cwd [])
        ".." (update state :cwd pop)
        (update state :cwd conj arg))
      state)))

(defn add-file-or-dir
  [{:keys [root cwd] :as state} line]
  (assoc state :root (append root cwd (mknode line))))

(defn make-tree
  [terminal-output]
  (:root
   (reduce
    (fn [state line]
      (if (is-command? line)
        (execute-cmd state line)
        (add-file-or-dir state line)))
    {:root (mknode "dir /") :cwd []}
    terminal-output)))

(defn read-input
  [filename]
  (->> filename
       slurp
       str/split-lines
       make-tree))

(defn sub-dirs
  [dir]
  (filter #(contains? % :children) (vals (:children dir))))

(defn dir-sizes
  [dir]
  (let [size (:size dir)
        subs (sub-dirs dir)]
    (if-not (empty? subs)
      (conj (flatten (map dir-sizes subs)) size)
      size)))

(defn part-1
  [filename]
  (let [root (read-input filename)]
    (->> root
         dir-sizes
         (filter #(< % 100000))
         (reduce +))))

(defn part-2
  [filename]
  (let [root (read-input filename)
        free (- 70000000 (:size root))
        goal (- 30000000 free)]
    (->> root
         dir-sizes
         (filter #(>= % goal))
         (reduce min))))

(part-1 "../inputs/day_07_test.txt")
(part-1 "../inputs/day_07.txt")

(part-2 "../inputs/day_07_test.txt")
(part-2 "../inputs/day_07.txt")
