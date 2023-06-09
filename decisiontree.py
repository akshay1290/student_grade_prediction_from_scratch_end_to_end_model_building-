# -*- coding: utf-8 -*-
"""decisiontree1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1duvmmtVwyLh7x9MsfdkvqqXDA9zGVwRs
"""

import numpy as np

class DecisionTreeRegressor:
    def __init__(self, max_depth=5, min_samples_split=2, min_impurity_decrease=0.0):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_impurity_decrease = min_impurity_decrease

    def fit(self, X, y):
        self.n_features_ = X.shape[1]
        self.tree_ = self._build_tree(X, y)

    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])

    def _build_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape

        # check for stopping criteria
        if depth >= self.max_depth or n_samples < self.min_samples_split or self._impurity(y) <= self.min_impurity_decrease:
            return np.mean(y)

        # select best split based on information gain
        best_feature, best_threshold = self._find_best_split(X, y)

        # split data into left and right subsets
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = X[:, best_feature] > best_threshold
        left_X, left_y = X[left_mask], y[left_mask]
        right_X, right_y = X[right_mask], y[right_mask]

        # create a new node and recursively build the tree
        node = {
            "feature": best_feature,
            "threshold": best_threshold,
            "left": self._build_tree(left_X, left_y, depth + 1),
            "right": self._build_tree(right_X, right_y, depth + 1),
        }

        return node

    def _find_best_split(self, X, y):
        best_gain = -np.inf
        best_feature = None
        best_threshold = None

        for feature in range(self.n_features_):
            values = X[:, feature]
            thresholds = np.unique(values)
            for threshold in thresholds:
                left_mask = values <= threshold
                right_mask = values > threshold
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue
                left_y = y[left_mask]
                right_y = y[right_mask]
                gain = self._information_gain(y, left_y, right_y)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def _information_gain(self, y, left_y, right_y):
        p = len(left_y) / len(y)
        return self._impurity(y) - p * self._impurity(left_y) - (1 - p) * self._impurity(right_y)

    def _impurity(self, y):
        mean = np.mean(y)
        return np.mean((y - mean) ** 2)

    def _predict_one(self, x):
        node = self.tree_
        while isinstance(node, dict):
            if x[node["feature"]] <= node["threshold"]:
                node = node["left"]
            else:
                node = node["right"]
        return node