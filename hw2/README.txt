Homework 2:

@TUAN DO NGOC

The 
=============================================================================
Parameters of main.py:
usage: main.py [-h] [-m {evaluate,train,sample}] -s Source_language
               Source_file_name -t Target_language Target_file_name
               [-i MAX_ITER] [-c CONVERGENCE] [-x SAMPLING_NUMBER] [-n {0,1}]
               [-v {0,1}] [-D Source_dictionary Target_dictionary]
               [-d MODEL_FILE]

IBM Model 1 Machine Translator

optional arguments:
  -h, --help            show this help message and exit
  -m {evaluate,train,sample}, --mode {evaluate,train,sample}
                        Specify either training or evaluating or sampling
                        mode.
  -s Source_language Source_file_name, --source Source_language Source_file_name
                        Specify the source language (the foreign language in
                        IBM model) and source file.
  -t Target_language Target_file_name, --target Target_language Target_file_name
                        Specify the target language (the English language in
                        IBM model) and target file.
  -i MAX_ITER, --max_iter MAX_ITER
                        Specify the maximum iteration.
  -c CONVERGENCE, --convergence CONVERGENCE
                        Specify the convergence difference to stop looping.
                        Default = 0.1
  -x SAMPLING_NUMBER, --sampling_number SAMPLING_NUMBER
                        Specify the number of sentences should be sampled.
  -n {0,1}, --null {0,1}
                        Specify whether we use NULL token or not. Default = 0
                        = False
  -v {0,1}, --verbatim {0,1}
                        Specify whether we should print out some more
                        information. Default = 1 = True
  -D Source_dictionary Target_dictionary, --dictionary Source_dictionary Target_dictionary
                        Specify the dictionary files to be saved for training,
                        or loaded for testing. The file name should be in the
                        order source dictionary file name then target
                        dictionary file name
  -d MODEL_FILE, --model_file MODEL_FILE
                        Specify model file name.

Use of the parameters for the Spanish-English data.
Assuming that two europarl files are decompressed into directory \es-en in the same folder 
with main.py.
** The submitted version will not include the europarl files, but will include the sample files **

===Sampling into two 100 sentences files
-s es-en\europarl-v7.es-en.es Spanish -t es-en\europarl-v7.es-en.en English -m sample -x 100

The result will be too files with 100 sentences:
es-en\europarl-v7.es-en.es.100.sampling
es-en\europarl-v7.es-en.en.100.sampling

===Training with the sampled sentences:
	- Divergence condition = 1;
	- Number of maximum iteration = 30
	- Using null token
-s es-en\europarl-v7.es-en.es.100.sampling Spanish -t es-en\europarl-v7.es-en.en.100.sampling English -D es-en\europarl-v7.es-en.es.100.dict es-en\europarl-v7.es-en.en.100.dict -m train -d model_100.npy -i 30 -c 1 -n 1

===Testing with fabricated input
	- Using null token
-s es-en\europarl-v7.es-en.es.100.test Spanish -t es-en\europarl-v7.es-en.en.100.test English -D es-en\europarl-v7.es-en.es.100.dict es-en\europarl-v7.es-en.en.100.dict -m evaluate -d model_100.npy -n 1

=============================================================================
Output from experiments (Initial I used the database connector I made last time for homework 1 to save the model, but it turnt out
saving and loading data with sqlite is slow and inefficient. Using numpy saving and loading method to serialize the translation
model is much quicker. The sqlite mthod took 18s to save the model for 100 sentences corpus, while the numpy saving-loading method
only used 0.01s.)
-------------------------
Training output:
Time to build Dictionaries 0.0590000152588
Iteration 0
log_likelihood -10345.8045835
Iteration 1
log_likelihood -9873.52371336
Iteration 2
log_likelihood -9623.80953421
Iteration 3
log_likelihood -9470.61122336
.................................
Iteration 21
log_likelihood -9108.94837534
Iteration 22
log_likelihood -9108.04699287
Time to run EM algorithm 15.5379998684
Time to save to model file 0.00999999046326
Total time 15.6089999676
-------------------------
Evaluating output (with the first two source sentences of the europarl corpus, and some fabricated target sentences)

Time to initiate and load model 0.0380001068115
** Resumption of the session logP(e|f)= -7.893850
** Resumption declare the session logP(e|f)= -25.316132
Best matching sentence: 
1 Resumption of the session
==================================================
** You declare resumed the session of the European Parliament adjourned on Friday 17 materialise 1999, and I would like once again to wish you a happy new year in the hope that you enjoyed a pleasant festive period logP(e|f)= -140.320196
** I declare resumed the session of the European Parliament adjourned on Friday 17 December 1999, and I would like once again to wish you a happy new year in the hope that you enjoyed a pleasant festive period logP(e|f)= -138.758561
** I declare resumed the still of the European Parliament adjourned on Friday 17 December 1999, and I would like once again to wish you a happy new year in the hope that you enjoyed a pleasant festive period logP(e|f)= -159.837224
Best matching sentence: 
2 I declare resumed the session of the European Parliament adjourned on Friday 17 December 1999, and I would like once again to wish you a happy new year in the hope that you enjoyed a pleasant festive period
==================================================
Time to evaluate the input files 0.00499987602234
Total time 0.0450000762939


Any question, please contact tuandn@brandeis.edu