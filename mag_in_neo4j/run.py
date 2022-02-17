# -*- coding: utf-8 -*-

import argparse

from neo4j_handler import Neo4jHandler


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('credential', help='credential.txt')
    pparser.add_argument('ipath', help='Path to mag files')
    args = pparser.parse_args()
    db = Neo4jHandler(args.credential, args.ipath)
    # db.get_nodes_count()
    # db.get_relationships_count()
    # db.load_mag()
