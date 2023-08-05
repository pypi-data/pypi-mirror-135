#include <stdio.h>
#include <stdlib.h>
#include "bundleTools.h"
#include "BundleTools.c"



int main(int argc, char *argv[]){//21 = 21 puntos
	if(argc!=4){
		printf("./sliceFibers infile outfile nslices\n");
		return -1;
	}

	struct bundle f1,f2;
	
	/*struct bundle {
    int32_t nfibers;
    int32_t* npoints;
    float** points;
    };*/
    
	//struct bundle read_bundle(char* bunfile)
	printf("\nargv1: %s \nargv2: %s \nstring2int(argv3): %i \nok\n",argv[1],argv[2],string2int(argv[3]));
	f1 = read_bundle(argv[1]);
	//struct bundle sliceFiber( struct bundle fibras, int sliceNum)
	f2= sliceFiber( f1, string2int(argv[3]));
    printf("\n23\n");
    //nfibers is okay
    printf("f2.nfibers: %i \n", f2.nfibers);
    printf("f1.npoints: %i \n", *f1.npoints);
    printf("f2.npoints: %i \n", *f2.npoints);
    printf("f1.points: %f \n", **f1.points);
    printf("f2.points: %f \n", **f2.points);
	//void write_bundle(char* outfile, int32_t nfibers, int32_t* npoints, float** points)
	write_bundle(argv[2], f2.nfibers, f2.npoints, f2.points);
    printf("\n26\n");

}







