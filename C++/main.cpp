#include <bits/stdc++.h>
using namespace std;


class average {
public:
    double summer = 0;
    double count = 0;
    double avg = 0;
    void add(double other) {
        summer += other;
        count += 1;
        avg = summer / count;
    }
};


double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}


double sigmoid_prime(double x) {
    double sig = sigmoid(x);
    return sig * (1.0 - sig);
}


int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    freopen("parameters.txt", "r", stdin);

    int n;
    cin >> n;
    vector<int> lengths(n, 0);
    for (int i = 0; i < n; i++) {cin >> lengths[i];}
    int test_cases = 60000;
    int repeats = 10000;
    double learning_rate = 20 ;
    vector<double> C;

    double x;

    // biases
    vector<vector<double>> biases(n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < lengths[i]; j++) {
            cin >> x;
            biases[i].push_back(x);
        }
    }
    cout << "Biases loaded!" << endl;

    // weights
    vector<vector<vector<double>>> weights(n - 1, vector<vector<double>>());
    for (int i = 0; i < n - 1; i++) {
        weights[i].resize(lengths[i]);
        for (int k = 0; k < lengths[i]; k++) {
            if (i != n - 2) {
                weights[i][k].resize(lengths[i + 1] - 1);
                for (int j = 0; j < lengths[i + 1] - 1; j++) {
                    cin >> weights[i][k][j];
                }
            }
            else {
                weights[i][k].resize(lengths[i + 1]);
                for (int j = 0; j < lengths[i + 1]; j++) {
                    cin >> weights[i][k][j];
                }
            }
        }
    }
    cout << "Weights loaded!" << endl;

    // testing data
    freopen("training_data.txt", "r", stdin);
    vector<vector<vector<double>>> testing(test_cases, {vector<double>(lengths[0] - 1, 0), vector<double>(lengths[n - 1], 0)});
    for (int i = 0; i < test_cases; i++) {
        for (int j = 0; j < lengths[0] - 1; j++) {
            cin >> testing[i][0][j];
        }
        for (int j = 0; j < lengths[n - 1]; j++) {
            cin >> testing[i][1][j];
        }
    }
    cout << "Testing data loaded!" << endl;


    // training
    freopen("log.txt", "a", stdout);
    for (int repeat = 0; repeat < repeats; repeat++) {

        vector<vector<vector<average>>> gradient_weights(n - 1);
        for (int i = 0; i < n - 1; i++) {
            gradient_weights[i].resize(lengths[i]);
            for (int k = 0; k < lengths[i]; k++) {
                if (i != n - 2) {
                    gradient_weights[i][k].resize(lengths[i + 1] - 1);
                }
                else {
                    gradient_weights[i][k].resize(lengths[i + 1]);
                }
            }
        }
        vector<vector<average>> gradient_biases(n);
        for (int i = 0; i < n; i++) {
            gradient_biases[i].resize(lengths[i]);
        }
        average C_cur;

        for (int current_test = 0; current_test < test_cases; current_test++) {

            vector<vector<double>> test = testing[current_test];
            vector<vector<double>> array(n);
            vector<vector<double>> z(n);
            for (int i = 0; i < n; i++) {
                if (i == 0) {
                    array[i] = test[0];
                    z[i] = test[0];
                } else {
                    array[i].resize(lengths[i]);
                    z[i].resize(lengths[i]);
                }
            }
            vector<double> y = test[1];

            for (int i = 1; i < n; i++) {
                for (int j = 0; j < lengths[i]; j++) {
                    if (i == n - 1 || j < lengths[i] - 1) {
                        for (int k = 0; k < lengths[i - 1] - 1; k++) {
                            array[i][j] += array[i - 1][k] * weights[i - 1][k][j];
                        }
                        array[i][j] += biases[i - 1][lengths[i - 1] - 1] * weights[i - 1][lengths[i - 1] - 1][j];
                        array[i][j] += biases[i][j];
                        z[i][j] = array[i][j];
                        array[i][j] = sigmoid(array[i][j]);
                    }
                }
            }


            double C_cur_cur = 0;
            for (int i = 0; i < lengths[n - 1]; i++) {
                C_cur_cur += pow(array[n - 1][i] - y[i], 2);
            }
            C_cur_cur /= (2 * lengths[n - 1]);
            C_cur.add(C_cur_cur);


            vector<vector<double>> d_bias_z(n), d_array(n);
            for (int i = 0; i < n; i++) {
                d_array[i].resize(lengths[i]);
                d_bias_z[i].resize(lengths[i]);
            }
            vector<vector<vector<double>>> d_weights(n - 1);
            for (int i = 0; i < n - 1; i++) {
                d_weights[i].resize(lengths[i]);
                for (int k = 0; k < lengths[i]; k++) {
                    if (i != n - 2) {
                        d_weights[i][k].resize(lengths[i + 1] - 1);
                    }
                    else {
                        d_weights[i][k].resize(lengths[i + 1]);
                    }
                }
            }

            for (int i = 0; i < lengths[n - 1]; i++) {
                d_array[n - 1][i] = (array[n - 1][i] - y[i]) / lengths[n - 1];
                d_bias_z[n - 1][i] = d_array[n - 1][i] * sigmoid_prime(z[n - 1][i]);
            }
            for (int i = n - 2; i >= 0; i--) {
                for (int k = 0; k < lengths[i]; k++) {
                    for (int j = 0; j < lengths[i + 1]; j++) {
                        if (i == n - 2 || j < lengths[i + 1] - 1) {
                            d_weights[i][k][j] = d_bias_z[i + 1][j] * array[i][k];
                            d_array[i][k] += d_bias_z[i + 1][j] * weights[i][k][j];
                        }
                    }
                    if (k < lengths[i] - 1) {
                        d_bias_z[i][k] = d_array[i][k] * sigmoid_prime(z[i][k]);
                    }
                    else {
                        d_bias_z[i][k] = d_array[i][k];
                    }
                }
            }


            for (int i = 0; i < n; i++) {
                for (int j = 0; j < lengths[i]; j++) {
                    gradient_biases[i][j].add(d_bias_z[i][j]);
                }
            }

            for (int i = 0; i < n - 1; i++) {
                for (int k = 0; k < lengths[i]; k++) {
                    for (int j = 0; j < lengths[i + 1]; j++) {
                        if (i == n - 2 || j < lengths[i + 1] - 1) {
                            gradient_weights[i][k][j].add(d_weights[i][k][j]);
                        }
                    }
                }
            }
        }

        C.push_back(C_cur.avg);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < lengths[i]; j++) {
                biases[i][j] -= gradient_biases[i][j].avg * learning_rate;
            }
        }
        for (int i = 0; i < n - 1; i++) {
            for (int k = 0; k < lengths[i]; k++) {
                for (int j = 0; j < lengths[i + 1]; j++) {
                    if (i == n - 2 || j < lengths[i + 1] - 1) {
                        weights[i][k][j] -= gradient_weights[i][k][j].avg * learning_rate;
                    }
                }
            }
        }


        freopen("log.txt", "a", stdout);
        cout << " " << repeat << " " << C_cur.avg << endl;

        ofstream file;
        file.open("generations/trained" + to_string(repeat), ios::out);

        file << n << endl;
        for (int i: lengths) { file << i << " "; }
        file << endl;
        for (int i = 0; i < n; i++) {
            for (double j: biases[i]) { file << setprecision(20) << j << " "; }
        }
        file << endl;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < lengths[i]; j++) {
                for (double k: weights[i][j]) { file << setprecision(20) << k << " "; }
            }
        }
        file << endl;

        file.close();


    }

    return 0;
}
