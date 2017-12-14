for i in {0..7}
do
	echo "[*] Testeando memoria $i"
	diff -s mem${i}_out.txt out_mem${i}.txt
done
