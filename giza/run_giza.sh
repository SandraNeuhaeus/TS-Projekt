cd giza-pp/GIZA++-v2
./plain2snt.out '../europarl_data/Source' '../europarl_data/Target'
cd ../mkcls-v2
./mkcls -p'../europarl_data/Source' -V '../europarl_data/Source.vcb.classes'
./mkcls -p'../europarl_data/Target' -V '../europarl_data/Target.vcb.classes'
cd ../GIZA++-v2
./snt2cooc.out '../europarl_data/Source.vcb' '../europarl_data/Target.vcb' '../europarl_data/Source_Target.snt' > '../europarl_data/Source_Target.cooc'
./GIZA++ -S '../europarl_data/Source.vcb' -T '../europarl_data/Target.vcb' -C '../europarl_data/Source_Target.snt' -CoocurrenceFile '../europarl_data/Source_Target.cooc' -o Result -outputpath '../europarl_data/output'
