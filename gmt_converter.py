import gzip
import csv
import sys

# This function is to read the homo_sapiens file and returns a dictionary with mapping of symbols to geneid. It also considered synonyms and added them to mapping. 
# Creates a mapping of symbols to geneid.

def read_gene_info(gene_info_file):
    symbol_to_geneid = {}

    with gzip.open(gene_info_file, 'rt') as file:
        reader = csv.reader(file, delimiter='\t')

        for row in reader:
            gene_id = row[1]
            symbol = row[2]
            synonyms = row[4].split('|')

            symbol_to_geneid[symbol] = gene_id

            for synonym in synonyms:
                symbol_to_geneid[synonym] = gene_id

    return symbol_to_geneid

# This function is to read the symbols file and replaces the symbols with Entrez_ID's using the symbol to gene_id mapping.
# Creates a GMT output file with replaced Entrez_ID's. 

def replace_gene_names_with_entrez_ids(gmt_file, symbol_to_geneid):
    output_file = "Entrez_ID.gmt"

    with open(gmt_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            pathway_name = row[0]
            pathway_description = row[1]
            gene_names = row[2:]

            entrez_ids = [symbol_to_geneid.get(gene_name, gene_name) for gene_name in gene_names]

            writer.writerow([pathway_name, pathway_description] + entrez_ids)

    print(f"Gene names in GMT file '{gmt_file}' have been replaced with Entrez IDs. Output saved in '{output_file}'.")

# The main() function is used to phrase the command line arguments to get the input files. It then calls the read_gene_info() function to create the mapping and 
# replace the gene_names with Entrez_ID's function to process the GMT file and save the updated Entrez_ID's GMT file.


def main():
    if len(sys.argv) != 3:
        print("Usage: python gmt_converter.py Homo_sapiens.gene_info.gz h.all.v2023.1.Hs.symbols.gmt")
        sys.exit(1)

    gene_info_file = sys.argv[1]
    gmt_file = sys.argv[2]

    symbol_to_geneid = read_gene_info(gene_info_file)
    replace_gene_names_with_entrez_ids(gmt_file, symbol_to_geneid)

if __name__ == "__main__":
    main()
