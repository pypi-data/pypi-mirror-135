# RDEER-SERVICE


rdeer-service is a tool to facilitate the use of [Reindeer](https://github.com/kamimrcht/REINDEER) as socket mode.
It also summarize its outputs.

It is a companion to Transipedia, a web application to query easily and fastly Reindeer.

## Installation

**Recommanded (pip)**


```
python3 -m pip install rdeer-service
```

**Other (git)**

```
git clone https://github.com/Bio2M/rdeer-service.git
```


## How to use?

### Prerequisite

[Reindeer](https://github.com/kamimrcht/REINDEER) must be installed and accessible by your PATH.

### Start the server

the server must be in the same physical server than Reindeer, You can have multiple servers with Reindeer.  Each of them must have the server.

```
rdeer-server /path/to/indexes
```

* rdeer-server listen on port 12800, you can change this with `--port` option.
* The server will only be able to handle indexes in the specified directory. If your indexes are spread over several directories, you may create symlinks in `/path/to/indexes`.
* You can add, remove or change the name of the indexes, rdeer-server takes the changes on the fly.
* It is recommanded to start rdeer-server as a daemon, using systemd, supervisord or whatever.



### Use the client

The client could requests remote rdeer-server servers. You can enterely manage yours Reindeer indexes with subcommand:

* ``list`` to show all indexes with their status
* ``start <index-name>`` to start a index (the index name is the directory hosting the index files)
* `stop <index-name>` to stop a index
* `check <index-name>` to verify if index responding

**show all indexes:**

```
rdeer-client list
```

list all accessible indexes by rdeer-server, with status. Status are : 

* `available` the index is not running
* `loading` the index is in a transitional mode until the running mode
* `running` the index is started, and can be resquested.

**Start an index:**

```
rdeer-client start my-index
```

Will starts the **my-index** Reindeer index. When status is `running`, the index is ready to respond to requests.

**Query an index**

```
rdeer-client query my-index -q fasta-query
```

Requests the specified index, the query file is required and must be in a fasta format.

Options of query subcommand (`rdeer-client query --help`):

* `-q`, `--query` to send a query file at the fasta format (**required**)
* `-n`, `--normalize` to obtain normalized counts
* `-s`, `--server` to request rdeer-server on remote host
* `-p`, `--port` to resquest rdeer-server on a specified port (default: 12800)
* `-o`, `--outfile` output is stdout by default, you can specified a file

