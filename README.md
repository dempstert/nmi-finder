# nmi-finder
A repository for finding NMIs and MIRNs for the Australian Energy Market

## Rules
This repo uses text-based parsing methods to identify NMIs / MIRNs in text.
NMIs/MIRNs conform to a specific set of rules:
1. 10 or 11 digits
2. All caps
3. All alpha-numeric
4. Must not contain ‘O' or ‘I’ (this refers to latin alphabet letters O and I, not to be confused with the numerals zero and one, which ARE allowed)
5. Must conform to these patterns for how they start:
  https://aemo.com.au/-/media/files/electricity/nem/retail_and_metering/metering-procedures/nmi-allocation-list.pdf?la=en
6. If there are 11 digits, the 11th digit must satisfy the NMI checksum (this also means the checksum must always be a single digit number)
