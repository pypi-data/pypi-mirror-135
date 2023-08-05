//Author: Narciso Lopez Lopez

#include <iostream>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <cstdlib>
#include <vector>
#include <climits>
#include <algorithm>
#include <ctime>

#define IDXK_SIZE 1024*1024

using namespace std;

static vector<int> corr;
static vector<int> scorr;
static vector<int> acorr;

vector<vector<int>> edges;
vector<float> weights;
vector<float> height;
vector<int> pop;
vector<int> cc;
vector<int> father;

struct smax{
    float value;
    int arg;
};

struct smax floatmax(vector<float> &dvector, int lenght){
    int i;
    struct smax sm;
    sm.value = dvector[0];
    sm.arg = 0;
    for (i = 1; i < lenght; i  += 1)
    {
        if(dvector[i]>sm.value){
            sm.value = dvector[i];
            sm.arg = i;
        }
    }
    return sm;
}

int comp(int a,int b){
    return a<b;
}

int compind(int a, int b){
    return corr[a] < corr[b];
}

int main( int argc, const char **argv ){

    if(argc != 3){
        cout << "./getAverageLinkHFromGraphFile affinityGraph averageLinkHC" << endl;
        cout <<  "affinityGraph: input file .txt with affinities graph" << endl;
        cout <<  "averageLinkHC: output file .txt with dendogram" << endl;
        return -1;
    }

    clock_t t_start= clock();

    int nV, nE = 0;
    int maxv = 0;

    ifstream is( argv[1]);

    if( is.fail() ){
        throw runtime_error( "Error while opening input file ...\n");
    }
    else{
        cout<< "File Opened" << endl <<flush;
        is >> nV;
        is >> nE;
        cout<< "Edges: " << nE
            << " Vertices: "<< nV << endl <<flush;

        maxv = 2*nV;

        edges.resize(2);
        edges[0].resize(nE);
        edges[1].resize(nE);
        weights.resize(2*nE);
        height.resize(maxv);
        father.resize(maxv);
        pop.resize(maxv);

        for (int i = 0; i < maxv; i += 1){
            pop[i] = 1;
            height[i] = INT_MAX;
            father[i] = i;
        }
///////////////////////////////////////////

        // Read
        for (int i = 0; i < nE; i += 1){
            is >> edges[0][i];
            is >> edges[1][i];
            is >> weights[i];
        }

        // CONNECTED COMPONENTS
        int n1,ne;
        int k;
        int remain = nV;
        int su,sv;
        cc.resize(nV);

        for (n1 = 0; n1 < nV; n1++)
            cc[n1] = -1;

        k=0;
        while (remain > 0) {
            n1 = 0;
            while (cc[n1]>-1) n1++;
            cc[n1] = k;
            su = 0;
            sv = 1;

            while (sv > su){
                su = sv;
                for(ne=0; ne<nE; ne++){
                    if(cc[edges[0][ne]]==k)
                        cc[edges[1][ne]] = k;
                    if(cc[edges[1][ne]]==k)
                        cc[edges[0][ne]] = k;
                }
                sv = 0;
                for(n1=0; n1<nV; n1++)
                    sv += (cc[n1]==k);
            }

            remain = remain-su;
            k++;
        }

        int nbcc = k;//0;
        //nbcc = k;
        maxv = maxv - nbcc;

        printf("Connected components: %d\n",nbcc);
        //fclose(inFile);

        //execute clustering
        // AVERAGE_LINK()

        int idxk[IDXK_SIZE];
        k = 0;
        int m,q,j,i,a,p,i1,i2;
        float fi,fj;

        for (q = 0; q < nV-nbcc; q += 1){
            if (q%500 == 0) {printf("#"); fflush(stdout);}
            // # 1. find the heaviest edge
            m = floatmax(weights,nE).arg; // best fitting edge
            k = q+nV;
            height[k] = weights[m]; // cost
            i = edges[0][m]; // element i from m edge
            j = edges[1][m]; // element j from m edge

            // # 2. remove the current edge
            edges[0][m] = -1; // remove the m edge (the heaviest)
            edges[1][m] = -1; // remove the m edge (the heaviest)
            weights[m] = INT_MIN;  // delete its weight
            //   i,j what is this?...the other one? I sould't be reading clones...
            for (a = 0; a < nE; a += 1){
                if( (edges[0][a]==j) && (edges[1][a]==i)){
                    edges[0][a] = -1;
                    edges[1][a] = -1;
                    weights[a] = INT_MIN;
                }
                if( (edges[0][a]==i) && (edges[1][a]==j)){
                    edges[0][a] = -1;
                    edges[1][a] = -1;
                    weights[a] = INT_MIN;
                }
            }
            // 3. merge the edges with third part edges
            father[i] = k;
            father[j] = k;
            pop[k] = pop[i]+pop[j];
            fi = ((float)pop[i])/(pop[k]);  // float
            fj = 1.0-fi;

            // # replace i by k
            for (a = 0; a < nE; a += 1){
                if (edges[0][a] == i){
                    weights[a] = weights[a]*fi;
                    edges[0][a] = k;
                }
                if (edges[1][a] == i){
                    weights[a] = weights[a]*fi;
                    edges[1][a] = k;
                }
                if (edges[0][a] == j){
                    weights[a] = weights[a]*fj;
                    edges[0][a] = k;
                }
                if (edges[1][a] == j){
                    weights[a] = weights[a]*fj;
                    edges[1][a] = k;
                }
            }

            //#sum/remove float edges
            // #left side
            p=0;
            for (a = 0; a < nE; a += 1){
                if (edges[0][a] == k){
                    idxk[p++] = a; // catch every index with an k on the leftside
                    if (p>=IDXK_SIZE){
                        printf("idxk out of bounds\n");
                        break;
                    }
                }
            }

            // maybe the edges will need to be sorted...maybe not

            corr.resize(p);
            scorr.resize(p);
            acorr.resize(p);
            for (a = 0; a < p; a += 1){
                corr[a] = edges[1][idxk[a]];
                scorr[a] = edges[1][idxk[a]];
                acorr[a] = a;
            }

            sort(scorr.begin(),scorr.begin(),comp);
            sort(acorr.begin(),acorr.end(),compind);

            for (a = 0; a < p-1; a += 1){
                if(scorr[a]==scorr[a+1]){
                    i1 = idxk[acorr[a]];
                    i2 = idxk[acorr[a+1]];
                    weights[i1] = weights[i1] + weights[i2];
                    weights[i2] = INT_MIN;
                    edges[0][i2] = -1;
                    edges[1][i2] = -1;
                }
            }
            corr.clear();
            vector<int>().swap(corr);
            scorr.clear();
            vector<int>().swap(scorr);
            acorr.clear();
            vector<int>().swap(acorr);

            // #right side
            p=0;
            for (a = 0; a < nE; a += 1){
                if (edges[1][a] == k){
                    idxk[p++] = a; // catch every index with an k on the leftside
                    if (p>=IDXK_SIZE){
                        printf("idxk out of bounds\n");
                        break;
                    }
                }
            }

            // maybe the edges will need to be sorted...maybe not
            corr.resize(p);
            scorr.resize(p);
            acorr.resize(p);
            for (a = 0; a < p; a += 1){
                corr[a] = edges[0][idxk[a]];
                scorr[a] = edges[0][idxk[a]];
                acorr[a] = a;
            }

            sort(scorr.begin(),scorr.end(),comp);
            sort(acorr.begin(),acorr.end(),compind);

            for (a = 0; a < p-1; a += 1){
                if(scorr[a]==scorr[a+1]){
                    i1 = idxk[acorr[a]];
                    i2 = idxk[acorr[a+1]];
                    weights[i1] = weights[i1] + weights[i2];
                    weights[i2] = INT_MIN;
                    edges[0][i2] = -1;
                    edges[1][i2] = -1;
                }
            }

        }

        for (i = 0; i < maxv; i += 1){
            if(height[i]<0)
                height[i] = 0;
            if(height[i]==INT_MAX)
                height[i] = height[nV] + 1;
        }
        printf("\n");

    }

    int  V = maxv;

    // initialize children vectors
    vector <int> _ch0(V,-1);
    vector <int> _ch1(V,-1);

    int fa;
    //determine children
    for (int i = 0; i < V; i++) {
        fa = father[i];
        //cout << "fa vale: " << fa << endl;
        //cout << "i vale: " << i << endl;
        if (fa != i){
            if (_ch0[fa] == -1)
                _ch0[fa] = i;
            else
                _ch1[fa] = i;
        }
    }

    ofstream wforestFile;
    wforestFile.open( argv[2]);

    if( wforestFile ){
        wforestFile << maxv << endl;
        for (int i = 0; i< maxv; i++){
            wforestFile << father[i] << " " << _ch0[i] <<" "<<_ch1[i]<<endl;
        }

    }
    wforestFile.close();

    cout<<"Execution Time: "<< ((double)(clock() - t_start))/CLOCKS_PER_SEC<<" secs"<<endl;
    cout << "done" << endl<<flush;

    return EXIT_SUCCESS;

}