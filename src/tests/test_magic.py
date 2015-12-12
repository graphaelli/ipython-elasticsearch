from elasticsearch.magic import ElasticsearchMagics


# globally available when running under ipython
ip = get_ipython()


def test_load_ext():
    elasticsearchmagic = ElasticsearchMagics(shell=ip)
    ip.register_magics(elasticsearchmagic)


def test_run_line_magic():
    ip.run_line_magic('elasticsearch', None)
    ip.run_line_magic('elasticsearch', 'http://foo')
