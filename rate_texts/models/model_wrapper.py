import pandas as pd
import numpy as np
import numpy.typing as npt
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score
from scipy.sparse import spmatrix
from pathlib import Path
from rate_texts.tools import keys


class ModelWrapper():

    name: str
    """A name for the model."""
    desc: str
    """A description"""
    train_scores: pd.DataFrame
    """A spreadsheet with the training scores"""
    test_scores: pd.DataFrame
    """A spreadsheet with the test scores"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.train_scores = pd.DataFrame([], columns=[
            keys.ACCURACY, keys.PRECISION, keys.RECALL, keys.F1], index=[0, 1, 2, 3, 4, 5, 'avg'])
        self.test_scores = pd.DataFrame([], columns=[
            keys.ACCURACY, keys.PRECISION, keys.RECALL, keys.F1], index=[0, 1, 2, 3, 4, 5, 'avg'])

    def fit(self, features: spmatrix, labels: pd.Series) -> None:
        pass

    def compute_training_scores(self, features: spmatrix, labels: pd.Series) -> pd.DataFrame:
        """
        Computes the accuracies, precisions, recalls, and f1 scores for the training data.

        labels:
        The true labels.

        pred:
        The predicted labels.
        """
        pred = self.predict(features)
        acc = self.compute_accuracy(labels, pred)
        self.train_scores[keys.ACCURACY] = acc
        prec = self.compute_precision(labels, pred)
        self.train_scores[keys.PRECISION] = prec
        rec = self.compute_recall(labels, pred)
        self.train_scores[keys.RECALL] = rec
        f1 = self.compute_f1(labels, pred)
        self.train_scores[keys.F1] = f1

        return self.train_scores

    def predict(self, features: spmatrix) -> npt.NDArray:
        return np.array([])

    def test(self, features: spmatrix, labels: pd.Series) -> pd.DataFrame:
        """
        Applies the test data. The predictions are computed for the test samples
        and compared against the test labels. Also writes the accuracy, precision,
        recall, and f1 scores into a data frame.

        features: scipy.sparse.spmatrix
        The feature matrix.

        labels: pandas.Series
        The correct labels.

        returns: pandas.DataFrame
        Speadsheet with the scores for each labelled category.
        """
        pred = self.predict(features)
        acc = self.compute_accuracy(labels, pred)
        self.test_scores[keys.ACCURACY] = acc
        prec = self.compute_precision(labels, pred)
        self.test_scores[keys.PRECISION] = prec
        rec = self.compute_recall(labels, pred)
        self.test_scores[keys.RECALL] = rec
        f1 = self.compute_f1(labels, pred)
        self.test_scores[keys.F1] = f1

        return self.test_scores

    def compute_precision(self, labels: pd.Series, pred: npt.NDArray, categories: int = 6) -> npt.NDArray[np.float64]:
        """
        Computes the precision (true positives over all positive classifications) for each label.
        Also computes the, unweighted, average of the precisions.

        ---

        labels:
        The true labels.

        pred:
        The predicted samples.

        categories (default 6):
        The number of categories.

        ---

        returns:
        The label-specific precisions, with the precision of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the average precision at index 6.
        """
        label_prec = precision_score(
            labels, pred, labels=np.arange(categories), average=None)
        avg = np.mean(label_prec)
        return np.concatenate([label_prec, [avg]])

    def compute_accuracy(self, labels: pd.Series, pred: npt.NDArray, categories: int = 6) -> npt.NDArray[np.float64]:
        """
        Computes the accuracy (fraction of correct classifications) for each label as well as for
        all samples.

        ---

        labels:
        The true labels.

        pred:
        The predicted samples.

        categories (default 6):
        The number of categories.

        ---

        returns:
        The label-specific accuracies, with the accuracy of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the overall accuracy at index 6 (if categories=6).

        """
        acc = []
        for label in range(categories):
            idx1 = labels == label
            idx2 = pred == label
            idxTP = idx1 & idx2
            idxTN = np.logical_not(idx1) & np.logical_not(idx2)
            acc_label = (len(pred[idxTP]) + len(pred[idxTN])) / len(pred)
            acc.append(acc_label)
        acc_mean = accuracy_score(labels, pred)
        acc.append(acc_mean)
        return np.array(acc)

    def compute_recall(self, labels: pd.Series, pred: npt.NDArray, categories: int = 6) -> npt.NDArray[np.float64]:
        """
        Computes the recall (true positives over all positive samples) for each label.
        Also computes the, unweighted, average of the recalls.

        ---

        labels:
        The true labels.

        pred:
        The predicted samples.

        categories (default 6):
        The number of categories.

        ---

        returns:
        The label-specific recalls, with the recall of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the average recall at index 6 (if categories=6).
        """
        label_rec = recall_score(
            labels, pred, labels=np.arange(categories), average=None)
        avg = np.mean(label_rec)
        return np.concatenate([label_rec, [avg]])

    def compute_f1(self, labels: pd.Series, pred: npt.NDArray, categories: int = 6) -> npt.NDArray[np.float64]:
        """
        Computes the f1 (true positives over all positive samples) for each label.
        Also computes the, unweighted, average of the f1s.

        ---

        labels:
        The true labels.

        pred:
        The predicted samples.

        categories (default 6):
        The number of categories.

        ---

        returns:
        The label-specific f1s, with the f1 of 0 star ratings at index 0, of 5 star ratings
        at index 5, and the average f1 at index 6 (if categories=6).
        """
        label_f1 = f1_score(
            labels, pred, labels=np.arange(categories), average=None)
        avg = np.mean(label_f1)
        return np.concatenate([label_f1, [avg]])

    def write_model(self, dir: Path) -> None:
        """
        Save the model under its name in the given directory.

        dir:
        The directory in which the model is saved.
        """
        pass
