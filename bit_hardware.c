/**************************
* Copyright (C) 2023 Advanced Micro Devices, Inc. All Rights Reserved.
* SPDX-License-Identifier: MIT
**************************/
/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */
/*
#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include <math.h>*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "xil_printf.h"
#include "xil_io.h"
#include "xtime_l.h"


#define NUM_POINTS 200
#define MAX_DISKS 200
#define RADIUS 100.0
#define PRINT_POINTS_LIMIT 200

typedef struct {
    float x, y;
    float dx, dy;
} Point;

typedef struct {
    float x, y;
} Disk;

typedef struct {
    float x, y;
    int active;
} ExtrapolatedPoint;

Point points[NUM_POINTS];
ExtrapolatedPoint extrapolated[NUM_POINTS];
Disk disks[MAX_DISKS];
int disk_count = 0;

float distance(float x1, float y1, float x2, float y2) {
    float dx = x1 - x2;
    float dy = y1 - y2;
    return sqrtf(dx * dx + dy * dy);
}

void compute_extrapolated_positions() {
    for (int i = 0; i < NUM_POINTS; i++) {
        extrapolated[i].x = points[i].x + points[i].dx;
        extrapolated[i].y = points[i].y + points[i].dy;
        extrapolated[i].active = 1;
      	points[i].x =  extrapolated[i].x;
        points[i].y =  extrapolated[i].y;
    }
}
void greedy_cover() {
	disk_count = 0;
    while (1) {
        int max_covered = 0;
        int best_index = -1;

        // En fazla noktayı kapsayan noktayı bul
        for (int i = 0; i < NUM_POINTS; i++) {
            if (!extrapolated[i].active) continue;

            int covered = 0;
            for (int j = 0; j < NUM_POINTS; j++) {
                if (extrapolated[j].active &&
                    distance(extrapolated[i].x, extrapolated[i].y,
                             extrapolated[j].x, extrapolated[j].y) <= RADIUS) {
                    covered++;
                }
            }

            if (covered > max_covered) {
                max_covered = covered;
                best_index = i;
            }
        }

        // Uygun nokta bulunamadıysa çık
        if (best_index == -1) break;

        // Disk sınırını kontrol et
        if (disk_count >= MAX_DISKS) {
            xil_printf("Error: Maximum disk limit (%d) reached!\n\r", MAX_DISKS);
            break;
        }

        // Yeni diski ekle
        float cx = extrapolated[best_index].x;
        float cy = extrapolated[best_index].y;
        disks[disk_count].x = cx;
        disks[disk_count].y = cy;
        disk_count++;

        // Kapsanan noktaları devre dışı bırak
        for (int j = 0; j < NUM_POINTS; j++) {
            if (extrapolated[j].active &&
                distance(cx, cy, extrapolated[j].x, extrapolated[j].y) <= RADIUS) {
                extrapolated[j].active = 0;
            }
        }
    }
}
void uart_print_results() {
    //xil_printf("Total Disks Used: %d\n\r", disk_count);
    for (int i = 0; i < NUM_POINTS; i++) {
        printf("%f,%f,%f,%f,%f,%f,", points[i].x,points[i].y,extrapolated[i].x, extrapolated[i].y,disks[i].x,disks[i].y);
        //printf("%f,%f",disks[i].x,disks[i].y);

    }
}

// UART üzerinden orijinal noktaları yazdır (sınırlı sayıda)
void uart_print_points() {
    //xil_printf("Original Points (showing up to %d):\n\r", PRINT_POINTS_LIMIT);
    for (int i = 0; i < PRINT_POINTS_LIMIT && i < NUM_POINTS; i++) {
        //xil_printf("P%d: X = %.1f, Y = %.1f, dx = %.2f, dy = %.2f\n\r",i + 1, points[i].x, points[i].y, points[i].dx, points[i].dy);
        //printf("%f,%f,%f,%f,", points[i].x,points[i].y,points[i].dx,points[i].dy);
    }
}



int main()
{
    init_platform();
    int a;
    XTime t;
    XTime_GetTime(&t);
    srand((unsigned int)t);


     for (int i = 0; i < NUM_POINTS; i++) {
    	 points[i].x = (float)(rand() % 800);                    // 0-799 arası x
         points[i].y = (float)(rand() % 800);                    // 0-799 arası y
         points[i].dx = ((float)(rand() % 3200) - 1600) / 100.0f; // -2.0 ile +2.0
         points[i].dy = ((float)(rand() % 3200) - 1600) / 100.0f; // -2.0 ile +2.0
     }

     /*for (int i = 0; i < NUM_POINTS; i++) {
         xil_printf("%f\n\r",points[i].x);
     }*/

     //xil_printf("Greedy Cover with Extrapolated Positions\n\r");
for(int i= 0; i<10; i++){
     // Algoritmayı çalıştır
     compute_extrapolated_positions(); // Tahmini konumları hesapla
     greedy_cover();                   // Diskleri yerleştir
     //uart_print_points();             // Orijinal noktaları yazdır
     uart_print_results();            // Disk merkezlerini yazdır
     for(int r=0;r<MAX_DISKS;r++){
    	 disks[r].x = 0;
    	 disks[r].y = 0;


     }
}
     //xil_printf("DONE.\n\r");

     // Gömülü sistemde çalışmaya devam et (hata ayıklama için koşullu)
     /*
     #ifdef DEBUG
     return 0; // Hata ayıklama modunda programı sonlandır
     #else
     while (1); // Normal modda sonsuz döngü
     #endif
*/

    //print("Hello World\n\r");
    //print("Successfully ran Hello World application");
    cleanup_platform();
    return 0;
}
