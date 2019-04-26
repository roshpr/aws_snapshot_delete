import json, subprocess


def remove_unused_snaps(profile,region):
    line = 'aws --profile {0} ec2 describe-images --region {1} --owners self'.format(profile,region)
    p = subprocess.Popen(line.split(),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print err
    obj = json.loads(out.decode("utf-8"))

    snaps_used = set(i['BlockDeviceMappings'][0]['Ebs']['SnapshotId'] for i in obj['Images'])

    line = 'aws --profile {0} ec2 describe-snapshots --region {1} --owner-ids self'.format(profile,region)
    p = subprocess.Popen(line.split(),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print err
    obj = json.loads(out.decode("utf-8"))

    snaps_old = set(i['SnapshotId'] for i in obj['Snapshots'])
    print 'Skip AMI snapshots {}\n\n'.format(list(snaps_old & snaps_used))
    line = 'aws --profile {0} ec2 delete-snapshot --region {1} --snapshot-id'.format(profile,region)
    count = 0
    for snap in list(snaps_old - snaps_used):
        print line, snap
        p = subprocess.Popen(line.split() + [snap],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print(count, snap, out, err)
        count += 1

remove_unused_snaps('us-west-2','us-west-2')
