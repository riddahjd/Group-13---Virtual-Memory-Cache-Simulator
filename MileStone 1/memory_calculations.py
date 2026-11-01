import math

PAGE_SIZE = 4096
PAGE_TABLE_ENTRIES = 512 * 1024


def calculate_memory(physical_memory_mb, os_percent, num_processes):
    physical_memory_bytes = physical_memory_mb * 1024 * 1024

    total_physical_pages = physical_memory_bytes // PAGE_SIZE

    os_pages = int(total_physical_pages * os_percent / 100)

    page_number_bits = int(math.log2(total_physical_pages))
    page_table_entry_bits = page_number_bits + 1

    page_table_ram_bytes = (PAGE_TABLE_ENTRIES * page_table_entry_bits * num_processes) // 8

    return {
        "total_physical_pages": total_physical_pages,
        "os_reserved_pages": os_pages,
        "user_available_pages": total_physical_pages - os_pages,
        "page_table_entry_bits": page_table_entry_bits,
        "page_table_ram_bytes": page_table_ram_bytes,
        "page_table_entries_per_process": PAGE_TABLE_ENTRIES,
    }


def format_memory_values(values):
    lines = [
        "***** Physical Memory Calculated Values *****",
        "",
        f"Number of Physical Pages: {values['total_physical_pages']}",
        f"Number of Pages for System: {values['os_reserved_pages']}",
        f"Size of Page Table Entry: {values['page_table_entry_bits']} bits",
        f"Total RAM for Page Table(s): {values['page_table_ram_bytes']} bytes",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    example = calculate_memory(1024, 75, 3)
    print(format_memory_values(example))
