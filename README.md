# R-and-D-data-management

Explore the PatentsView, Mcirosoft Academic Graph (MAG), and Aminer in the search engine (Elasticsearch) and graph database (Neo4j).

## Requirements

1. Install and start `Neo4j` and `Elasticsearch` in your system.
2. Install python package `neo4j`, `elasticsearch`, `numpy` and `tqdm`.
3. Create a `credential.txt` which contains your neo4j username and password looks like below.

```bash
neo4j_username
neo4j_password
```

## Datasets and Usage

**OAG** can be downloaded from [here](https://www.openacademic.ai/oag/). **Open Academic Graph (OAG)** unifies two billion-scale academic graphs: **Microsoft Academic Graph (MAG)** and **AMiner**.

### MAG V1

In total, 167 files named in pattern  `mag_papers_[0-166].txt` are included in `MAG V1` dataset. 

Running the script below to upload the dataset to Elasticsearch. The index name is set up by `--index` option and is `mag_v1` by default. The script was tested on `Elasitcsearch >= 7.4` using English only publications in `MAG V1`.

```bash
python index_mag_v1.py --inputs [path/mag_papers*.txt]
```

However, it would take too much memory to load those files into the `Neo4j`. One simple solution is to merge and re-split the MAG files by lines to lower the memory requirement but also keep the speed of loading data into neo4j database in batch. A simple script which splits the MAG dataset by 10,000 lines is provided as below. 

```bash
mkdir mag.neo4j
# merge to one file and split
cat [mag_dataset]/* > [mag.neo4j]/mag.all
# split by lines
cd [mag.neo4j] && split -l 10000 mag.all && rm mag.all
```


### Aminer V1

In total, 155 files named in pattern  `aminer_papers_[0-154].txt` are included in `Aminer V1` dataset. Running the script below to upload the dataset to Elasticsearch. The index name is set up by `--index` option and is `aminer_v1` by default. The script was tested on `Elasitcsearch >= 7.4` and publications which have both title and abstract.

```bash
python index_aminer_v1.py --inputs [path/aminer_papers*.txt]
```

### PatentsView

PatentsView provides FREE USPTO patents, which can be downloaded [here](http://www.patentsview.org/download/). You only need to download files which contain patent's context such as `title`, `abstract`, `claim`, `summary`. See table below to choose which one to download.

| Filename | Description |
| -- | -- |
| `claim.tsv` | Claims of patents |
| `brf_sum_text.tsv` | Summary of patents |
| `patent.tsv` | Title and abstract of patents |

`Title`, `abstract`, `claim` and `summary` of a patent are saved in different files as shown in the above table. As a result, one has to join all three files by the patent id column to have all the context fields of a patent available. The most straightforward way is to load the file into memory and join together using `pandas` or `dask`, as long as you have enough memory. An alternative way is to load data into Elasticsearch separately and then join different fields together using Elasticsearch's match function.

```bash
python index_patentsview.py --patent [patent.tsv] --claim [claim.tsv] --summary [brf_sum_text.tsv]
```

For each input file, a temporal index is generated in Elasticsearch which are `patent_tmp`, `claim_tmp` and `summary_tmp` respectively. At last, the above script generates file `es.tmp.json` in the directory where the `[patent.tsv]` is.

