This script supports to use `paper`, `fos`, `keyword`, or `venue` as nodes in neo4j database. What to use is totally up to you. Options provided are shown as below.

| Option | Description |
| -- | -- |
| `--paper-as-node` | Add paper nodes and associated edges |
| `--fos-as-node` | Add fos nodes and associated edges |
| `--keyword-as-node` | Add keyword nodes and associated edges |
| `--venue-as-node` | Add venue nodes and associated edges  |

For example, to add paper node into database, simply run the following command. 
```bash
python neo4j_load_mag.py credential.txt [mag.neo4j]/* --paper-as-node
```

New type of nodes and edges can be "appended" to the exsiting database. For example, if you already had a paper as nodes database and find `venue` nodes can also be useful. Simple run
```bash
python neo4j_load_mag.py credential.txt [mag.neo4j]/* --venue-as-node
```
