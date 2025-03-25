import numpy as np
import matplotlib.pyplot as plt
from fig_dp import FIGDP
import time
from datetime import datetime

def generate_random_dna_sequence(n: int) -> str:
    """
    Generate a random DNA sequence of length n.
    Uses standard DNA nucleotides: A (Adenine), C (Cytosine), G (Guanine), T (Thymine)
    
    Args:
        n: Length of the sequence to generate
        
    Returns:
        A random DNA sequence of length n
    """
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(np.random.choice(nucleotides, size=n))

def format_sequence(seq: str, line_length: int = 80) -> str:
    """Format a DNA sequence with line breaks and position markers."""
    lines = []
    for i in range(0, len(seq), line_length):
        chunk = seq[i:i+line_length]
        pos = str(i+1).rjust(8)
        lines.append(f"{pos} {chunk}")
    return '\n'.join(lines)

def run_experiments():
    """Run experiments with varying input sizes and gap constraints."""
    sizes = [100, 200, 400, 800, 1600, 3200]
    gap_constraints = [5, 10, 20]
    results = {k: [] for k in gap_constraints}
    
    for size in sizes:
        print(f"Testing with size {size}...")
        seq1 = generate_random_dna_sequence(size)
        seq2 = generate_random_dna_sequence(size)
        
        for k in gap_constraints:
            # Run multiple times to get average
            num_runs = 5
            total_time = 0
            max_lengths = []
            
            for run in range(num_runs):
                solver = FIGDP(seq1, seq2, k)
                max_length, matching_seq, execution_time = solver.solve()
                total_time += execution_time
                max_lengths.append(max_length)
                
                if run == 0:  # Save first run's results for analysis
                    with open(f'results/lcs_fig_size_{size}_k_{k}.txt', 'w') as f:
                        # Write header with timestamp
                        f.write("="*80 + "\n")
                        f.write("LCS-FIG Algorithm Results\n")
                        f.write("="*80 + "\n")
                        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Input Size: {size}\n")
                        f.write(f"Gap Constraint (K): {k}\n")
                        f.write("\n")

                        # Write input sequences
                        f.write("-"*80 + "\n")
                        f.write("Input Sequences\n")
                        f.write("-"*80 + "\n")
                        f.write("\nDNA Sequence 1:\n")
                        f.write(format_sequence(seq1))
                        f.write("\n\nDNA Sequence 2:\n")
                        f.write(format_sequence(seq2))
                        f.write("\n")

                        # Write results
                        f.write("\n" + "-"*80 + "\n")
                        f.write("Results\n")
                        f.write("-"*80 + "\n")
                        f.write(f"Maximum LCS Length: {max_length}\n")
                        f.write("\nMatching DNA Sequence:\n")
                        f.write(format_sequence(matching_seq))
                        f.write(f"\n\nExecution Time: {execution_time:.4f} seconds\n")
                        
                        # Write match positions
                        f.write("\n" + "-"*80 + "\n")
                        f.write("Match Positions\n")
                        f.write("-"*80 + "\n")
                        pos1 = []
                        pos2 = []
                        i, j = 0, 0
                        for char in matching_seq:
                            # Find next occurrence in seq1
                            while i < len(seq1) and seq1[i] != char:
                                i += 1
                            if i < len(seq1):
                                pos1.append(i+1)  # Convert to 1-based indexing
                                i += 1
                            
                            # Find next occurrence in seq2
                            while j < len(seq2) and seq2[j] != char:
                                j += 1
                            if j < len(seq2):
                                pos2.append(j+1)  # Convert to 1-based indexing
                                j += 1
                        
                        # Format positions in columns
                        f.write("\nPosition mapping (1-based indexing):\n")
                        f.write("\nIndex  Seq1_Pos  Seq2_Pos  Nucleotide\n")
                        f.write("-"*40 + "\n")
                        for idx, (p1, p2, nuc) in enumerate(zip(pos1, pos2, matching_seq), 1):
                            f.write(f"{str(idx).rjust(5)}  {str(p1).rjust(8)}  {str(p2).rjust(8)}  {nuc.center(9)}\n")
                        
                        # Write nucleotide composition
                        f.write("\n" + "-"*80 + "\n")
                        f.write("Nucleotide Composition Analysis\n")
                        f.write("-"*80 + "\n")
                        for seq_name, seq in [("DNA Sequence 1", seq1), ("DNA Sequence 2", seq2), ("Matching Sequence", matching_seq)]:
                            f.write(f"\n{seq_name}:\n")
                            f.write("Nucleotide  Count  Percentage\n")
                            f.write("-"*30 + "\n")
                            for nucleotide in ['A', 'C', 'G', 'T']:
                                count = seq.count(nucleotide)
                                percentage = (count / len(seq)) * 100
                                f.write(f"{nucleotide.center(10)}  {str(count).rjust(5)}  {percentage:6.1f}%\n")
            
            avg_time = total_time / num_runs
            avg_length = sum(max_lengths) / len(max_lengths)
            results[k].append((size, avg_time, avg_length))
            print(f"K={k}, Average time: {avg_time:.4f} seconds, Average length: {avg_length:.2f}")
    
    # Plot time results
    plt.figure(figsize=(12, 6))
    for k in gap_constraints:
        sizes, times, _ = zip(*results[k])
        plt.plot(sizes, times, 'o-', label=f'K={k}')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('LCS-FIG Algorithm Performance (DNA Sequences)')
    plt.grid(True)
    plt.legend()
    plt.savefig('performance_plot.png')
    plt.close()
    
    # Plot length results
    plt.figure(figsize=(12, 6))
    for k in gap_constraints:
        sizes, _, lengths = zip(*results[k])
        plt.plot(sizes, lengths, 'o-', label=f'K={k}')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Average LCS Length')
    plt.title('LCS-FIG Solution Length (DNA Sequences)')
    plt.grid(True)
    plt.legend()
    plt.savefig('length_plot.png')
    plt.close()
    
    # Save data to file
    with open('performance_data.txt', 'w') as f:
        f.write("Size\tK\tTime (seconds)\tAverage Length\n")
        for k in gap_constraints:
            for size, time, length in results[k]:
                f.write(f"{size}\t{k}\t{time:.4f}\t{length:.2f}\n")

if __name__ == "__main__":
    run_experiments() 