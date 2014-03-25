Sampling into two 100 sentences files
-s es-en\europarl-v7.es-en.es Spanish -t es-en\europarl-v7.es-en.en English -m sample -x 100


-s es-en\europarl-v7.es-en.es.100.sampling Spanish -t es-en\europarl-v7.es-en.en.100.sampling English -D es-en\europarl-v7.es-en.es.100.dict es-en\europarl-v7.es-en.en.100.dict -m train -d model_100.mod -i 10