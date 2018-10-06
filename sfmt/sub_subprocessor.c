#include <math.h>
#include <stdio.h>
#define _XOPEN_SOURCE 600
#include <stdlib.h>
#include <stdint.h>
#include "SFMT.h"
#include <unistd.h>

void roll(int* values, size_t times, int min, int max) 
{
    int i, j, seed;
    int R_SIZE = 2 * times;
    int size;
    uint64_t *array;
    sfmt_t sfmt;
    
    // Initializing seed to systime.
    seed = time(NULL);
    // Setting size to minimum, if not large enough, set size to
    // twice required integers for roll.
    size = sfmt_get_min_array_size64(&sfmt);
    if (size < R_SIZE) {
        size = R_SIZE;
    }
    // Assign memory using posix_memalign for optimization.
    posix_memalign((void **)&array, 16, sizeof(double) * size);
    
    // Initiating SFMT then filling array.
    sfmt_init_gen_rand(&sfmt, seed);
    sfmt_fill_array64(&sfmt, array, size);
    
    // Converting each array to 0-1 number then converting that
    // to required range for die results.
    j = 0;
    for (i = 0; i < times; i++) {
        values[i] = (int)floor(sfmt_to_res53(array[j++]) * (max-min+1) + min);
    }
    
    free(array);
}
