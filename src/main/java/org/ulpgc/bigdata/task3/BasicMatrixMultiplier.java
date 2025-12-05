package org.ulpgc.bigdata.task3;

/**
 * Basic O(N^3) matrix multiplication using a straightforward triple loop.
 * This serves as the baseline for speedup calculations.
 */
public class BasicMatrixMultiplier implements MatrixMultiplier {

    @Override
    public String getName() {
        return "Basic";
    }

    @Override
    public void multiply(double[] A, double[] B, double[] C, int N) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                double sum = 0.0;
                for (int k = 0; k < N; k++) {
                    sum += A[i * N + k] * B[k * N + j];
                }
                C[i * N + j] = sum;
            }
        }
    }
}
