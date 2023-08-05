"""

Graph / Network Analysis

"""

import emoji
import networkx as nx
import spacy

from easyexplore.data_import_export import DataImporter
from easyexplore.utils import SPECIAL_CHARACTERS
from typing import List


class GraphTextAnalysisException(Exception):
    """
    Class for handling exception for class GraphTextAnalysis
    """
    pass


class GraphTextAnalysis:
    """
    Class for analyse text data using graph / network analysis algorithms
    """
    def __init__(self,
                 file_path: str = None,
                 as_data_frame: bool = False,
                 feature: str = None,
                 graph: nx = None,
                 text_pre_processing: bool = True,
                 **kwargs
                 ):
        """
        :param file_path: str
            Complete file path of the text data

        :param graph: nx
            Network graph

        :param text_pre_processing: bool
            Pre-process text data

        :param kwargs: dict
            Key-word arguments
        """
        self.file_path: str = file_path
        self.graph: nx = graph
        self.text_pre_processing: bool = text_pre_processing
        self.kwargs: dict = kwargs
        if self.file_path is None:
            if self.graph is None:
                raise GraphTextAnalysisException('No file path nor graph were given')
        else:
            _text_data: str = DataImporter(file_path=self.file_path,
                                           as_data_frame=False,
                                           use_dask=False,
                                           create_dir=False,
                                           cloud=self.kwargs.get('cloud'),
                                           bucket_name=self.kwargs.get('bucket_name'),
                                           region=self.kwargs.get('region')
                                           ).file(table_name=self.kwargs.get('table_name'))
            if self.text_pre_processing:
                _pre_processed_text_data: str = self._pre_process_text_data(text_data=_text_data)
                self._generate_graph(text_data=_pre_processed_text_data)
            else:
                self._generate_graph(text_data=_text_data)

    def _generate_graph(self, text_data: str):
        """
        Generate graph from data set
        """
        # get graph nodes
        _nodes: List[str] = text_data.split(' ')
        # get graph edges
        _edges: List[List[str]] = []
        for i in range(len(_nodes) - 1):
            # for every word and the next in the sentence
            pair = [_nodes[i], _nodes[i+1]]
            # only add unique bigrams
            if pair not in _edges:
                _edges.append(pair)
        # create graph structure with NetworkX
        self.graph = nx.Graph()
        self.graph.add_nodes_from(_nodes)
        self.graph.add_edges_from(_edges)

    @staticmethod
    def _pre_process_text_data(text_data: str,
                               decap: bool = True,
                               numbers: bool = True,
                               stop_words: bool = True,
                               special_chars: bool = True,
                               punct: bool = True,
                               pron: bool = True,
                               web: bool = True,
                               entity: bool = True,
                               lemmatizing: bool = True
                               ) -> str:
        """
        Pre-process text data

        :param text_data: str
            Text data to pre-process

        :param decap: bool
            Whether to decapitulate text or not

        :param numbers: bool
            Whether to remove numbers from text or not

        :param stop_words: bool
            Whether to remove stop-words from text or not

        :param special_chars: bool
            Whether to remove all special characters from text or not

        :param punct: bool
            Whether to remove punctuation from text or not

        :param pron: bool
            Whether to remove pronouns from text or not

        :param web: bool
            Whether to remove all web elements like url or email from text or not

        :param entity: bool
            Whether to remove recognized entities from text or not

        :param lemmatizing: bool
            Lemmatize (trim words to their word-stem) text or not

        :return: str
            Pre-processed text data
        """
        _text_data: str = str(text_data).lower() if decap else text_data
        _model = spacy.load('de_core_news_sm')
        _nlp = _model(_text_data)
        _pre_processed_text_data: List[str] = []
        for token in _nlp:
            if token in emoji.UNICODE_EMOJI.get('de'):
                _pre_processed_text_data.append(emoji.demojize(string=token, use_aliases=False))
            if token.pos_ in ['ADJ', 'ADV']:
                pass
            if token.pos_ == 'VERB':
                pass
            if token.pos_ == 'NOUN':
                pass
            if (numbers and token.is_digit) or (numbers and token.like_num):
                continue
            if stop_words and token.is_stop:
                continue
            if special_chars and token.text in SPECIAL_CHARACTERS:
                continue
            if punct and token.is_punct:
                continue
            if pron and token.lemma_ == '-PRON-':
                continue
            if (web and token.like_url) or (web and token.like_email):
                continue
            if entity and token.ent_type > 0:
                continue
            if lemmatizing:
                _pre_processed_text_data.append(token.lemma_)
            else:
                _pre_processed_text_data.append(token.text)
        return ' '.join(_pre_processed_text_data)

    def get_shortest_path(self, algorithm: str = 'dikstra'):
        """
        Get shortest path of graph

        :param algorithm: str
            Name of the algorithm to use:
                -> dikstra: Dikstra
                -> a_star: A*
                -> bellman_ford: Bellman-Ford
                -> floyd_warshall: Floyd-Warshall

        :return:
        """
        if algorithm == 'dikstra':
            return nx.dijkstra_path(G=self.graph, source=None, target=None, weight='distance')
        else:
            raise GraphTextAnalysisException(f'Algorithm ({algorithm}) not supported')
