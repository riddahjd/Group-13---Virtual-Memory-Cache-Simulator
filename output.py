import os

def write_results(team_number, trace_files, inputs, cache_results, memory_results, run_number, output_directory):
    policy_map = {"RR": "Round Robin", "RND": "Random"}
    display_policy = policy_map.get(inputs["replacement_policy"], inputs["replacement_policy"])

    lines = [
        "MILESTONE #1: Input Parameters and Calculated Values",
        f"Cache Simulator - CS 3853 – Team #{team_number}",
        "Trace File(s):"
    ]
    
    for file in trace_files:
        lines.append(f"   {file}")
        
    lines.extend([
        "***** Cache Input Parameters *****",
        "",
        f"Cache Size:                {inputs['cache_size_kb']} KB",
        f"Block Size:                {inputs['block_size']} bytes",
        f"Associativity:             {inputs['associativity']}",
        f"Replacement Policy:        {display_policy}",
        f"Physical Memory:           {inputs['physical_memory_mb']} MB",
        f"Percent Memory Used by System: {inputs['os_percent']:.1f}%",
        f"Instructions / Time Slice: {inputs['instructions_per_time_slice']}",
        "",
        "***** Cache Calculated Values *****",
        "",
        f"Total # Blocks:            {cache_results['total_blocks']}",
        f"Tag Size:                  {cache_results['tag_bits']} bits",
        f"Index Size:                {cache_results['index_bits']} bits",
        f"Total # Rows:              {cache_results['total_rows']}",
        f"Overhead Size:             {cache_results['overhead_bytes']} bytes",
        f"Implementation Memory Size: {cache_results['implementation_kb']:.2f} KB ({cache_results['implementation_bytes']} bytes)",
        f"Cost:                      ${cache_results['cost']:.2f} @ $0.07 per KB",
        "",
        "***** Physical Memory Calculated Values *****",
        "",
        f"Number of Physical Pages:  {memory_results['total_physical_pages']}",
        f"Number of Pages for System: {memory_results['os_reserved_pages']}",
        f"Size of Page Table Entry:  {memory_results['page_table_entry_bits']} bits",
        f"Total RAM for Page Table(s): {memory_results['page_table_ram_bytes']} bytes"
    ])

    output_content = "\n".join(lines)
    print(output_content)

    os.makedirs(output_directory, exist_ok=True)
    filename = f"Team_{team_number}_Sim_{run_number}_M#1.txt"
    filepath = os.path.join(output_directory, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output_content)

    return filepath
