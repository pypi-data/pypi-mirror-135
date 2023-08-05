from spacy.attrs import ORTH
from spacy.tokens import Doc, DocBin
import dataqa.nlp.spacy_nlp as spacy_nlp


class ModifiedDocBin(DocBin):

    def get_doc(self, doc_id, vocab):
        for string in self.strings:
            vocab[string]
        orth_col = self.attrs.index(ORTH)
        try:
            tokens = self.tokens[doc_id]
            spaces = self.spaces[doc_id]
            words = [vocab.strings[orth] for orth in tokens[:, orth_col]]
            doc = Doc(vocab, words=words, spaces=spaces)
            doc = doc.from_array(self.attrs, tokens)
            doc.cats = self.cats[doc_id]
            return doc
        except:
            return None


class SpacySerialiser:

    def __init__(self):
        self.doc_bin = DocBin(attrs=["POS", "LEMMA", "HEAD", "ENT_TYPE", "ENT_IOB", "DEP"])

    def add_doc(self, text):
        doc = spacy_nlp.nlp(text)
        self.doc_bin.add(doc)

    def get_bytes(self):
        return self.doc_bin.to_bytes()


def serialise_spacy_docs(df):
    # for some reason, I need to add POS to be able to access the lemmas (https://github.com/explosion/spaCy/issues/4824)
    # I also need to add SENT_START to access the sentences (https://github.com/explosion/spaCy/issues/5578)
    doc_bin = DocBin(attrs=["POS", "LEMMA", "HEAD", "ENT_TYPE", "ENT_IOB", "DEP"])
    texts = df.text

    for doc in spacy_nlp.nlp.pipe(texts):
        doc_bin.add(doc)

    bytes_data = doc_bin.to_bytes()
    return bytes_data


def save_spacy_docs(bytes_data, spacy_binary_filepath):
    out_file = open(spacy_binary_filepath, "wb")  # open for [w]riting as [b]inary
    out_file.write(bytes_data)
    out_file.close()


def serialise_save_spacy_docs(df, spacy_binary_filepath):
    bytes_data = serialise_spacy_docs(df)
    save_spacy_docs(bytes_data, spacy_binary_filepath)
    return spacy_binary_filepath


def deserialise_spacy_docs(spacy_binary_filepath):
    with open(spacy_binary_filepath, "rb") as file:
        bytes_data = file.read()
        doc_bin = DocBin().from_bytes(bytes_data)
        data_list = list(doc_bin.get_docs(spacy_nlp.nlp.vocab))
        spacy_docs = [x for x in data_list]

    return spacy_docs


def deserialise_spacy_doc_id(spacy_binary_filepath, doc_id):
    with open(spacy_binary_filepath, "rb") as file:
        bytes_data = file.read()
        doc_bin = ModifiedDocBin().from_bytes(bytes_data)
        doc = doc_bin.get_doc(doc_id, spacy_nlp.nlp.vocab)
        if doc is None:
            raise Exception(f"Could not find document with id {doc_id}")
        return doc


