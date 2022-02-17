# MAG in neo4j

## Requirement

1. Install and start `neo4j`
2. Use `python>=3.4`. 
3. `pip install neo4j numpy`
4. Create a `credential.txt` which contains your neo4j username and password looks like below.
```bash
neo4j_username
neo4j_password
```

## MAG_V1

### Preprocessing

The original MAG dataset has 167 files. 

Based on your application, you may want to do some filtering such as securing papers written in English.

It takes much memory to load a file for further processing. So if you only have limited memory available, and don't want to write too much code to load a file chunk by chunk. One simple solution is to further split the MAG files by lines to lower the memory requirement but also keep the speed of loading data into neo4j database in batch. A simple script which splits the MAG dataset by 10,000 lines is provided as below. 

```bash
mkdir mag.neo4j
# merge to one file and split
cat [mag_dataset]/* > [mag.neo4j]/mag.all
# split by lines
cd [mag.neo4j] && split -l 10000 mag.all && rm mag.all
```

### Load dataset

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
