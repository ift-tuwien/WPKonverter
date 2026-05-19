-- Setup -----------------------------------------------------------------------

  $ cd "$TESTDIR"
  $ DATADIR=../data

-- Check Conversion of Test Data -----------------------------------------------

  $ wpkonverter "${DATADIR}/works.csv"
  Stored data in “../data/works.xlsx”

-- Cleanup ---------------------------------------------------------------------

  $ rm -f "${DATADIR}/works.xlsx"