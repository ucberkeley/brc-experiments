# TODO
- [X] unix group 'bceadm' on the SAVIO cluster
- [X] directory to start installing BCE software stack on Savio
  - temporarily located at `/global/home/groups/BCE`
- [ ] building packages in BCE directory
- [ ] create versioned BCE modules like `bce/0.1.3`
- [ ] make versioned BCE modules visible to all Savio users
- [ ] permanent location for the BCE stack with backups and proper access
  - [ ] will BCE module installation and maintenance be handled by non-BRC staff (e.g. SCF / D-Lab)?
- [ ] BCE requirements spec for future BCE releases

# Use Case

Access from [UC Berkeley's Institutional HPC Cluster
(Savio)](http://research-it.berkeley.edu/services/high-performance-computing/institutional-and-condo-computing)
to the analytics stacks and other [commonly requested
software](https://www.xsede.org/xsede-nsf-release-cloud-survey-report)
identified by campus partners, D-Lab and SCF, in the Social Sciences
and Statistics, as bundled in the [Berkeley Compute Environment
(BCE)](http://collaboratool.berkeley.edu/) as a reference platform
which allows mobilitiy of compute so that software developed on a
laptop virtual machine (VM) will run on the HPC cluster without
further work by end users.

# Instructions

Log into Savio and load the BCE module:

    ssh username@hpc.brc.berkeley.edu
    export MODULEPATH=/global/home/groups/BCE:$MODULEPATH
    module load bce-0.1.3
