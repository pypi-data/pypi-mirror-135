from gensim.models import Word2Vec
from qdk.models import Word2VecModel


def test_word2vec_model():
    X = [["a", "b"]]

    # Instanciate the model
    w2v_model = Word2VecModel(
        vector_size=5,
        min_count=1,
    )

    # Make sure there is no fitted model yet
    assert w2v_model.model == None

    # Fit the model
    w2v_model.fit(X)

    # Make sure the model is fitted now
    assert isinstance(w2v_model.model, Word2Vec)

    # Test the fit_transform functionality
    word_vectors = w2v_model.fit_transform(X)

    assert len(word_vectors) == 1
    assert len(word_vectors[0]) == 5


def test_word2vec_model_mean_vector():
    X = [["a", "b"]]

    # Instanciate the model
    w2v_model = Word2VecModel(
        vector_size=5,
        min_count=1,
        mean_vector=False,
    )

    word_vectors = w2v_model.fit_transform(X)

    assert len(word_vectors[0]) == 2
    assert len(word_vectors[0][0]) == 5
