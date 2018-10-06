all: sub_subprocessor.so

sub_subprocessor.so : sub_subprocessor.c
	gcc -O3 -msse2 -DHAVE_SSE2 -DSFMT_MEXP=2281 -lm -Wl,-export-dynamic --shared -o sub_subprocessor.so -fPIC SFMT.c sub_subprocessor.c

clean:
	rm ./sub_subprocessor.so
