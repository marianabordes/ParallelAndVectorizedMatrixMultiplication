package org.ulpgc.bigdata.task3;

import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import java.util.Random;

/**
 * Benchmark runner for matrix multiplication strategies.
 * Measures execution time, memory, CPU load, speedup, and efficiency.
 **/

public class Main {

    private static volatile boolean monitorRunning = false;
    private static volatile double maxCpuLoad = 0.0;

    public static void main(String[] args) throws IOException {

        int[] sizes = {128, 256, 512, 1024, 2048};
        MatrixMultiplier[] strategies = {
                new BasicMatrixMultiplier(),
                new ParallelMatrixMultiplier(),
                new VectorizedMatrixMultiplier(),
                new ParallelVectorizedMatrixMultiplier()
        };

        try (FileWriter writer = new FileWriter("results2.csv")) {
            writer.append("N,Strategy,TimeMs,Speedup,Efficiency,CPU%,MemoryBytes\n");

            for (int N : sizes) {
                double[] A = randomMatrix(N);
                double[] B = randomMatrix(N);

                double[] C_basic = new double[N * N];
                BasicMatrixMultiplier basic = new BasicMatrixMultiplier();

                System.out.println("\n========== N = " + N + " ==========");

                // Warm-up
                basic.multiply(A, B, C_basic, N);

                long timeBasic = measureTime(basic, A, B, C_basic, N);

                for (MatrixMultiplier s : strategies) {
                    double[] C = new double[N * N];

                    long time = measureWithCpuAndMemory(s, A, B, C, N);

                    // correctness check
                    validateResults(C_basic, C, s.getName(), N);

                    double speedup = (double) timeBasic / time;
                    int cores = Runtime.getRuntime().availableProcessors();
                    double efficiency = speedup / cores;

                    double cpu = maxCpuLoad * 100;

                    long mem = getUsedMemory();

                    writer.append(String.format("%d,%s,%d,%.4f,%.4f,%.2f,%d\n",
                            N, s.getName(), time, speedup, efficiency, cpu, mem));

                    System.out.printf(
                            "N=%d | %-20s | Time=%d ms | Speedup=%.2f | Eff=%.2f | CPU=%.2f%% | Mem=%d bytes\n",
                            N, s.getName(), time, speedup, efficiency, cpu, mem
                    );

                }
            }
        }
    }

    // --------------------------------------------------------------------
    // Utility methods
    // --------------------------------------------------------------------

    private static double[] randomMatrix(int N) {
        Random r = new Random();
        double[] m = new double[N * N];
        for (int i = 0; i < m.length; i++) m[i] = r.nextDouble();
        return m;
    }

    private static long measureTime(MatrixMultiplier m, double[] A, double[] B, double[] C, int N) {
        long start = System.nanoTime();
        m.multiply(A, B, C, N);
        return (System.nanoTime() - start) / 1_000_000;
    }

    private static long measureWithCpuAndMemory(MatrixMultiplier m, double[] A, double[] B, double[] C, int N) {

        startCpuMonitor();

        long start = System.nanoTime();
        m.multiply(A, B, C, N);
        long timeMs = (System.nanoTime() - start) / 1_000_000;

        stopCpuMonitor();

        return timeMs;
    }

    private static void startCpuMonitor() {
        maxCpuLoad = 0.0;
        monitorRunning = true;

        Thread monitor = new Thread(() -> {
            OperatingSystemMXBean os = ManagementFactory.getOperatingSystemMXBean();
            while (monitorRunning) {
                if (os instanceof com.sun.management.OperatingSystemMXBean osMx) {
                    double load = osMx.getProcessCpuLoad();
                    if (load >= 0) maxCpuLoad = Math.max(maxCpuLoad, load);
                }
                try {
                    Thread.sleep(5);
                } catch (InterruptedException ignored) {}
            }
        });

        monitor.setDaemon(true);
        monitor.start();
    }

    private static void stopCpuMonitor() {
        monitorRunning = false;
        // small wait to ensure last reads finish
        try { Thread.sleep(10); } catch (InterruptedException ignored) {}
    }

    private static void validateResults(double[] ref, double[] test, String name, int N) {
        double maxDiff = 0.0;
        for (int i = 0; i < ref.length; i++) {
            maxDiff = Math.max(maxDiff, Math.abs(ref[i] - test[i]));
        }
        if (maxDiff > 1e-6) {
            throw new RuntimeException("Validation failed for " + name + " at N=" + N +
                    ". Max diff = " + maxDiff);
        }
    }

    private static long getUsedMemory() {
        System.gc();
        return Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
    }
}