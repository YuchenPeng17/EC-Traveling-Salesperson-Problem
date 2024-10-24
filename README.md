# EC-Traveling-Salesperson-Problem

## Project Overview

This project explores the Particle Swarm Optimization (PSO) algorithm using various configurations and topologies. It includes an in-depth analysis of swarm size, topologies, weight adjustment, and other key parameters to understand their effect on PSO performance. The project implements standard PSO as well as custom configurations to examine multiple optimization techniques. The results of these experiments are visualized in the form of metrics and data diagrams for detailed analysis.

## Project Structure

```
.
├── Code/
│   ├── analysis_*.py                      # Analysis scripts for swarm size, topologies, weight adjustment
│   ├── metrics_*.py                        # Metrics and results for different PSO configurations
│   ├── metrics_*.png                       # Visualization of PSO results (e.g., swarm size, topology)
├── LICENSE
├── README.md
├── architecture_diagram.png                # PSO architecture design diagram
├── architecture_design.py                  # PSO architecture design code
└── pso_lib.py                              # Core PSO library implementation
```

## Key Components

- **PSO Library**: 
  - `pso_lib.py`: Core implementation of the Particle Swarm Optimization algorithm, providing a modular and flexible framework for different swarm sizes, topologies, and parameters.
  
- **Analysis Scripts**: 
  - `analysis_*.py`: Each script explores different configurations of the PSO algorithm, including swarm size, topologies (e.g., ring, star, fully connected), and weight adjustments. These scripts run experiments and gather metrics for evaluation.
  
- **Metrics and Visualization**:
  - `metrics_*`: These files store the results of various PSO experiments. They include data on fitness values, swarm behaviors, and performance metrics under different conditions. Visual representations are saved as `.png` files for easy interpretation.

- **Architecture Design**:
  - `architecture_design.py`: Defines the object-oriented architecture of the PSO system, following modular design principles.
  - `architecture_diagram.png`: Visual representation of the system's architecture, summarizing the structure of the PSO implementation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pso-analysis.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the analysis scripts to perform various PSO experiments:
   ```bash
   python Code/analysis_swarm_size.py
   ```

## Usage

1. To perform an analysis with a specific PSO configuration, run the corresponding script in the `Code` directory. For example, to analyze the effect of swarm size, use:
   ```bash
   python Code/analysis_swarm_size.py
   ```

2. Generated metrics and visualizations will be saved in the appropriate directories, providing insights into the performance of the PSO under different conditions.

## Data Diagrams

The results of the experiments are visualized through various data diagrams, saved as `.png` files in the `Code` directory. These diagrams include:

- **Swarm Size Analysis**: Visualizes the effect of different swarm sizes on PSO performance (`metrics_std_pso_swarm*.png`).
- **Topology Analysis**: Compares the performance of different topologies such as fully connected, ring, and star (`metrics_std_pso_topo_*.png`).
- **Weight Adjustment Analysis**: Visualizes how adjusting particle weights impacts the optimization (`metrics_std_pso_weight_adjust.png`).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README provides a clear overview of your project, including structure, installation, and usage instructions, along with a dedicated section for the data diagrams generated during the analysis. Let me know if you need any modifications!