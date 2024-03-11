pydp-external: An Example Python Data Provider for NSO
======================================================

A python data provider for NSO that retrieves data from external sources, specifically <http://numbersapi.com> and <https://random-word-api.herokuapp.com>.

Building
--------
1. Deploy this repo to `$NCS_DIR/packages/pydp-external`
2. Source your `ncsrc`
3. `make -C packages/pydp-external/src`       ## builds the fxs from the yang
4. Start NSO if necessary (`ncs`)
5. `echo 'request packages reload' | ncs_cli -u admin`

Watching it Work
----------------
1. In one window, start `tail -F $NCSDIR/logs/ncs-python-vm-pydp-external.log`  ## assuming you haven't mucked w/ the logfile prefix settings
   - Verify that you get the `ComponentThread:main: - Main RUNNING` log message
2. In another window, start ncs_cli (`ncs_cli -u admin`)
3. In ncs_cli, create an instance of `external-data`:

		admin@ncs> configure
		Entering configuration mode private
		[ok][2024-03-11 13:17:31]
		
		[edit]
		admin@ncs% set external-data instance foo 
		[ok][2024-03-11 13:17:42]
		
		[edit]
		admin@ncs% commit
		Commit complete.
		[ok][2024-03-11 13:17:46]
		
		[edit]
		admin@ncs%
		exit
		[ok][2024-03-11 13:19:11]
		admin@ncs> show external-data instance foo ?
		Description: An instance of external-data
		Possible completions:
		  numbers - External number data from http://numbersapi.com
		  words   - External word data from https://random-word-api.herokuapp.com
		admin@ncs> show external-data instance foo
		NAME  TRIVIA                                                          MATH                                      RANDOM  
		------------------------------------------------------------------------------------------------------------------------
		foo   564000 is the number of words in War and Peace by Leo Tolstoy.  880 is the number of 4×4 magic squares.  tides   
		
		[ok][2024-03-11 13:19:24]
		admin@ncs>
		
4. Notice the log messages in `$NCSDIR/logs/ncs-python-vm-pydp-external.log` showing the different data provider handlers being called. Test out what happens if you execute `show external-data instance foo numbers` or `show external-data instance foo words random`.

Next Steps
----------
As this and all the example Python data provider code I've seen uses the `experimental.DataCallbacks` helper class that's [_experimental_](https://community.cisco.com/t5/nso-developer-hub-discussions/python-datacallback-daemon/m-p/3951604/highlight/true#M4457) and [incomplete](https://developer.cisco.com/docs/nso/api/#!ncs-experimental/ncs.experimental.DataCallbacks), I'd like to implement a Python data provider for config data similar to the Java implementation in the NSO 6.2.1 distribution's `examples.ncs/getting-started/developing-with-ncs/6-extern-db` example. As I read the doc for [\_ncs.dp.register\_data\_cb](https://developer.cisco.com/docs/nso/api/#!_ncs-dp/_ncs.dp.register_data_cb), this should just require implementing a class with all the methods listed there.

As further study, I'd also like to better understand the relationship between the placement of the callpoint in the yang and the format of what the handler code returns, i.e. from `DataCallbacks.get_*` or from the handler class passed to `_ncs.dp.register_data_cb`'s various methods.
