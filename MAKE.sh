
if [[ $1 == 'compile' ]]
then
  python3 C_compile_data.py
fi

if [[ $1 == 'analyze' ]]
then
  python3 C_analyze.py runs=500000 hp matrix=fitch
  python3 C_analyze.py runs=500000 hp matrix=sankoff
  python3 C_analyze.py runs=500000 hp matrix=diwest
fi

if [[ $1 == 'plot' ]]
then
  python3 C_analyze.py plot matrix=fitch tree=R_fitch_consensus.tre
  python3 C_analyze.py plot matrix=sankoff tree=R_sankoff_consensus.tre
  python3 C_analyze.py plot matrix=diwest tree=R_diwest_consensus.tre
  python3 C_analyze.py plot matrix=diwest tree=E_chacon_2014.tre alias=CHACON
  python3 C_analyze.py plot matrix=diwest tree=E_consensus.tre alias=CONSENSUS
  python3 C_analyze.py plot matrix=sankoff tree=R_sankoff_consensus-rooted.tre alias=SANKOFF_ROOTED
  python3 C_analyze.py plot matrix=fitch tree=R_fitch_consensus-rooted.tre alias=FITCH_ROOTED
fi

if [[ $1 == 'proto' ]]
then
  python3 C_analyze.py proto matrix=fitch tree=R_fitch_consensus.tre
  python3 C_analyze.py proto matrix=sankoff tree=R_sankoff_consensus.tre
  python3 C_analyze.py proto matrix=diwest tree=R_diwest_consensus.tre
fi

if [[ $1 == 'homoplasy' ]]
then
  python3 C_analyze.py homoplasy matrix=fitch tree=R_fitch_consensus.tre
  python3 C_analyze.py homoplasy matrix=sankoff tree=R_sankoff_consensus.tre
  python3 C_analyze.py homoplasy matrix=diwest tree=R_diwest_consensus.tre
fi

