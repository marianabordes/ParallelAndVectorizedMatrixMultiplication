package org.ulpgc.bigdata.task3;
import java.util.stream.IntStream;

/**
 * Parallel matrix multiplication using Java parallel streams.
 * Each row of the result matrix is processed by a different task.
 */
public class ParallelMatrixMultiplier implements MatrixMultiplier {

    @Override
    public String getName() {
        return "Parallel";
    }

    @Override
    public void multiply(double[] A, double[] B, double[] C, int N) {
        IntStream.range(0, N).parallel().forEach(i -> {
            for (int j = 0; j < N; j++) {
                double sum = 0.0;
                for (int k = 0; k < N; k++) {
                    sum += A[i * N + k] * B[k * N + j];
                }
                C[i * N + j] = sum;
            }
        });
    }
}