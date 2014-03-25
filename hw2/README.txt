Sampling into two 100 sentences files
-s es-en\europarl-v7.es-en.es Spanish -t es-en\europarl-v7.es-en.en English -m sample -x 100

Training with divergence condition being 1, and number of maximum iteration being 30
-s es-en\europarl-v7.es-en.es.100.sampling Spanish -t es-en\europarl-v7.es-en.en.100.sampling English -D es-en\europarl-v7.es-en.es.100.dict es-en\europarl-v7.es-en.en.100.dict -m train -d model_100.npy -i 30 -c 1 -n 1

Testing with fabricated input
-s es-en\europarl-v7.es-en.es.100.test Spanish -t es-en\europarl-v7.es-en.en.100.test English -D es-en\europarl-v7.es-en.es.100.dict es-en\europarl-v7.es-en.en.100.dict -m evaluate -d model_100.npy -n 1