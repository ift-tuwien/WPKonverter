-- Setup -----------------------------------------------------------------------

  $ cd "$TESTDIR"
  $ DATADIR=../data

-- Check Conversion of Test Data -----------------------------------------------

  $ wpkonverter "${DATADIR}/works.csv"
  Stored data of 8 successfully parsed mails in “../data/works.xlsx”

-- Cleanup ---------------------------------------------------------------------

  $ rm -f "${DATADIR}/works.xlsx"