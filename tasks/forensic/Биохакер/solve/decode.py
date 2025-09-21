from Bio import SeqIO
signal_bits = ''
for rec in SeqIO.parse('lettuce.fastq', 'fastq'):
    for base in str(rec.seq):
        if base in ('A', 'T'):
            signal_bits += '0' if base == 'A' else '1'
signal_bits = signal_bits[:len(signal_bits)//8*8]
binary_data = bytes(int(signal_bits[i:i+8], 2) for i in range(0, len(signal_bits), 8))
with open('data.bin', 'wb') as f:
    f.write(binary_data)