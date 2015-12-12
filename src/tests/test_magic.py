import responses

from elasticsearch.magic import ElasticsearchMagics


# globally available when running under ipython
ip = get_ipython()


def test_load_ext():
    elasticsearchmagic = ElasticsearchMagics(shell=ip)
    ip.register_magics(elasticsearchmagic)


def test_run_line_magic():
    ip.run_line_magic('elasticsearch', None)
    ip.run_line_magic('elasticsearch', 'http://foo')

def test_cell_magic_json_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 'http://magic.mock:1234/',
                 body="""{
                     "name" : "Slither",
                     "cluster_name" : "elasticsearch",
                     "version" : {
                         "number" : "2.0.0",
                         "build_hash" : "de54438d6af8f9340d50c5c786151783ce7d6be5",
                         "build_timestamp" : "2015-10-22T08:09:48Z",
                         "build_snapshot" : false,
                         "lucene_version" : "5.2.1"
                     },
                     "tagline" : "You Know, for Search"
                 }""",
                 content_type='application/json; charset=UTF-8',
                 status=200,
        )
        ip.run_cell_magic('elasticsearch', 'http://magic.mock:1234/', 'GET /')


def test_cell_magic_text_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 'http://magic.mock:1234/_cat',
                 body="""=^.^=
                     /_cat/allocation
                     /_cat/shards
                     /_cat/shards/{index}
                     /_cat/master
                     /_cat/nodes
                     /_cat/indices
                     /_cat/indices/{index}
                     /_cat/segments
                     /_cat/segments/{index}
                     /_cat/health
                  """,
                 content_type='text/plain; charset=UTF-8',
                 status=200,
        )
        ip.run_cell_magic('elasticsearch', 'http://magic.mock:1234/', 'GET /_cat')
