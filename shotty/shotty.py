import boto3
import botocore
import click


session = boto3.Session(profile_name='default')
ec2 = session.resource('ec2')

@click.group()
def cli():
    """Shotty manages snapshots"""
    
@cli.group("snapshots")
def snapshots():
    """Commands for snapshots"""
    
    
@snapshots.command('list')
@click.option("--project", default=None,
    help="Only snapshots for project (tag tutorials:<name>)")
def list_snapshots(project):
    "List EC2 volume snapshots"
    instances = filter_instances(project)
    
    for i in instances.all(): 
        for v in i.volumes.all(): 
            for s in v.snapshots.all():
                 print(",".join((s.id,
                                v.id, 
                                i.id,
                                s.state,
                                s.progress,
                                s.start_time.strftime("%c")
                 )))
    

@cli.group('volumes')
def volumes():
    """Commands for volumes"""
    
@volumes.command('list')
@click.option("--project", default=None,
    help="Only volumes for project (tag tutorials:<name>)")
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)
    
    for i in instances.all(): 
        for v in i.volumes.all(): 
                 print(",".join((v.id, i.id,v.state,str(v.size)+"GiB", 
                 v.encrypted and "Encrypted" or "Not Encrypted" 
                 ))) 
    
@cli.group('instances')
def instances():
    """Commands for instances"""
    
def filter_instances(project):
    instances = []

    if project:
        filters = [
            {
                'Name':'tag:tutorials',
                'Values':[project]
                
            }
        ] 
        instances = ec2.instances.filter(Filters=filters) 
    else:
        instances = ec2.instances.all()
    
    return instances
    
@instances.command("snapshot")
@click.option("--project", default=None,
    help="Only instances for project (tag tutorials:<name>)")
def create_snapshots(project):
    """Create snapshots for EC2 instances"""
    
    instances = filter_instances(project)
    
    for i in instances.all():
        print("Stopping instance {0}".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            #Ignore if try to stop in an invalid state
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue;
        
        # Instance must be stopped before snapshot can be taken
        i.wait_until_stopped() 
        
        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshotanalyzer 3000")
            
        # Safe to restart once snapshot process initiated
        print("Starting {0}...".format(i.id))
        try:
            i.start()  
            i.wait_until_running()
        except botocore.exceptions.ClientError as e:
            # Ignore if try to start in an invalid state
            print("Could not start {0}.".format(i.id) + str(e))
            continue;
        
    print("Job's done!")
    return

    
    
    
@instances.command('list')
@click.option("--project", default=None,
    help="Only instances for project (tag tutorials:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] } 
        print(','.join( (
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('tutorials','<no project>'))))
            
@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
    "Stop EC2 instances"
    
    instances = filter_instances(project)

    
    for i in instances:
        print("Stopping instance {0}...".format(i.id))
        try:
            i.stop()  
        except botocore.exceptions.ClientError as e:
            # Ignore if try to start in an invalid state
            print("Could not stop {0}. ".format(i.id) + str(e))
            continue;
        
    
@instances.command('terminate')
@click.option('--project', default=None, help='Only instances for project')
def terminate_instances(project):
    "Terminate EC2 instances"
    
    instances = filter_instances(project)

    for i in instances:
        print("Terminating instance {0}...".format(i.id))
        try:
            i.terminate()  
        except botocore.exceptions.ClientError as e:
            # Ignore if try to terminate in an invalid state
            print("Could not terminate {0}. ".format(i.id) + str(e))
            continue;

@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')
def start_instances(project):
    "Start EC2 instances"
    
    instances = filter_instances(project)

    for i in instances:
        print("Starting instance {0}...".format(i.id))
        try:
            i.start()  
        except botocore.exceptions.ClientError as e:
            # Ignore if try to start in an invalid state
            print("Could not start {0}. ".format(i.id) + str(e))
            continue;
    

if __name__ == '__main__':
    cli()
    