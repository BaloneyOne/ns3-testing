# ns3-testing

This repository hosts wrappers around the ns3 testing system in order to ease some common operations.

For instance, it can load specific command line arguments if the chosen test supports extra arguments.
This way tests can run extra scripts before running or other scripts to postprocess the data.

For instance, the mptcp-tcp test will:
1. Empty statistics folders
2. Run
3. Generate plots based on the newly saved statistics

Helper scripts to help debug ns3 applications (wrappers)
