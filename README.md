# Parallel and Vectorized Matrix Multiplication Benchmarking

This project is part of the **Big Data** course at **ULPGC (Universidad de Las Palmas de Gran Canaria)**. 

It implements a comprehensive benchmarking suite to evaluate and compare different matrix multiplication strategies in Java. The study focuses on the impact of **Parallel Computing** (using Java Streams) and **Memory Optimization** (Cache Locality/Vectorization) on computational performance.

## Project Overview

The application benchmarks four distinct algorithms for multiplying dense square matrices ($N \times N$). It measures execution time, CPU load, and memory consumption to calculate **Speedup** and **Efficiency** relative to a naive baseline.

### Implemented Strategies

1.  **Basic (`BasicMatrixMultiplier`)**: 
    - Standard $O(N^3)$ triple-loop implementation.
    - Single-threaded.
    - Suffers from poor cache locality due to row-major traversal of the second matrix.

2.  **Parallel (`ParallelMatrixMultiplier`)**:
    - Uses Java **Parallel Streams** to distribute the outer loop (rows) across available CPU cores.
    - Improves CPU utilization but does not resolve memory access bottlenecks.

3.  **Vectorized / Cache-Optimized (`VectorizedMatrixMultiplier`)**:
    - Single-threaded implementation that performs **B-Matrix Transposition** before multiplication.
    - Ensures sequential memory access (unit stride), enabling CPU prefetching and SIMD auto-vectorization.

4.  **Parallel + Vectorized (`ParallelVectorizedMatrixMultiplier`)**:
    - **Hybrid approach**. Transposes the matrix for cache locality and executes the multiplication in parallel.
    - Achieves super-linear speedup by optimizing both compute power and memory bandwidth.

## Prerequisites

* **Java JDK 17** or higher (tested on OpenJDK 19).
* **Python 3.x** (for data visualization).
* Python libraries: `pandas`, `matplotlib`, `seaborn`.

## How to Run

### 1. Compile the Java Project
Navigate to the root directory of the project and compile the source code:

```bash
mkdir -p bin
javac -d bin src/org/ulpgc/bigdata/task3/*.java
````

### 2\. Run the Benchmark

Execute the `Main` class. This will run the benchmarks for matrix sizes defined in the code (e.g., 128, 256, 512, 1024, 2048) and generate a CSV file with the results.

```bash
java -cp bin org.ulpgc.bigdata.task3.Main
```

*Output:* The program will print progress to the console and save the raw data to `results.csv`.

### 3\. Generate Visualizations

Use the provided Python script to parse the CSV results and generate performance graphs.

First, install dependencies:

```bash
pip install pandas matplotlib seaborn
```

Then run the script:

```bash
python visualizations.py
```

*Output:* The graphs will be saved in the `visualizations/` folder.

## Results Summary

The benchmarking results typically highlight the following behaviors:

  * **Basic:** Performance degrades cubically; severe cache misses on large matrices.
  * **Parallel:** Provides a speedup roughly proportional to the core count, but hits a memory wall.
  * **Vectorized:** Outperforms the Parallel strategy on large matrices despite being single-threaded, proving the importance of cache locality.
  * **ParallelVectorized:** Achieves **super-linear speedup** (e.g., \>100x on 8 cores) by combining efficient memory access with multi-core processing.

## Project Structure

```
.
├── src/org/ulpgc/bigdata/task3/
│   ├── Main.java                        # Benchmark runner
│   ├── MatrixMultiplier.java            # Strategy Interface
│   ├── BasicMatrixMultiplier.java       # Baseline algorithm
│   ├── ParallelMatrixMultiplier.java    # Multithreaded algorithm
│   ├── VectorizedMatrixMultiplier.java  # Transposed/Cache-optimized
│   └── ParallelVectorizedMatrixMultiplier.java # Hybrid algorithm
├── visualizations.py                    # Python script for plotting
├── results.csv                          # Benchmark output data
├── visualizations/                      # Generated graphs (.png/.jpg)
└── README.md                            # Project documentation
```

## Author

**Mariana Bordes Bueno** Grado en Ciencia e Ingeniería de Datos  
ULPGC - Academic Year 2025
