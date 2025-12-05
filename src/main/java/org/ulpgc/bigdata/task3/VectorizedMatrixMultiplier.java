package org.ulpgc.bigdata.task3;
/**
 * Cache-friendly and SIMD-friendly matrix multiplication.
 * B is transposed so that both A and B_T are accessed with unit stride,
 * which improves cache locality and allows JVM auto-vectorization.
 *
 * This version is intentionally single-threaded to isolate the effect
 * of vectorization vs. parallelization.
 */
public class VectorizedMatrixMultiplier implements MatrixMultiplier {

    @Override
    public String getName() {
        return "Vectorized";
    }

    @Override
    public void multiply(double[] A, double[] B, double[] C, int N) {

        // Build B^T (B transposed) for unit-stride access in the inner loop.
        double[] B_T = new double[N * N];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                B_T[j * N + i] = B[i * N + j];
            }
        }

        // Multiply using SIMD-friendly memory access.
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                double sum = 0.0;
                int rowA = i * N;
                int rowBT = j * N;
                for (int k = 0; k < N; k++) {
                    sum += A[rowA + k] * B_T[rowBT + k];
                }
                C[i * N + j] = sum;
            }
        }
    }
}