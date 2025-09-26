import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_gflops_per_inference_time(df):
    """
    Generates a plot showing for each model_size and each DPU type,
    the gflop/infer diveded by the total inference vaitrace time.
    """
    # Ensure the 'plots' directory exists
    if not os.path.exists('plots'):
        os.makedirs('plots')

    df['gflops_per_vaitrace_time'] = df['GFLOP/inference'] / df['total inference vaitrace time (ms)']

    plt.figure(figsize=(15, 8))
    for dpu_type in df['DPU type'].unique():
        subset = df[df['DPU type'] == dpu_type]
        plt.plot(subset['model_size'], subset['gflops_per_vaitrace_time'], marker='o', linestyle='-', label=dpu_type)

    plt.xlabel('Model Size')
    plt.ylabel('GFLOP/s (Vaitrace)')
    plt.title('GFLOP/s (Vaitrace) per Model Size for each DPU Type')
    plt.legend(title='DPU Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/gflops_per_inference_time.png')
    plt.close()
    return 'plots/gflops_per_inference_time.png'

def plot_total_inference_time(df):
    """
    Generates a plot showing total inference time by DPU type for each model size.
    """
    # Ensure the 'plots' directory exists
    if not os.path.exists('plots'):
        os.makedirs('plots')

    plt.figure(figsize=(15, 8))
    for dpu_type in df['DPU type'].unique():
        subset = df[df['DPU type'] == dpu_type]
        plt.plot(subset['model_size'], subset['total inference vaitrace time (ms)'], marker='o', linestyle='-', label=dpu_type)

    plt.xlabel('Model Size')
    plt.ylabel('Total Inference Vaitrace Time (ms)')
    plt.title('Total Inference Vaitrace Time per Model Size for each DPU Type')
    plt.legend(title='DPU Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/total_inference_time.png')
    plt.close()
    return 'plots/total_inference_time.png'

def main():
    """
    Main function to analyze data and generate plots.
    """
    # Load the data
    filepath = 'analyse_data_inference.txt'
    try:
        df = pd.read_csv(filepath, sep='\t', decimal=',')
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return

    # Clean up DPU type names
    df['DPU type'] = df['DPU type'].str.replace(' copy', '').str.strip()

    # Generate plots
    plot1_path = plot_gflops_per_inference_time(df.copy())
    plot2_path = plot_total_inference_time(df.copy())

    # Generate markdown file
    with open('plot.md', 'w') as f:
        f.write("# Analysis Plots\n\n")
        f.write("## GFLOP/s per Inference Time\n")
        f.write(f"![GFLOP/s per Inference Time]({plot1_path})\n\n")
        f.write("## Total Inference Time\n")
        f.write(f"![Total Inference Time]({plot2_path})\n\n")

    print("Plots and plot.md have been generated successfully.")

if __name__ == '__main__':
    main()