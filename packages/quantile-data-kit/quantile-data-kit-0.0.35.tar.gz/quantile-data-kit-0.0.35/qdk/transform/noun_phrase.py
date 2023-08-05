from typing import List, Union

import dask.dataframe as dd
import nltk
import pandas as pd
import spacy
from dagster import Field
from qdk.transform.base import BaseTransformer
from qdk.utils.text import clean_text


class NounPhraseTransformer(BaseTransformer):
    noun_phrase_regex = "NP: {<NOUN.*|ADJ>*<NOUN.*>}"
    remove_pos = {"PUNCT"}
    config_schema = {
        "text_columns": Field(
            list,
            default_value=["text"],
            description="Columns to tokenize",
        ),
        "spacy_model": Field(
            str,
            default_value="nl_core_news_lg",
            description="The name of the spacy language model (nl_core_news_lg)",
        ),
        "keep_tokens": Field(
            bool,
            default_value=False,
            description="Whether to keep all tokens, or only noun phrases",
        ),
    }

    @classmethod
    def extract_noun_phrases(
        cls,
        text: str,
        nlp: str,
        keep_tokens: bool,
    ) -> List[str]:
        """This function takes a string as input and outputs a list of
        noun phrase candidates:

        "Dit is een zin met tekst" -> ["zin", "tekst"]

        Args:
            text (str): The text you would like to transform.
            nlp (str): A spacy language model. Used for POS tagging.
            keep_tokens (bool): Whether to keep all tokens, or only noun phrases

        Returns:
            List[str]: The noun phrases found in the text.
        """
        # Clean the text before extracting phrases
        cleaned_text = clean_text(text=text)

        # Use spacy to parse and tokenize the text
        doc = nlp(cleaned_text)

        # Only retrieve the text and part of speech tag
        doc = [(token.text.lower(), token.pos_) for token in doc]

        # Use the nltk regex parser to extract different parts of speech
        parser = nltk.RegexpParser(cls.noun_phrase_regex)
        tree = parser.parse(doc)

        # Buffer for all noun phrases and extra tokens
        tokens = []

        # Only select the deepest subtree, this prevents duplicate tokens
        for subtree in tree.subtrees(lambda t: t.height() == tree.height()):
            # The items in the subtree are either a word or a noun phrase subtree
            for phrase in subtree:
                # If it is a noun phrase subtree, join it and add it to the tokens buffer
                if isinstance(phrase, nltk.tree.Tree):
                    noun_phrases = phrase.leaves()
                    tokens.append(" ".join(word for word, _ in noun_phrases))
                # Otherwise keep the word if the user requests it
                elif keep_tokens:
                    word, pos = phrase
                    if pos not in cls.remove_pos:
                        tokens.append(word)

        return tokens

    @classmethod
    def transform(
        cls,
        df: Union[pd.DataFrame, dd.DataFrame],
        text_columns: List[str] = ["text"],
        spacy_model: str = "nl_core_news_lg",
        keep_tokens: bool = False,
    ) -> Union[pd.DataFrame, dd.DataFrame]:
        nlp = spacy.load(
            spacy_model,
            disable=[
                "parser",
                "ner",
                "lemmatizer",
                "textcat",
            ],
        )

        # Use dask to parallelize the keyword extraction over the workers
        if type(df) == dd.DataFrame:
            for text_column in text_columns:
                df[f"_nouns_{text_column}"] = df.map_partitions(
                    lambda _df: _df[text_column].apply(
                        cls.extract_noun_phrases, args=(nlp, keep_tokens)
                    )
                )
        # Pandas apply function
        else:
            for text_column in text_columns:
                df[f"_nouns_{text_column}"] = df[text_column].apply(
                    cls.extract_noun_phrases, args=(nlp, keep_tokens)
                )

        # Return the dataframe with the keywords
        return df
