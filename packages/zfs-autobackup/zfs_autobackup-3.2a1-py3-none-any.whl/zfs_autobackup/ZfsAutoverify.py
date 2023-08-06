import os
import time

from .ExecuteNode import ExecuteNode
from .ZfsAuto import ZfsAuto
from .ZfsDataset import ZfsDataset
from .ZfsNode import ZfsNode
import sys
import platform

def tmp_name(suffix=""):
    """create temporary name unique to this process and node"""

    #we could use uuids but those are ugly and confusing
    name="zfstmp_{}_{}".format(platform.node(), os.getpid())
    name=name+suffix
    return name

def hash_tree_tar(node, path):
    """calculate md5sum of a directory tree, using tar"""

    node.debug("Hashing filesystem {} ".format(path))

    cmd=[ "tar", "-cf", "-", "-C", path, ".",
          ExecuteNode.PIPE, "md5sum"]

    stdout = node.run(cmd)

    if node.readonly:
        hashed=None
    else:
        hashed = stdout[0].split(" ")[0]

    node.debug("Hash of {} filesytem is {}".format(path, hashed))

    return hashed


def compare_trees_tar(source_node, source_path, target_node, target_path):
    """compare two trees using tar. compatible and simple"""

    source_hash= hash_tree_tar(source_node, source_path)
    target_hash= hash_tree_tar(target_node, target_path)

    if source_hash != target_hash:
        raise Exception("md5hash difference: {} != {}".format(source_hash, target_hash))


def compare_trees_rsync(source_node, source_path, target_node, target_path):
    """use rsync to compare two trees.
     Advantage is that we can see which individual files differ.
     But requires rsync and cant do remote to remote."""

    cmd = ["rsync", "-rcn", "--info=COPY,DEL,MISC,NAME,SYMSAFE", "--msgs2stderr", "--delete" ]

    #local
    if source_node.ssh_to is None and target_node.ssh_to is None:
        cmd.append("{}/".format(source_path))
        cmd.append("{}/".format(target_path))
        source_node.debug("Running rsync locally, on source.")
        stdout, stderr = source_node.run(cmd, return_stderr=True)

    #source is local
    elif source_node.ssh_to is None and target_node.ssh_to is not None:
        cmd.append("{}/".format(source_path))
        cmd.append("{}:{}/".format(target_node.ssh_to, target_path))
        source_node.debug("Running rsync locally, on source.")
        stdout, stderr = source_node.run(cmd, return_stderr=True)

    #target is local
    elif source_node.ssh_to is not None and target_node.ssh_to is None:
        cmd.append("{}:{}/".format(source_node.ssh_to, source_path))
        cmd.append("{}/".format(target_path))
        source_node.debug("Running rsync locally, on target.")
        stdout, stderr=target_node.run(cmd, return_stderr=True)

    else:
        raise Exception("Source and target cant both be remote when verifying. (rsync limitation)")

    if stderr:
        raise Exception("Dataset verify failed, see above list for differences")


def verify_filesystem(source_snapshot, source_mnt, target_snapshot, target_mnt, method):
    """Compare the contents of two zfs filesystem snapshots """

    try:

        # mount the snapshots
        source_snapshot.mount(source_mnt)
        target_snapshot.mount(target_mnt)

        if method=='rsync':
            compare_trees_rsync(source_snapshot.zfs_node, source_mnt, target_snapshot.zfs_node, target_mnt)
        elif method == 'tar':
            compare_trees_tar(source_snapshot.zfs_node, source_mnt, target_snapshot.zfs_node, target_mnt)
        else:
            raise(Exception("program errror, unknown method"))

    finally:
        source_snapshot.unmount()
        target_snapshot.unmount()


def hash_dev(node, dev):
    """calculate md5sum of a device on a node"""

    node.debug("Hashing volume {} ".format(dev))

    cmd = [ "md5sum", dev ]

    stdout = node.run(cmd)

    if node.readonly:
        hashed=None
    else:
        hashed = stdout[0].split(" ")[0]

    node.debug("Hash of volume {} is {}".format(dev, hashed))

    return hashed

# def activate_volume_snapshot(dataset, snapshot):
#     """enables snapdev, waits and tries to findout /dev path to the volume, in a compatible way. (linux/freebsd/smartos)"""
#
#     dataset.set("snapdev", "visible")
#
#     #NOTE: add smartos location to this list as well
#     locations=[
#         "/dev/zvol/" + snapshot.name
#     ]
#
#     dataset.debug("Waiting for /dev entry to appear...")
#     time.sleep(0.1)
#
#     start_time=time.time()
#     while time.time()-start_time<10:
#         for location in locations:
#             stdout, stderr, exit_code=dataset.zfs_node.run(["test", "-e", location], return_all=True, valid_exitcodes=[0,1])
#
#             #fake it in testmode
#             if dataset.zfs_node.readonly:
#                 return location
#
#             if exit_code==0:
#                 return location
#         time.sleep(1)
#
#     raise(Exception("Timeout while waiting for {} entry to appear.".format(locations)))
#
# def deacitvate_volume_snapshot(dataset):
#     dataset.inherit("snapdev")

#NOTE: https://www.google.com/search?q=Mount+Path+Limit+freebsd
#Freebsd has limitations regarding path length, so we cant use the above method.
#Instead we create a temporary clone

def get_tmp_clone_name(snapshot):
    pool=snapshot.zfs_node.get_pool(snapshot)
    return pool.name+"/"+tmp_name()

def activate_volume_snapshot(snapshot):
    """clone volume, waits and tries to findout /dev path to the volume, in a compatible way. (linux/freebsd/smartos)"""

    clone_name=get_tmp_clone_name(snapshot)
    clone=snapshot.clone(clone_name)

    #NOTE: add smartos location to this list as well
    locations=[
        "/dev/zvol/" + clone_name
    ]

    clone.debug("Waiting for /dev entry to appear...")
    time.sleep(0.1)

    start_time=time.time()
    while time.time()-start_time<10:
        for location in locations:
            stdout, stderr, exit_code=clone.zfs_node.run(["test", "-e", location], return_all=True, valid_exitcodes=[0,1])

            #fake it in testmode
            if clone.zfs_node.readonly:
                return location

            if exit_code==0:
                return location
        time.sleep(1)

    raise(Exception("Timeout while waiting for {} entry to appear.".format(locations)))

def deacitvate_volume_snapshot(snapshot):
    clone_name=get_tmp_clone_name(snapshot)
    clone=snapshot.zfs_node.get_dataset(clone_name)
    clone.destroy()

def verify_volume(source_dataset, source_snapshot, target_dataset, target_snapshot):
    """compare the contents of two zfs volume snapshots"""

    try:
        source_dev= activate_volume_snapshot(source_snapshot)
        target_dev= activate_volume_snapshot(target_snapshot)

        source_hash= hash_dev(source_snapshot.zfs_node, source_dev)
        target_hash= hash_dev(target_snapshot.zfs_node, target_dev)

        if source_hash!=target_hash:
            raise Exception("md5hash difference: {} != {}".format(source_hash, target_hash))

    finally:
        deacitvate_volume_snapshot(source_snapshot)
        deacitvate_volume_snapshot(target_snapshot)

def create_mountpoints(source_node, target_node):

    # prepare mount points
    source_node.debug("Create temporary mount point")
    source_mnt = "/tmp/"+tmp_name("source")
    source_node.run(["mkdir", source_mnt])

    target_node.debug("Create temporary mount point")
    target_mnt = "/tmp/"+tmp_name("target")
    target_node.run(["mkdir", target_mnt])

    return source_mnt, target_mnt


def cleanup_mountpoint(node, mnt):
    node.debug("Cleaning up temporary mount point")
    node.run([ "rmdir", mnt ], hide_errors=True, valid_exitcodes=[] )


class ZfsAutoverify(ZfsAuto):
    """The zfs-autoverify class, default agruments and stuff come from ZfsAuto"""

    def __init__(self, argv, print_arguments=True):

        # NOTE: common options and parameters are in ZfsAuto
        super(ZfsAutoverify, self).__init__(argv, print_arguments)

    def parse_args(self, argv):
        """do extra checks on common args"""

        args=super(ZfsAutoverify, self).parse_args(argv)

        if args.target_path == None:
            self.log.error("Please specify TARGET-PATH")
            sys.exit(255)

        return args

    def get_parser(self):
        """extend common parser with  extra stuff needed for zfs-autobackup"""

        parser=super(ZfsAutoverify, self).get_parser()

        group=parser.add_argument_group("Verify options")
        group.add_argument('--fs-compare', metavar='METHOD', default="tar", choices=["tar", "rsync"],
                            help='Compare method to use for filesystems. (tar, rsync) Default: %(default)s ')

        return parser

    def verify_datasets(self, source_mnt, source_datasets, target_node, target_mnt):

        fail_count=0
        count = 0
        for source_dataset in source_datasets:

            # stats
            if self.args.progress:
                count = count + 1
                self.progress("Analysing dataset {}/{} ({} failed)".format(count, len(source_datasets), fail_count))

            try:
                # determine corresponding target_dataset
                target_name = self.make_target_name(source_dataset)
                target_dataset = target_node.get_dataset(target_name)

                # find common snapshots to  verify
                source_snapshot = source_dataset.find_common_snapshot(target_dataset)
                target_snapshot = target_dataset.find_snapshot(source_snapshot)

                if source_snapshot is None or target_snapshot is None:
                    raise(Exception("Cant find common snapshot"))

                target_snapshot.verbose("Verifying...")

                if source_dataset.properties['type']=="filesystem":
                    verify_filesystem(source_snapshot, source_mnt, target_snapshot, target_mnt, self.args.fs_compare)
                elif source_dataset.properties['type']=="volume":
                    verify_volume(source_dataset, source_snapshot, target_dataset, target_snapshot)
                else:
                    raise(Exception("{} has unknown type {}".format(source_dataset, source_dataset.properties['type'])))


            except Exception as e:
                if self.args.progress:
                    self.clear_progress()

                fail_count = fail_count + 1
                target_dataset.error("FAILED: " + str(e))
                if self.args.debug:
                    self.verbose("Debug mode, aborting on first error")
                    raise

        if self.args.progress:
            self.clear_progress()

        return fail_count

    def run(self):

        source_node=None
        source_mnt=None
        target_node=None
        target_mnt=None


        try:

            ################ create source zfsNode
            self.set_title("Source settings")

            description = "[Source]"
            source_node = ZfsNode(snapshot_time_format=self.snapshot_time_format, hold_name=self.hold_name, logger=self,
                                  ssh_config=self.args.ssh_config,
                                  ssh_to=self.args.ssh_source, readonly=self.args.test,
                                  debug_output=self.args.debug_output, description=description)

            ################# select source datasets
            self.set_title("Selecting")
            source_datasets = source_node.selected_datasets(property_name=self.property_name,
                                                            exclude_received=self.args.exclude_received,
                                                            exclude_paths=self.exclude_paths,
                                                            exclude_unchanged=self.args.exclude_unchanged,
                                                            min_change=0)
            if not source_datasets:
                self.print_error_sources()
                return 255

            # create target_node
            self.set_title("Target settings")
            target_node = ZfsNode(snapshot_time_format=self.snapshot_time_format, hold_name=self.hold_name,
                                  logger=self, ssh_config=self.args.ssh_config,
                                  ssh_to=self.args.ssh_target,
                                  readonly=self.args.test, debug_output=self.args.debug_output,
                                  description="[Target]")
            target_node.verbose("Verify datasets under: {}".format(self.args.target_path))

            self.set_title("Verifying")

            source_mnt, target_mnt= create_mountpoints(source_node, target_node)

            fail_count = self.verify_datasets(
                source_mnt=source_mnt,
                source_datasets=source_datasets,
                target_mnt=target_mnt,
                target_node=target_node)

            if not fail_count:
                if self.args.test:
                    self.set_title("All tests successful.")
                else:
                    self.set_title("All datasets verified ok")

            else:
                if fail_count != 255:
                    self.error("{} dataset(s) failed!".format(fail_count))

            if self.args.test:
                self.verbose("")
                self.warning("TEST MODE - DID NOT VERIFY ANYTHING!")

            return fail_count

        except Exception as e:
            self.error("Exception: " + str(e))
            if self.args.debug:
                raise
            return 255
        except KeyboardInterrupt:
            self.error("Aborted")
            return 255
        finally:

            # cleanup
            if source_mnt is not None:
                cleanup_mountpoint(source_node, source_mnt)

            if target_mnt is not None:
                cleanup_mountpoint(target_node, target_mnt)




def cli():
    import sys

    sys.exit(ZfsAutoverify(sys.argv[1:], False).run())


if __name__ == "__main__":
    cli()
