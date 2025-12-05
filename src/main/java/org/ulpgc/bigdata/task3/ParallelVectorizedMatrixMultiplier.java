package org.ulpgc.bigdata.task3;
import java.util.stream.IntStream;

/**
 * Parallel + Vectorized version.
 * Uses B-transposition for SIMD/cache benefits and parallelizes by rows.
 */
public class ParallelVectorizedMatrixMultiplier implements MatrixMultiplier {

    @Override
    public String getName() {
        return "ParallelVectorized";
    }

    @Override
    public void multiply(double[] A, double[] B, double[] C, int N) {

        double[] B_T = new double[N * N];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                B_T[j * N + i] = B[i * N + j];
            }
        }

        IntStream.range(0, N).parallel().forEach(i -> {
            for (int j = 0; j < N; j++) {
                double sum = 0.0;
                int rowA = i * N;
                int rowBT = j * N;
                for (int k = 0; k < N; k++) {
                    sum += A[rowA + k] * B_T[rowBT + k];
                }
                C[i * N + j] = sum;
            }
        });
    }
}
