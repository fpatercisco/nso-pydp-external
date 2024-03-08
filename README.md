pydp-external: An Example Python Data Provider for NSO
======================================================

A python data provider for NSO that retrieves data from external sources.

Building
--------
1. Deploy this repo to `$NCS_DIR/packages/pydp-external`
2. Source your `ncsrc`
3. `make -C src packages/pydp-external/src`       ## builds the fxs from the yang
4. Start NSO if necessary (`ncs`)
5. `echo 'request packages reload' | ncs_cli -u admin`

Watching it Work
----------------
1. In one window, start `tail -F $NCSDIR/logs/ncs-python-vm-pydp-external.log`  ## assuming you haven't mucked w/ the logfile prefix settings
   - Verify that you get the `ComponentThread:main: - Main RUNNING` log message
2. In another window, start ncs_cli (`ncs_cli -u admin`)
3. *_TBD_*
4. Notice the log message(s) in `$NCSDIR/logs/ncs-python-vm-pydp-external.log` showing the data provider handler being called.

