# Disclaimer

No warranty is given that the presented method works as expected and that it does not destroy anything. Use at your own risk!

# Prerequisites

* `git-clang-format` installed somewhere in the `$PATH`. `git-clang-format` might be shipped with `clang` in your distro and is also available from [here](https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/git-clang-format).

# Operating system

This should work on Linux.

# How to apply clang-format to a series of commits?

The following ingredients are needed:
* `git rebase` can execute a command after each commit
* We use that feature (`-x`) to execute `git clang-format` after each commit, which will reformat only the files that changed in that commit.
* Afterwards `git diff` shows the changes introduced by `git clang-format`
* The user is prompted to hit enter, making it possible to examine small diffs, where `git diff` immediately returns.
* Finally the formatting changes are added to the preceding commit

Since `clang-format` changes the formatting after each original commit, it is very likely that it introduces conflicts with the subsequent commits. Since we know that these conflicts are due to (i) changes in formatting in the already rebased commits (ii) more profound changes in the subsequent commits, it is a sensible setting, to just take the changes from the new commits in each conflicting case. This is accomplished by choosing the merge strategy `-X theirs`. :warning: This strategy automatically resolves conflicts, but if the changes in both code and formatting are too complex for the algorithm, it might generate wrong results! Therefore it is recommended to always double-check that the reformatting did not mess anything up!

:warning: If you use the command given below, make sure you have a backup, at least of the branch that you are going to rebase! If you don't understand (even after the explanation) what this command does, you better do not use it!

```{sh}
git rebase -i COMMIT_ONTO_WHICH_TO_REBASE \
  -X theirs \
  -x "git clang-format HEAD^ \
      && git diff \
      && read -r -p 'Hit enter to continue' \
      && git commit --all --amend --no-edit"
```

## filter-branch solution

To apply `clang-format` to each commit in the range `COMMIT..HEAD` rewriting the history:
```sh
git filter-branch --tree-filter 'git-clang-format $GIT_COMMIT^' -- COMMIT..HEAD
```
