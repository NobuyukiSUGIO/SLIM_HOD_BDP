#include<stdio.h>
#include <stdlib.h>
typedef unsigned short u16;
typedef unsigned int u32;

main(void) {

    int loop,i1,i2,j,N;
    u16 L, R, R0, R1;
    u16 x, x0, x1, x2, x3;
    u16 y0, y1, y2, y3;
    u16 b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15;
    u16 s[16] = { 0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2 };
    u16 z,temp;
    u16 sumL =0, ALL_sumL = 0;
    u16 sumR =0, ALL_sumR = 0;
    u16 k[33] = { 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0 };

    srand((unsigned int)time(NULL));

    /* Repeat N-times */
    for (N = 0; N < 10; N++) {

        /* Initialization */
        R0 = (rand() << 8) ^ rand();
        for (j = 0; j < 32; j++) {
            /* All subkeys are random */
            k[j] = (rand() << 8) ^ rand();
        }
        sumL = 0;
        sumR = 0;
        L = 0;
        R = 0;
        R1 = 0;

        /* Searching Higher-order differential characteristics */
    	/* i1, i2 are used to span sub-space */
        for (i1 = 0; i1 <= 0xffff; i1++) {
            for (i2 = 0; i2 <= 0x7fff; i2++) {
                L = i1;
                R = R0 ^ i2;
    
                /* R-round SLIM */
                for (loop = 1; loop <= 9; loop++) {
                    x = R ^ k[loop];
                    x3 = x & 0x000f;
                    x2 = (x & 0x00f0) >> 4;
                    x1 = (x & 0x0f00) >> 8;
                    x0 = (x & 0xf000) >> 12;

                    /* S-boxes */
                    y3 = s[x3];
                    y2 = s[x2];
                    y1 = s[x1];
                    y0 = s[x0];

                    /* Permutation */
                    b15 = y3 & 0x1;
                    b14 = (y3 & 0x2) >> 1;
                    b13 = (y3 & 0x4) >> 2;
                    b12 = (y3 & 0x8) >> 3;
                    b11 = y2 & 0x1;
                    b10 = (y2 & 0x2) >> 1;
                    b9 = (y2 & 0x4) >> 2;
                    b8 = (y2 & 0x8) >> 3;
                    b7 = y1 & 0x1;
                    b6 = (y1 & 0x2) >> 1;
                    b5 = (y1 & 0x4) >> 2;
                    b4 = (y1 & 0x8) >> 3;
                    b3 = y0 & 0x1;
                    b2 = (y0 & 0x2) >> 1;
                    b1 = (y0 & 0x4) >> 2;
                    b0 = (y0 & 0x8) >> 3;
                    z = (b0 << 4) ^ (b1 << 13) ^ (b2 << 9) ^ (b3 << 3) ^ (b4 << 7) ^ (b5 << 8) ^ (b6 << 2) ^ (b7 << 15) ^ (b8 << 12) ^ (b9 << 1) ^ (b10 << 6) ^ (b11 << 11) ^ (b12 << 0) ^ (b13 << 14) ^ (b14 << 10) ^ (b15 << 5);
 
                    R1 = L ^ z;

                    /* Swap */
                    L = R;
                    R = R1;
                }
                temp = 0;
                sumL ^= L;
                sumR ^= R;
            }
        }
        ALL_sumL |= sumL;
        ALL_sumR |= sumR;
        printf("%04x %04x\n", ALL_sumL, ALL_sumR);
    }
    return 0;

}