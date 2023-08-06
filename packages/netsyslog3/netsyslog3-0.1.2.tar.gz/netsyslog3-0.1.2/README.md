# netsyslog3

`netsyslog3` enables you to construct syslog messages and send them (via
UDP) to a remote syslog server directly from Python. Unlike other
syslog modules it allows you to set the metadata (e.g. time, host
name, program name, etc.) yourself, giving you full control over the
contents of the UDP packets that it creates.

`netsyslog3` was initially developed for the Hack Saw project, where it
was used to read log messages from a file and inject them into a
network of syslog servers, whilst maintaining the times and hostnames
recorded in the original messages.

The module also allows you to send log messages that contain the
current time, local hostname and calling program name (i.e. the
typical requirement of a logging package) to one or more syslog
servers.

The format of the UDP packets sent by netsyslog3 adheres closely to
that defined in [RFC 3164](http://tools.ietf.org/html/rfc3164).

## Installation

    pip install netsyslog3

## Usage


    $ python3
    >>> import netsyslog3
    >>> import syslog
    >>> logger = netsyslog3.Logger()
    >>> logger.add_host("somehost.mydomain.com")
    >>> logger.add_host("otherhost.mydomain.com")
    >>> logger.log(syslog.LOG_USER, syslog.LOG_NOTICE, "Hey, it works!", pid=True)

The [API docs](http://hacksaw.sourceforge.net/netsyslog/doc/) are also available over on the (old) SourceForge site.
