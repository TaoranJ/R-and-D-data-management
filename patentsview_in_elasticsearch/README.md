## Load dataset to Elasticsearch

By default, Elasticsearch supports to insert file less than `100MB`. So if you don't want to change the default configuration of Elasticsearch, use the script below to split original files to smaller ones
```bash
mkdir [patent.es] && split -d -l 5000 [es.tmp.json] [patent.es]/patent. && rm [es.tmp.json]
```
where `[es.tmp.json]` is data generated in above step.

Finally, it's time to load dataset into Elasticsearch. 

```bash
bash load_data.sh [patent.es]
```
where `[patent.es]` is the directory name used in the last step.

## Clean up temporal indices

The following command lists all indices in your Elasticsearch.
```bash
curl -X GET "localhost:9200/_cat/indices?v&s=index:asc"
```

The result should have three temporal indices we build in step [Indexing PatentsView data](#idexing-patentsview-data), which are `patent_tmp`, `claim_tmp`, and `summary_tmp`. And most importantly, the patents data should be in Elasticsearch under the name `patentsview`. You can quickly do some simple search on it to test if it works as expected. If everything goes well, then it's safe to delete those temporal indices to save space in disk.
```bash
curl -X DELETE "localhost:9200/patent_tmp"
curl -X DELETE "localhost:9200/claim_tmp"
curl -X DELETE "localhost:9200/summary_tmp"
```
