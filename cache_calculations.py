import math
COST_PER_KB = 0.07
VALID_BITS = 1

def calculate_cache(cache_size_kb, block_size, associativity, physical_memory_mb):
    cache_bytes = cache_size_kb * 1024
    phys_mem_bytes = physical_memory_mb * 1024 * 1024

    total_blocks = cache_bytes // block_size
    total_rows = total_blocks // associativity

    offset_bits = int(math.log2(block_size))
    index_bits = int(math.log2(total_rows))

    phys_addr_bits = int(math.log2(phys_mem_bytes))
    tag_bits = phys_addr_bits - index_bits - offset_bits

    # overhead = tag + valid bit stored for every block
    overhead_bytes = (total_blocks * (tag_bits + VALID_BITS)) // 8

    implementation_bytes = cache_bytes + overhead_bytes
    implementation_kb = implementation_bytes / 1024
    cost = implementation_kb * COST_PER_KB

    return {
        "total_blocks": total_blocks,
        "tag_bits": tag_bits,
        "index_bits": index_bits,
        "offset_bits": offset_bits,
        "total_rows": total_rows,
        "overhead_bytes": overhead_bytes,
        "implementation_bytes": implementation_bytes,
        "implementation_kb": implementation_kb,
        "cost": cost,
    }


def format_cache_values(values):
    lines = [
        "***** Cache Calculated Values *****",
        "",
        f"Total # Blocks: {values['total_blocks']}",
        f"Tag Size: {values['tag_bits']} bits",
        f"Index Size: {values['index_bits']} bits",
        f"Total # Rows: {values['total_rows']}",
        f"Overhead Size: {values['overhead_bytes']} bytes",
        f"Implementation Memory Size: {values['implementation_kb']:.2f} KB "
        f"({values['implementation_bytes']} bytes)",
        f"Cost: ${values['cost']:.2f} @ ${COST_PER_KB:.2f} per KB",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_cache_values(calculate_cache(512, 16, 4, 1024)))
