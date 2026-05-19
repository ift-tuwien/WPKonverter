-- Setup -----------------------------------------------------------------------

  $ cd "$TESTDIR"
  $ DATADIR=../data

-- Check Conversion of Data Containing Error -----------------------------------

  $ wpkonverter "${DATADIR}/error.csv"
  Unable to parse data in mail 1:
  
  ┆ 
  ┆ Ich nehme teil an folgenden Programmpunkten teil:
  ┆ Dienstag 6.10.2026 - Come Together, Mittwoch 7.10.2026 - 1. Kongresstag, Mittwoch 7.10.2026 - Galadinner, Donnerstag 8.10.2026 - 2. Kongresstag
  ┆ 
  ┆ Begleitperson Error: ja
     ^
     Expected Keyword 'Begleitperson:', found 'Begleitperson'  \(at char \d+\), \(line:16, col:1\) (re)
  ┆ Speaker+1 Speaker+1
  
  Stored data in “../data/error.xlsx”

-- Cleanup ---------------------------------------------------------------------

  $ rm -f "${DATADIR}/error.xlsx"