#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include "bundleTools.h"

struct bundle read_bundle(char* bunfile)
{
    int i, j;
    struct bundle fas;

    FILE *fb;
    fb = fopen(bunfile, "r");
    if (fb == NULL) {fputs ("File error",stderr); exit (1);}

    char buffer[100];   //buffer para la linea
    fgets(buffer,100,fb);//Lecturas para llegar la liena 5 del archivo
    fgets(buffer,100,fb);
    fgets(buffer,100,fb);
    fgets(buffer,100,fb);
    fgets(buffer,100,fb);
    int index_i=0;//Indice posición inicial de los numeros
    for(i=0;i<sizeof(buffer);i++)
    {
        if(buffer[i]>=48 && buffer[i]<=57)//Detecta cuando hay un número en la línea leída y guarda el índice
        {
            index_i=i;
            break;
        }
    }
    int index_f=index_i;//Indice posición final de los números
    int32_t nfibers=0;   // variable para numero de fibras
    while(buffer[index_f]!=44)//Mientras no se detecte una coma aumenta el otro indice de la pos final
    {
        index_f++;
    }
    for(i=0;i<(index_f-index_i);i++)
    {
        nfibers+=(buffer[index_i+i]-48)*pow(10,(index_f-(index_i+i))-1);
    }
    fclose(fb);

    fas.nfibers = nfibers;

    char* bunfileb;
    bunfileb = masdata(bunfile);

    FILE *fp;
    fp = fopen(bunfileb, "rb");
    if (fp == NULL) {fputs ("File error",stderr); exit (1);}

    float** points; // puntero a cada fibra
    points = (float**) malloc (nfibers*sizeof(float*));

    int32_t* npoints;//Puntero para la cantidad de puntos de cada fibra
    npoints=(int32_t*) malloc(nfibers*sizeof(int32_t));//Memoria para cada fibra

    for ( i = 0; i < nfibers; i++ )//Itera en cantidad de fibras
    {
       fread(npoints+i,sizeof(int32_t),1,fp);//Lee primer elemento(cantidad de funtos)

       points[i]=(float*) malloc((*(npoints+i))*3*sizeof(float));//Asigna memoria para toda una fibra
       if (points[i] == NULL) {fputs ("Memory error",stderr); exit (2);}
       fread( points[i], sizeof(float), *(npoints+i)*3, fp );//Lee todos los puntos de la fibra

    }
    fas.npoints=npoints;
    fas.points=points;
    fclose(fp);
    return fas;
}

void write_bundle(char* outfile, int32_t nfibers, int32_t* npoints, float** points)
{
    char par1[] = "attributes = {\n    'binary' : 1,\n    'bundles' : ['fibers', 0],\n    'byte_order' : 'DCBA',\n    'curves_count' : ";
    char par2[] = ",\n    'data_file_name' : '*.bundlesdata',\n    'format' : 'bundles_1.0',\n    'space_dimension' : 3\n  }";

    int32_t len=strlen(int2string(nfibers))+1;

    FILE *fw;
    fw = fopen(outfile,"w");

    fwrite(par1,sizeof(char),strlen(par1),fw);
    fwrite(int2string(nfibers),sizeof(char),len,fw);
    fseek(fw, -1 , SEEK_CUR);
    fwrite(par2,sizeof(char),strlen(par2),fw);

    fclose(fw);
    char* outfileb;
    outfileb=masdata(outfile);

    FILE *fwb;
    fwb = fopen(outfileb,"wb");
    int i;
    for(i=0;i<nfibers;i++)
    {
        fwrite(npoints+i,sizeof(int32_t),1,fwb);
        fwrite(points[i],sizeof(float),*(npoints+i)*3,fwb);
    }

    fclose(fwb);
}
char* masdata(char* bunfile)
{
    int cont=0,i;
    char data[5]="data";
    char* bunfileb=malloc(sizeof(char)*(strlen(bunfile)+strlen(data)));

    while(bunfile[cont]!=NULL)
    {
        bunfileb[cont]=bunfile[cont];//Iguala string excepto el nulo
        cont++;
    }
    for(i=0;i<sizeof(data);i++)
    {
        bunfileb[cont]=data[i];//Le agrega data al final
        cont++;
    }
    return bunfileb;
}

char* int2string(int32_t si)
{
    int32_t exp,base,i;
    for(exp=0;;exp++)
    {
        base=pow(10,exp);
        if(base==99){base++;}
        if(si<base)
        {
            exp--;
            base=pow(10,exp);
            if(base==99){base++;}
            break;
        }
    }

    char* cad=(char*)malloc(sizeof(char)*(exp+1));
    for(i=0;i<exp+1;i++)
    {
        cad[i]=(char)((si/base)%10 +48);
        base=pow(10,exp-(i+1));
        if(base==99){base++;}
    }
    cad[i]=NULL;
    return cad;
}

struct bundle sliceFiber( struct bundle fibras, int sliceNum)
{
    struct bundle sB;
    sB.nfibers = fibras.nfibers;
    sB.npoints = (int32_t*) malloc(sB.nfibers*sizeof(int32_t));
    sB.points = (float**) malloc (sB.nfibers*sizeof(float*));

    int k;
    for(k=0;k<fibras.nfibers;k++)
    {
        int fSize = 1;
        *(sB.npoints+k) = sliceNum;
        sB.points[k] = (float*) malloc((*(sB.npoints+k))*3*sizeof(float));
        *(sB.points[k]+0) = *(fibras.points[k]+0);
        *(sB.points[k]+1) = *(fibras.points[k]+1);
        *(sB.points[k]+2) = *(fibras.points[k]+2);

        float fiberlength = 0;
        float acc_length[*(sB.npoints+k)];
        acc_length[0] = 0;

        int j;
        for (j = 0; j < *(fibras.npoints+k)-3; j++)
        {
            fiberlength += sqrt( pow(*(fibras.points[k]+(j*3)) - *(fibras.points[k]+(j*3)+3),2) +
                                 pow(*(fibras.points[k]+(j*3)+1) - *(fibras.points[k]+(j*3)+1+3),2) +
                                 pow(*(fibras.points[k]+(j*3)+2) - *(fibras.points[k]+(j*3)+2+3),2));

            acc_length[j + 1] = fiberlength;
        }
        float step = fiberlength / (float)(sliceNum-1);
        float currentLength = step;

        int currentInd = 0;

        float lengthtmp = fiberlength - step*0.5;

        while ( currentLength < lengthtmp)
        {
            if (acc_length[currentInd] < currentLength)
            {
                while (acc_length[currentInd] < currentLength)
                {
                    currentInd++;
                }
                currentInd--;
            }

            float fact = (currentLength - acc_length[currentInd])/(acc_length[currentInd + 1] - acc_length[currentInd]);
            if ( fact > 0.000001 )
            {
                *(sB.points[k] + fSize*3 + 0) = (*(fibras.points[k] + (int)(currentInd + 1)*3) - *(fibras.points[k] + (int)currentInd*3))*fact + *(fibras.points[k] + (int)currentInd*3);
                *(sB.points[k] + fSize*3 + 1) = (*(fibras.points[k] + (int)(currentInd + 1)*3 + 1) - *(fibras.points[k] + (int)currentInd*3 + 1))*fact + *(fibras.points[k] + (int)currentInd*3 + 1);
                *(sB.points[k] + fSize*3 + 2) = (*(fibras.points[k] + (int)(currentInd + 1)*3 + 2) - *(fibras.points[k] + (int)currentInd*3 + 2))*fact + *(fibras.points[k] + (int)currentInd*3 + 2);
                fSize++;
            }
            else
            {
                 *(sB.points[k] + fSize*3 + 0) = *(fibras.points[k] + (int)currentInd*3);
                 *(sB.points[k] + fSize*3 + 1) = *(fibras.points[k] + (int)currentInd*3 + 1);
                 *(sB.points[k] + fSize*3 + 2) = *(fibras.points[k] + (int)currentInd*3 + 2);
                fSize++;
            }

            currentLength += step;
        }

        *(sB.points[k] + fSize*3) = *(fibras.points[k] + (*(fibras.npoints + k) - 1)*3);
        *(sB.points[k] + fSize*3 + 1) = *(fibras.points[k] + (*(fibras.npoints + k) - 1)*3 + 1);
        *(sB.points[k] + fSize*3 + 2) = *(fibras.points[k] + (*(fibras.npoints + k) - 1)*3 + 2);
        fSize++;
    }
    return sB;

}

int32_t string2int(char* si)
{
    int i,j;
    int32_t ent=0;
    for(i=0;si[i]!=NULL;i++){}

    for(j=0;j<i;j++)
    {
        ent+=(si[j]-48)*pow(10,i-j-1);
    }
    return ent;
}

float** fiberDistanceMax(struct bundle f)
{
    // Calcula la distancia máxima entre todas las fibras de un bundle
    // Todas deben tener la misma cantidad de puntos

    float** matriz = (float**) malloc (f.nfibers*sizeof(float*));
    float distancias[*(f.npoints)],distancias1[*(f.npoints)],maximo,maximo1,distancia;

    int i,j,k,cont=1;
    for(i=0;i<f.nfibers;i++)
    {
        matriz[i] = (float*) malloc(cont*sizeof(float));//Asigna memoria para toda una fibra
        for(j=0;j<cont;j++)
        {
            for(k=0;k<*(f.npoints);k++)
            {
                distancias[k] = pow(*(f.points[i]+(k*3)+0) - *(f.points[j]+(k*3)+0),2) +
                                pow(*(f.points[i]+(k*3)+1) - *(f.points[j]+(k*3)+1),2) +
                                pow(*(f.points[i]+(k*3)+2) - *(f.points[j]+(k*3)+2),2);
                if(k==0 || distancias[k]>maximo)
                {
                    maximo = distancias[k];
                }

                distancias1[k] = pow(*(f.points[i]+((*(f.npoints)-k-1)*3)+0) - *(f.points[j]+(k*3)+0),2) +
                                 pow(*(f.points[i]+((*(f.npoints)-k-1)*3)+1) - *(f.points[j]+(k*3)+1),2) +
                                 pow(*(f.points[i]+((*(f.npoints)-k-1)*3)+2) - *(f.points[j]+(k*3)+2),2);
                if(k==0 || distancias1[k]>maximo1)
                {
                    maximo1 = distancias1[k];
                }
            }
            if(maximo<maximo1){distancia=maximo;}
            else{distancia=maximo1;}

            *(matriz[i]+j) = distancia;
        }
        cont++;
    }

    return matriz;
}
//_____________________________________________________________________________vvvvvvvvvvvvvvvvvvvvvvvv

float** fiberDistanceMax2bun(struct bundle f1,struct bundle f2)
{
    // Calcula la distancia máxima entre todas las fibras de un bundle
    // Todas deben tener la misma cantidad de puntos
int i,j,k,cont=1;

float** matriz = (float**) malloc (f1.nfibers*sizeof(float*));
	for(int i=0;i<f1.nfibers;i++)
	{
		matriz[i]=(float *)malloc (f2.nfibers*sizeof(float));
	}
	
    float distancias[*(f1.npoints)],distancias1[*(f1.npoints)],maximo,maximo1,distancia;

    
    for(i=0;i<f1.nfibers;i++)
    {
        matriz[i] = (float*) malloc(f2.nfibers*sizeof(float));//Asigna memoria para toda una fibra
        for(j=0;j<f2.nfibers;j++)
        {
            for(k=0;k<*(f1.npoints);k++)
            {
                distancias[k] = pow(*(f1.points[i]+(k*3)+0) - *(f2.points[j]+(k*3)+0),2) +
                                pow(*(f1.points[i]+(k*3)+1) - *(f2.points[j]+(k*3)+1),2) +
                                pow(*(f1.points[i]+(k*3)+2) - *(f2.points[j]+(k*3)+2),2);
                if(k==0 || distancias[k]>maximo)
                {
                    maximo = distancias[k];
                }

                distancias1[k] = pow(*(f1.points[i]+((*(f1.npoints)-k-1)*3)+0) - *(f2.points[j]+(k*3)+0),2) +
                                 pow(*(f1.points[i]+((*(f1.npoints)-k-1)*3)+1) - *(f2.points[j]+(k*3)+1),2) +
                                 pow(*(f1.points[i]+((*(f1.npoints)-k-1)*3)+2) - *(f2.points[j]+(k*3)+2),2);
                if(k==0 || distancias1[k]>maximo1)
                {
                    maximo1 = distancias1[k];
                }
            }
            if(maximo<maximo1){distancia=maximo;}
            else{distancia=maximo1;}

            *(matriz[i]+j) = distancia;
        }
    }

    return matriz;
}
//_____________________________________________________________________________^^^^^^^^^^^^^^^^^^^^{

struct bundle bundleSampler(struct bundle fibras, float sampler, int modo)//modo=0 para porcentaje y modo=1 numero de fibras
{
    struct bundle nuevo;

    if(modo==0)
    {
        if(sampler>=0 && sampler<=100)
        {
            nuevo.nfibers=(int32_t)fibras.nfibers*sampler/100.0;
        }
        else
        {
            printf("Porcentaje supera el 100%");
        }
    }
    else
    {
        if(modo==1)
        {
            if(sampler<=fibras.nfibers)
            {
                nuevo.nfibers=sampler;
            }
            else
            {
                printf("Cantidad de fibras ingresada supera la cantidad de fibras del bundle");
            }
        }
        else
        {
            printf("Modo incorrecto. Lo valido es: modo=0 para porcentaje y modo=1 numero de fibras\n");
        }
    }

    nuevo.npoints=(int32_t*) malloc(nuevo.nfibers*sizeof(int32_t));
    nuevo.points = (float**) malloc (nuevo.nfibers*sizeof(float*));

    srand(time(NULL));
    int i, j, ales[nuevo.nfibers];
    for(i=0;i<nuevo.nfibers;i++)
    {
        ales[i]=-1;
    }

    for(i=0;i<nuevo.nfibers;i++)
    {
        int flag=1,ale;
        while(flag)
        {
            ale=((float)rand()/RAND_MAX)*fibras.nfibers;
            int cont=0;
            for(j=0;j<nuevo.nfibers;j++)
            {
                if(ale!=ales[j]){cont++;}
            }
            if(cont==nuevo.nfibers){flag=0;}
        }
        ales[i]=ale;

        *(nuevo.npoints+i)=*(fibras.npoints + ale);
        nuevo.points[i]=fibras.points[ale];
    }
    return nuevo;
}
