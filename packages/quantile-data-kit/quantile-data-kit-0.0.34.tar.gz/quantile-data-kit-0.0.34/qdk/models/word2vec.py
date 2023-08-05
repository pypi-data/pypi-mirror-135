#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Chinmaya Pancholi <chinmayapancholi13@gmail.com>
# Copyright (C) 2017 Radim Rehurek <radimrehurek@seznam.cz>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""Scikit learn interface for :class:`~gensim.models.word2vec.Word2Vec`.
Follows scikit-learn API conventions to facilitate using gensim along with scikit-learn.
Examples
--------
.. sourcecode:: pycon
    >>> from gensim.test.utils import common_texts
    >>> from gensim.sklearn_api import W2VTransformer
    >>>
    >>> # Create a model to represent each word by a 10 dimensional vector.
    >>> model = W2VTransformer(size=10, min_count=1, seed=1)
    >>>
    >>> # What is the vector representation of the word 'graph'?
    >>> wordvecs = model.fit(common_texts).transform(['graph', 'system'])
    >>> assert wordvecs.shape ==2, 10)
"""
from typing import List, Optional

import numpy as np
from gensim.models import Word2Vec
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError


class Word2VecModel(TransformerMixin, BaseEstimator):
    """Base Word2Vec module, wraps :class:`~gensim.models.word2vec.Word2Vec`.
    For more information please have a look to `Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean: "Efficient
    Estimation of Word Representations in Vector Space" <https://arxiv.org/abs/1301.3781>`_.
    """

    def __init__(
        self,
        corpus_file=None,
        vector_size=100,
        alpha=0.025,
        window=5,
        min_count=5,
        max_vocab_size=None,
        sample=1e-3,
        seed=1,
        workers=3,
        min_alpha=0.0001,
        sg=0,
        hs=0,
        negative=5,
        ns_exponent=0.75,
        cbow_mean=1,
        hashfxn=hash,
        epochs=5,
        null_word=0,
        trim_rule=None,
        sorted_vocab=1,
        batch_words=10_000,
        compute_loss=False,
        callbacks=(),
        comment=None,
        max_final_vocab=None,
        shrink_windows=True,
        mean_vector=True,
    ):
        """Train, use and evaluate neural networks described in https://code.google.com/p/word2vec/.

        Once you're finished training a model (=no more updates, only querying)
        store and use only the :class:`~gensim.models.keyedvectors.KeyedVectors` instance in ``self.wv``
        to reduce memory.

        The full model can be stored/loaded via its :meth:`~gensim.models.word2vec.Word2Vec.save` and
        :meth:`~gensim.models.word2vec.Word2Vec.load` methods.

        The trained word vectors can also be stored/loaded from a format compatible with the
        original word2vec implementation via `self.wv.save_word2vec_format`
        and :meth:`gensim.models.keyedvectors.KeyedVectors.load_word2vec_format`.

        Parameters
        ----------
        sentences : iterable of iterables, optional
            The `sentences` iterable can be simply a list of lists of tokens, but for larger corpora,
            consider an iterable that streams the sentences directly from disk/network.
            See :class:`~gensim.models.word2vec.BrownCorpus`, :class:`~gensim.models.word2vec.Text8Corpus`
            or :class:`~gensim.models.word2vec.LineSentence` in :mod:`~gensim.models.word2vec` module for such examples.
            See also the `tutorial on data streaming in Python
            <https://rare-technologies.com/data-streaming-in-python-generators-iterators-iterables/>`_.
            If you don't supply `sentences`, the model is left uninitialized -- use if you plan to initialize it
            in some other way.
        corpus_file : str, optional
            Path to a corpus file in :class:`~gensim.models.word2vec.LineSentence` format.
            You may use this argument instead of `sentences` to get performance boost. Only one of `sentences` or
            `corpus_file` arguments need to be passed (or none of them, in that case, the model is left uninitialized).
        vector_size : int, optional
            Dimensionality of the word vectors.
        window : int, optional
            Maximum distance between the current and predicted word within a sentence.
        min_count : int, optional
            Ignores all words with total frequency lower than this.
        workers : int, optional
            Use these many worker threads to train the model (=faster training with multicore machines).
        sg : {0, 1}, optional
            Training algorithm: 1 for skip-gram; otherwise CBOW.
        hs : {0, 1}, optional
            If 1, hierarchical softmax will be used for model training.
            If 0, and `negative` is non-zero, negative sampling will be used.
        negative : int, optional
            If > 0, negative sampling will be used, the int for negative specifies how many "noise words"
            should be drawn (usually between 5-20).
            If set to 0, no negative sampling is used.
        ns_exponent : float, optional
            The exponent used to shape the negative sampling distribution. A value of 1.0 samples exactly in proportion
            to the frequencies, 0.0 samples all words equally, while a negative value samples low-frequency words more
            than high-frequency words. The popular default value of 0.75 was chosen by the original Word2Vec paper.
            More recently, in https://arxiv.org/abs/1804.04212, Caselles-Dupré, Lesaint, & Royo-Letelier suggest that
            other values may perform better for recommendation applications.
        cbow_mean : {0, 1}, optional
            If 0, use the sum of the context word vectors. If 1, use the mean, only applies when cbow is used.
        alpha : float, optional
            The initial learning rate.
        min_alpha : float, optional
            Learning rate will linearly drop to `min_alpha` as training progresses.
        seed : int, optional
            Seed for the random number generator. Initial vectors for each word are seeded with a hash of
            the concatenation of word + `str(seed)`. Note that for a fully deterministically-reproducible run,
            you must also limit the model to a single worker thread (`workers=1`), to eliminate ordering jitter
            from OS thread scheduling. (In Python 3, reproducibility between interpreter launches also requires
            use of the `PYTHONHASHSEED` environment variable to control hash randomization).
        max_vocab_size : int, optional
            Limits the RAM during vocabulary building; if there are more unique
            words than this, then prune the infrequent ones. Every 10 million word types need about 1GB of RAM.
            Set to `None` for no limit.
        max_final_vocab : int, optional
            Limits the vocab to a target vocab size by automatically picking a matching min_count. If the specified
            min_count is more than the calculated min_count, the specified min_count will be used.
            Set to `None` if not required.
        sample : float, optional
            The threshold for configuring which higher-frequency words are randomly downsampled,
            useful range is (0, 1e-5).
        hashfxn : function, optional
            Hash function to use to randomly initialize weights, for increased training reproducibility.
        epochs : int, optional
            Number of iterations (epochs) over the corpus. (Formerly: `iter`)
        trim_rule : function, optional
            Vocabulary trimming rule, specifies whether certain words should remain in the vocabulary,
            be trimmed away, or handled using the default (discard if word count < min_count).
            Can be None (min_count will be used, look to :func:`~gensim.utils.keep_vocab_item`),
            or a callable that accepts parameters (word, count, min_count) and returns either
            :attr:`gensim.utils.RULE_DISCARD`, :attr:`gensim.utils.RULE_KEEP` or :attr:`gensim.utils.RULE_DEFAULT`.
            The rule, if given, is only used to prune vocabulary during build_vocab() and is not stored as part of the
            model.

            The input parameters are of the following types:
                * `word` (str) - the word we are examining
                * `count` (int) - the word's frequency count in the corpus
                * `min_count` (int) - the minimum count threshold.
        sorted_vocab : {0, 1}, optional
            If 1, sort the vocabulary by descending frequency before assigning word indexes.
            See :meth:`~gensim.models.keyedvectors.KeyedVectors.sort_by_descending_frequency()`.
        batch_words : int, optional
            Target size (in words) for batches of examples passed to worker threads (and
            thus cython routines).(Larger batches will be passed if individual
            texts are longer than 10000 words, but the standard cython code truncates to that maximum.)
        compute_loss: bool, optional
            If True, computes and stores loss value which can be retrieved using
            :meth:`~gensim.models.word2vec.Word2Vec.get_latest_training_loss`.
        callbacks : iterable of :class:`~gensim.models.callbacks.CallbackAny2Vec`, optional
            Sequence of callbacks to be executed at specific stages during training.
        shrink_windows : bool, optional
            New in 4.1. Experimental.
            If True, the effective window size is uniformly sampled from  [1, `window`]
            for each target word during training, to match the original word2vec algorithm's
            approximate weighting of context words by distance. Otherwise, the effective
            window size is always fixed to `window` words to either side.
        mean_vector : bool, optional
            Whether to predict a word vector for each individual word, or whether to
            average them.

        Examples
        --------
        Initialize and train a :class:`~gensim.models.word2vec.Word2Vec` model

        .. sourcecode:: pycon

            >>> from gensim.models import Word2Vec
            >>> sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]
            >>> model = Word2Vec(sentences, min_count=1)

        Attributes
        ----------
        wv : :class:`~gensim.models.keyedvectors.KeyedVectors`
            This object essentially contains the mapping between words and embeddings. After training, it can be used
            directly to query those embeddings in various ways. See the module level docstring for examples.

        """
        self.model = None
        self.corpus_file = corpus_file
        self.vector_size = vector_size
        self.alpha = alpha
        self.window = window
        self.min_count = min_count
        self.max_vocab_size = max_vocab_size
        self.sample = sample
        self.seed = seed
        self.workers = workers
        self.min_alpha = min_alpha
        self.sg = sg
        self.hs = hs
        self.negative = negative
        self.ns_exponent = ns_exponent
        self.cbow_mean = cbow_mean
        self.hashfxn = hashfxn
        self.epochs = epochs
        self.null_word = null_word
        self.trim_rule = trim_rule
        self.sorted_vocab = sorted_vocab
        self.batch_words = batch_words
        self.compute_loss = compute_loss
        self.callbacks = callbacks
        self.comment = comment
        self.max_final_vocab = max_final_vocab
        self.shrink_windows = shrink_windows
        self.mean_vector = mean_vector

    def fit(self, X, y=None):
        """Fit the model according to the given training data.
        Parameters
        ----------
        X : iterable of iterables of str
            The input corpus. X can be simply a list of lists of tokens, but for larger corpora,
            consider an iterable that streams the sentences directly from disk/network.
            See :class:`~gensim.models.word2vec.BrownCorpus`, :class:`~gensim.models.word2vec.Text8Corpus`
            or :class:`~gensim.models.word2vec.LineSentence` in :mod:`~gensim.models.word2vec` module for such examples.
        Returns
        -------
        :class:`~gensim.sklearn_api.w2vmodel.W2VTransformer`
            The trained model.
        """
        self.model = Word2Vec(
            sentences=X,
            corpus_file=self.corpus_file,
            vector_size=self.vector_size,
            alpha=self.alpha,
            window=self.window,
            min_count=self.min_count,
            max_vocab_size=self.max_vocab_size,
            sample=self.sample,
            seed=self.seed,
            workers=self.workers,
            min_alpha=self.min_alpha,
            sg=self.sg,
            hs=self.hs,
            negative=self.negative,
            ns_exponent=self.ns_exponent,
            cbow_mean=self.cbow_mean,
            hashfxn=self.hashfxn,
            epochs=self.epochs,
            null_word=self.null_word,
            trim_rule=self.trim_rule,
            sorted_vocab=self.sorted_vocab,
            batch_words=self.batch_words,
            compute_loss=self.compute_loss,
            callbacks=self.callbacks,
            comment=self.comment,
            max_final_vocab=self.max_final_vocab,
            shrink_windows=self.shrink_windows,
        )
        return self

    def infer_single_token(
        self,
        token: str,
    ) -> Optional[np.ndarray]:
        """
        Use the trained Word2Vec to infer the vector of a single token.
        If the token is unknown it returns an empty numpy array.
        """
        return self.model.wv[token] if token in self.model.wv else np.array([])

    def infer_list_of_tokens(
        self,
        tokens: List[str],
    ) -> List[np.ndarray]:
        """
        If the word vectors of multiple token in a document.
        """
        return [self.infer_single_token(token) for token in tokens if token]

    def mean_of_vector_list(
        self,
        vector_list: List[np.ndarray],
    ) -> np.ndarray:
        """
        Take the mean word vector of a document. It excludes tokens that do
        not have a vector.
        """
        vectors_without_nones = [vector for vector in vector_list if vector.size > 0]
        return np.mean(vectors_without_nones, axis=0)

    def transform(self, X):
        """
        Transform a list of documents. It returns the mean vector for each document.
        Documents that do not have any recognised tokens returns np.nan.
        """
        if self.model is None:
            raise NotFittedError(
                "This model has not been fitted yet. Call 'fit' with appropriate arguments before using this method."
            )

        word_tokens = [self.infer_list_of_tokens(tokens) for tokens in X]

        # Calculate the mean vector of all tokens in each document
        if self.mean_vector:
            word_tokens = [self.mean_of_vector_list(tokens) for tokens in word_tokens]

        return word_tokens

    def partial_fit(self, X):
        raise NotImplementedError(
            "'partial_fit' has not been implemented for W2VTransformer. "
            "However, the model can be updated with a fixed vocabulary using Gensim API call."
        )
