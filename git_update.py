import pygit2
import os

currentDirectory = os.getcwd()
repository_path = pygit2.discover_repository(currentDirectory)
repo = pygit2.Repository(repository_path)

remoteName = repo.remotes[0].name
remote = repo.remotes[remoteName]
credentials = pygit2.UserPass('b03a55b8cec0e62743a73421d4f7cf29a3866d19', 'x-oauth-basic')
callbacks = pygit2.RemoteCallbacks(credentials=credentials)
remote.fetch(callbacks=callbacks)
# Update local repo
remote_master_id = repo.lookup_reference(
    'refs/remotes/origin/%s' % (repo.head.shorthand)).target
merge_result, _ = repo.merge_analysis(remote_master_id)
if merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
    repo.checkout_tree(repo.get(remote_master_id))
    master_ref = repo.lookup_reference(repo.head.name)
    master_ref.set_target(remote_master_id)
    repo.head.set_target(remote_master_id)
#Update a local file
with open('test_push.txt', 'a') as f:
    f.write("Adding a new line\n")
commit_message = "testing push with pygit2"
index = repo.index
status = repo.status()
diff_status = [k for k in status.keys() if not repo.path_is_ignored(k)]
#Add and commit the files changed
if len(diff_status):
    for changed_file in diff_status:
        if not repo.path_is_ignored(changed_file):
            index.add(changed_file)
            index.write()
tree = index.write_tree()

user = pygit2.Signature(
    'Praveen', 'praveen.kanna39@gmail.com')
oid = repo.create_commit(repo.head.name,
                                 user, user, commit_message, tree, [repo.head.target])

repo.head.set_target(oid)
remote.push([repo.head.name], callbacks=callbacks)