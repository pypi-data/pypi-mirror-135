# LbAPLocal

LbAPLocal is the python library for running offline tests for the LHCb AnalysisProductions framework.


## Usage

LbAPLocal is installed by default with the LHCb environment on lxplus.  For users on external clusters, one can source the LHCb environment from CVMFS to get setup: ``` source /cvmfs/lhcb.cern.ch/lib/LbEnv ```
After installing, LbAPLocal can be run from the command line with the following options:

```
Usage: lb-ap [OPTIONS] COMMAND [ARGS]...

  Command line tool for the LHCb AnalysisProductions

Options:
  --version
  --help     Show this message and exit.

Commands:
  list       List the available production folders by running lb-ap list...
  render     Render the info.yaml for a given production
  validate   Validate the configuration for a given production
  test       Execute a job locally
  debug      Start an interactive session inside the job's environment
  reproduce  Reproduce an existing online test locally
  parse-log  Read a Gaudi log file and extract information
```

To see which productions are available:
```bash
$ lb-ap list
The available productions are:
* MyAnalysis
```

To see which jobs are available for a given production:
```bash
$ lb-ap list MyAnalysis
The available jobs for MyAnalysis are:
* My2016MagDownJob
* My2016MagUpJob
```

To render the templating in `info.yaml` for a given production:
```bash
$ lb-ap render MyAnalysis
```

To validate the configuration of a given production:
```bash
$ lb-ap validate MyAnalysis
Rendering info.yaml for MyAnalysis
YAML parsed successfully
YAML validated successfully
```

To run a test of a job interactively:
```bash
$ lb-ap debug MyAnalysis My2016MagDownJob

Welcome to analysis productions debug mode:

The production can be tested by running:

gaudirun.py -T '$ANALYSIS_PRODUCTIONS_DYNAMIC/Lb2Lll/MC_2017_MagDown_Lb2PsiL_mm_strip_autoconf.py' '$ANALYSIS_PRODUCTIONS_BASE/Lb2Lll/stripping_seq.py' prodConf_DaVinci_00012345_00006789_1.py

[DaVinci v45r5] output $
```

To test a job non-interactively:
```bash
$ lb-ap test MyAnalysis My2016MagDownJob
Success! Output can be found in xxxxxxxxxxxx
```

For both interactive and non-interactive testing, when testing a job that depends on another job to provide the input file the dependent job will be tested first and its output passed to the requested job. If the dependent job has already been run the location of its output can be passed to the requested job by appending `-i <output_file_path>` to `lb-ap test <production_name> <job_name>`.

To test a job on a specific input file:
```bash
$ lb-ap test MyAnalysis My2016MagDownJob -i InputFileLocation
Success! Output can be found in xxxxxxxxxxxx
```
InputFileLocation can be either an LFN or a path to a local file. This is also valid for the debug command.

To read a Gaudi log file and extract information:
```bash
$ lb-ap parse-log Job.log
Summary of log messages in: Job.log
    Found 2659 ERROR messages
        * 2649 instances of "*** Flag container MC/TrackInfo not found."
        * 9 instances of "HltSelReportsDecoder::   Failed to add Hlt selection name Hlt2RecSummary to its container "
        * 1 instances of "HltSelReportsDecoder:: The   ERROR message is suppressed : '  Failed to add Hlt selection name Hlt2RecSummary to its container '"
    Found 61 WARNING messages
        * 7 instances of "TupleToolBremInfo:: TupleToolBremInfo requires fullDST -  BremP and BremOrigin might not be reliable (Multiplicity is OK)"
        and 54 others (50 unique), pass "--suppress=0" to show all messages

Errors have been detected!
  * Lines: 3275, 3277, 3279, 3281, 3283 and 17 others
    This message indicates the location specified for the information being accessed by
    RelatedInfo does not exist. It is likely that either:

    * The location specified is incorrect, try looking for it with dst-dump.
    * The given information was never stored for that candidate, in which case the use of
    RelatedInfo should be removed.

General explanations
  * Line: 6318
    Histograms are not being saved as no filename has been specified for storing them. This
    message is harmless and normally ignored.
Error: Found issues in log
```
