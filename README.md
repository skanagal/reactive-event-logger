# Use-Case

The script `event-logger.py` generates syslog every 30 seconds. The workflow is:
1. Daemon "eventlogger" below executes the python script `event-logger.py`. It is shutdown by default. Do not unshut it yet.
2. Event-handler `start-logger` will unshut the daemon when syslog with regex "%CAPACITY-1-UTILIZATION_HIGH: AegisPrefix-Resource" is generated. The daemon will keep running in the background.
3. Event-handler `stop-logger` will shutdown the daemon when syslog with regex "%CAPACITY-1-UTILIZATION_NORMAL: AegisPrefix-Resource" is generated. The daemon will quit immediately.
