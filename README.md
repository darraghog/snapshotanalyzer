# snapshotanalyzer
ACG Python AWS project to manage EC2 instance snapshots

## About
This project is a demo, and uses boto3 to manage EC2 snapshots.


## Configuring

shotty uses the configuration files generated by AWS CLI - e.g. on EC2:

```
aws configure --profile default
```

## Running
`pipenv run "python shotty/shotty.py <command> <subcommand> <--project=PROJECT>`

*command* is instances, snapshots or volumes
*subcommand* is list, start, stop depending on <command>
*project* is optional

`