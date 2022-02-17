# -*- coding: utf-8 -*-

import os
import math
import datetime

from tqdm import tqdm
import pandas as pd
from neo4j import GraphDatabase


class Neo4jHandler(object):
    """API interface for manipulations of MAG data in neo4j.

    Parameters
    ----------
    credential : str
        Path to credential file.
    data : str
        Dir to data files.

    Attributes
    ----------
    _username : str
        Username
    _password : str
        Password
    _data : str
        Dir to data files.

    """

    def __init__(self, credential, data):
        super(Neo4jHandler, self).__init__()
        with open(credential, 'r') as ifp:
            lines = ifp.readlines()
            self._username = lines[0].strip()
            self._password = lines[1].strip()
        self.paper_path = os.path.join(data, 'Papers.txt')
        self.ref_path = os.path.join(data, 'PaperReferences.txt')
        self.pids = set()

    def load_mag(self):
        """Load MAG dataset into Neo4j database."""

        self.create_nodes()
        self.create_edges()

    def load_papers(self):
        """Load papers."""

        print('Loading Papers.txt')
        reader = pd.read_csv(self.paper_path, sep='\t', quoting=3, header=None,
                             lineterminator='\n', dtype=str, usecols=[0, 8],
                             chunksize=50000)
        start_date = '2012-01-01'
        for papers in reader:
            papers[8] = pd.to_datetime(papers[8], errors='coerce')
            papers.rename(columns={0: 'pid', 8: 'date'}, inplace=True)
            papers.dropna(inplace=True)
            mask = (papers['date'] >= start_date)
            papers = papers.loc[mask]
            papers['pid'] = papers['pid'].astype('int64')
            self.pids |= set(papers['pid'].tolist())
            yield papers.loc[mask]

    def create_nodes(self):
        """CREATE paper, fos and venue nodes in neo4j database."""

        # graph = GraphDatabase.driver('bolt://localhost:7687',
        #                              auth=(self._username, self._password))
        # total = math.ceil(214012980 / 50000)
        # with graph.session() as session:
        #     session.run(('CREATE CONSTRAINT ON (p:paper) '
        #                  'ASSERT p.pid IS UNIQUE'))
        #     for papers in tqdm(self.load_papers(), total=total):
        #         tx = session.begin_transaction()
        #         self.create_paper_nodes(tx, papers)
        #         tx.commit()
        #     session.run('CREATE INDEX ON :paper(date)')
        total = math.ceil(214012980 / 50000)
        for papers in tqdm(self.load_papers(), total=total):
            pass

    def create_paper_nodes(self, tx, chunk):
        """CREATE paper node."""

        for _, row in chunk.iterrows():
            st = ('CREATE (p:paper {pid: $pid, date: $date})')
            try:
                row['date'] = row['date'].date()
            except ValueError:  # invalid date, e.g., '1968-05-00'
                continue
            if type(row['date']) is not datetime.date:
                continue
            tx.run(st, pid=row['pid'], date=row['date'])

    def load_edges(self):
        """Load references.

        citation edge: p1-[:CITES]->p2

        """

        print('Loading PaperReferences.txt')
        reader = pd.read_csv(self.ref_path, sep='\t', quoting=3, header=None,
                             lineterminator='\n', dtype='int64',
                             chunksize=50000)
        for refs in reader:
            refs.rename(columns={0: 'pid1', 1: 'pid2'}, inplace=True)
            refs.dropna(inplace=True)
            mask = refs.isin(self.pids)
            refs = refs[mask]
            refs.dropna(inplace=True)
            yield refs

    def create_edges(self):
        """MERGE citation edges in neo4j database."""

        graph = GraphDatabase.driver('bolt://localhost:7687',
                                     auth=(self._username, self._password))
        total = math.ceil(1419880598 / 50000)
        with graph.session() as session:
            for refs in tqdm(self.load_edges(), total=total):
                tx = session.begin_transaction()
                self.create_citation_edges(tx, refs)
                tx.commit()

    def create_citation_edges(self, tx, refs):
        for _, row in refs.iterrows():
            st = ('MATCH (a:paper {pid: $pid1}), (b:paper {pid: $pid2}) '
                  'MERGE (a)-[:CITES]->(b)')
            tx.run(st, pid1=int(row['pid1']), pid2=int(row['pid2']))

    def delete_db(self):
        graph = GraphDatabase.driver('bolt://localhost:7687',
                                     auth=(self._username, self._password))
        with graph.session() as session:
            session.run('MATCH (n) DELETE n')

    def get_nodes_count(self):
        graph = GraphDatabase.driver('bolt://localhost:7687',
                                     auth=(self._username, self._password))
        with graph.session() as session:
            count = session.run('MATCH (n) RETURN count(n) as count')
            print(count.values())

    def get_relationships_count(self):
        graph = GraphDatabase.driver('bolt://localhost:7687',
                                     auth=(self._username, self._password))
        with graph.session() as session:
            count = session.run('MATCH (n)-[r]->() RETURN count(r)')
            print(count.values())
