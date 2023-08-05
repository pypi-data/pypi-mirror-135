//Author: Narciso Lopez Lopez

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cmath>
#include <cstdlib>
#include <algorithm>
#include <ctime>

using namespace std;

int main (int argc, char *argv[]) {

    if(argc!=4){
        cout << "./getAffinityGraphFromDistanceMatrix distanceMatrix affinityGraph maximumDistance" << endl;
        cout <<  "distanceMatrix: input file .bin with distance matrix" << endl;
        cout <<  "affinityGraph: output file .txt with affinities graph" << endl;
        cout <<  "maximumDistance: e.g. 50" << endl;
        return -1;
    }

    clock_t t_start = clock();  	// medir tiempo ejecución

    float var = 3600.;				// varianza
    float maxdist = atof(argv[3]);			// dcl

    vector <vector<double> > matrix_distance;       // matriz que almacena las distancias
    vector<double> v;                                               // vector para leer la entrada binaria del fichero y pasar posteriormente a la matriz de distancias

    ifstream in(argv[1], ios_base::in);                      // fichero binario de entrada con las distancias de las fibras

    if (!in.is_open()){                             // comprobación para saber si se ha abierto el fichero
        cout << "Error opening file";
        exit (1);
    }

    string str;
    while(getline(in, str)){			    // leer linea a linea el fichero binario de entrada
        istringstream ss(str);
        double num;
        while(ss >> num)
            v.push_back(num);			            // insertar al vector
        matrix_distance.push_back(v);		// insertar a la matriz de distancias
        v.clear();
    }

    in.close();					        // se cierra el fichero binario de entrada

    float dist, aff = 0.;
    uint nodes = 0;              // contador para saber el número de nodos
    uint edges = 0;              // contador para saber el número de aristas
    FILE *out = fopen(argv[2] ,"w");    // ruta del fichero de salida para almacenar el "grafo de afinidades"

    fprintf(out, "%s", "                     \n" ); // dejar espacio para introducir nodes y edges a posteriori

    for (uint p1 = 0; p1 < matrix_distance.size(); p1++){
        for (uint p2 = 0; p2 < p1; p2++){			    // se recorre como si fuera una triangular inferior ya que por simetría no es necesario hacer todas las operaciones
            dist = matrix_distance[p1][p2]; 		// obtener distancia de la celda entre nodos
            if (dist <= maxdist){					        // si la distancia entre nodos es más pequeña que la distancia del clúster
                aff = exp(-dist*dist/var);			        // cálculo de la afinidad entre nodos
                fprintf(out, "%d %d %f\n", p2, p1, aff);    // escribir conexiones entre nodos y afinidad entre ellos
                fprintf(out, "%d %d %f\n", p1, p2, aff);
                edges+=2;		// número de aristas +2
            }
        }
        nodes++;            // número de nodos +1
    }

    rewind(out);                                            // inicio de fichero
    fprintf(out, "%d %d", nodes, edges);    // escribir número de nodos y aristas
    fclose(out);                                             // cerrar fichero de salida

    //   cout << "Execution Time: " << ((double)(clock() - t_start)*1000)/CLOCKS_PER_SEC  << " ms" << endl;	// mostrar tiempo de ejecución
    cout << "Execution Time: " << ((double)(clock() - t_start))/CLOCKS_PER_SEC  << " secs" << endl;	// mostrar tiempo de ejecución

    return EXIT_SUCCESS;
}
