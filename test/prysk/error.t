-- Setup -----------------------------------------------------------------------

  $ cd "$TESTDIR"
  $ DATADIR=../data

-- Check Conversion of Data Containing Error -----------------------------------

  $ wpkonverter "${DATADIR}/error.csv" 2>&1
  Unable to parse data in mail 1:
  
  ┆ 
  ┆ Ich nehme teil an folgenden Programmpunkten teil:
  ┆ Dienstag 6.10.2026 - Come Together, Mittwoch 7.10.2026 - 1. Kongresstag, Mittwoch 7.10.2026 - Galadinner, Donnerstag 8.10.2026 - 2. Kongresstag
  ┆ 
  ┆ Begleitperson Error: ja
     ^
     Expected Keyword 'Begleitperson:', found 'Begleitperson'  \(at char \d+\), \(line:16, col:1\) (re)
  ┆ Speaker+1 Speaker+1
  
  Unable to parse 1 mail
  Stored data of 0 successfully parsed mails in “../data/error.xlsx”
  [1]

-- Check Conversion of Unreadable Data -----------------------------------------

  $ wpkonverter "${DATADIR}/garbage"
  Unable to determine text encoding of file “../data/garbage”
  [1]

-- Cleanup ---------------------------------------------------------------------

  $ rm -f "${DATADIR}/error.xlsx"