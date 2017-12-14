for i in {0..5}
do
	echo "---------> Generando memoria $i"
	python2 ../../py/memory-generator.py -i ../../../img/da_bossGS.jpg -f mem${i}.txt -c ${i} -s 440
done	
for i in {0..3}
do
	echo "---------> Generando salida $i"
	python2 ../../py/memory-generator.py -i ../../../img/da_bossGS.jpg -f mem${i}_out.txt -c ${i} -s 438 -p
done
