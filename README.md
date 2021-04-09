# Use-Case

The script `event-logger.py` generates syslog every 30 seconds. The workflow is:
1. Daemon "eventlogger" below executes the python script `event-logger.py`. It is shutdown by default. Do not unshut it yet.
2. Event-handler `start-logger` will unshut the daemon when syslog with regex `%CAPACITY-1-UTILIZATION_HIGH: AegisPrefix-Resource` is generated. The daemon will keep running in the background.
3. Event-handler `stop-logger` will shutdown the daemon when syslog with regex `%CAPACITY-1-UTILIZATION_NORMAL: AegisPrefix-Resource` is generated. The daemon will quit immediately.

# Config

Daemon:

```
daemon eventlogger
   exec /mnt/flash/event-logger.py
```

Event-handlers:

```
event-handler start-logging
   action bash FastCli -p15 -c $'conf\ndaemon eventlogger\n no shutdown'
   delay 0
   !
   trigger on-logging
      regex %CAPACITY-1-UTILIZATION_HIGH: AegisPrefix-Resource
event-handler stop-logging-daemon
   action bash FastCli -p15 -c $'conf\ndaemon eventlogger\n shutdown'
   delay 0
   !
   trigger on-logging
      regex %CAPACITY-1-UTILIZATION_NORMAL: AegisPrefix-Resource
```

# Example Run:

```

pe1-ghb265(config)#show daemon eventlogger
Process: eventlogger (shutdown with PID 13893)
No configuration options stored.

No status data stored.

pe1-ghb265(config)#
```


Crafting a syslog message to trigger the event-handler `start-logger`. As you can see the message "custom log - CAPACITY-1-UTILIZATION_HIGH" is being logged every 30 seconds.

```pe1-ghb265#  send log message %CAPACITY-1-UTILIZATION_HIGH: AegisPrefix-Resource4-Fap0.0 table utilization is currently at 66%, crossed threshold 50%```




```
Apr  9 08:53:07 pe1-ghb265 ConfigAgent: %SYS-6-LOGMSG_INFO: Message from admin on vty3 (10.95.69.90): %CAPACITY-1-UTILIZATION_HIGH: AegisPrefix-Resour
ce4-Fap0.0 table utilization is currently at 66%, crossed threshold 50%
Apr  9 08:53:08 pe1-ghb265 EventMgr: %SYS-6-EVENT_TRIGGERED: Event handler start-logging was activated
Apr  9 08:53:08 pe1-ghb265 ConfigAgent: %SYS-5-CONFIG_E: Enter configuration mode from console by root on UnknownTty (UnknownIpAddr)
Apr  9 08:53:08 pe1-ghb265 ConfigAgent: %SYS-5-CONFIG_I: Configured from console by root on UnknownTty (UnknownIpAddr)
Apr  9 08:53:08 pe1-ghb265 Launcher: %LAUNCHER-6-PROCESS_START: Configuring process 'eventlogger' to start in role 'ActiveSupervisor'
Apr  9 08:53:08 pe1-ghb265 ProcMgr-worker: %PROCMGR-6-WORKER_WARMSTART: ProcMgr worker warm start. (PID=2203)
Apr  9 08:53:08 pe1-ghb265 ProcMgr-worker: %PROCMGR-7-NEW_PROCESSES: New processes configured to run under ProcMgr control: ['eventlogger']
<SKIP>
Apr  9 08:53:08 pe1-ghb265 event-logger.py: custom log - CAPACITY-1-UTILIZATION_HIGH
Apr  9 08:53:38 pe1-ghb265 event-logger.py: custom log - CAPACITY-1-UTILIZATION_HIGH
Apr  9 08:54:08 pe1-ghb265 event-logger.py: custom log - CAPACITY-1-UTILIZATION_HIGH
```

Now crafting a syslog message to trigger the event-handler `stop-logger`. As you can see daemon eventlogger is terminated successfully.

Apr  9 08:56:09 pe1-ghb265 event-logger.py: custom log - CAPACITY-1-UTILIZATION_HIGH
Apr  9 08:56:15 pe1-ghb265 ConfigAgent: %SYS-6-LOGMSG_INFO: Message from admin on vty3 (10.95.69.90): %CAPACITY-1-UTILIZATION_NORMAL: AegisPrefix-Resource4-Fap0.0 table utilization is back to normal
Apr  9 08:56:15 pe1-ghb265 EventMgr: %SYS-6-EVENT_TRIGGERED: Event handler stop-logging-daemon was activated
Apr  9 08:56:15 pe1-ghb265 ConfigAgent: %SYS-5-CONFIG_E: Enter configuration mode from console by root on UnknownTty (UnknownIpAddr)
Apr  9 08:56:15 pe1-ghb265 ConfigAgent: %SYS-5-CONFIG_I: Configured from console by root on UnknownTty (UnknownIpAddr)
Apr  9 08:56:15 pe1-ghb265 Launcher: %LAUNCHER-6-PROCESS_STOP: Configuring process 'eventlogger' to stop in role 'ActiveSupervisor'
Apr  9 08:56:15 pe1-ghb265 ProcMgr-worker: %PROCMGR-6-WORKER_WARMSTART: ProcMgr worker warm start. (PID=2203)
<SKIP>
Apr  9 08:56:15 pe1-ghb265 ProcMgr-worker: %PROCMGR-6-TERMINATE_RUNNING_PROCESS: Terminating deconfigured/reconfigured process 'eventlogger' (PID=21554)
Apr  9 08:56:15 pe1-ghb265 ProcMgr-worker: %PROCMGR-7-WORKER_WARMSTART_DONE: ProcMgr worker warm start done. (PID=2203)
Apr  9 08:56:16 pe1-ghb265 ProcMgr-worker: %PROCMGR-6-PROCESS_TERMINATED: 'eventlogger' (PID=21554, status=9) has terminated.
