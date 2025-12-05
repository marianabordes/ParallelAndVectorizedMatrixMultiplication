package org.ulpgc.bigdata.task3;

/**
 * Interface for matrix multiplication strategies.
 * Implementations must provide a name and a multiply() method.
 */
public interface MatrixMultiplier {

    /**
     * @return A human-readable name for this strategy.
     */
    String getName();

    /**
     * Computes C = A × B for NxN matrices stored in row-major layout.
     *
     * @param A First matrix (row-major)
     * @param B Second matrix (row-major)
     * @param C Output matrix (row-major)
     * @param N Dimension of the matrices
     */
    void multiply(double[] A, double[] B, double[] C, int N);
}

