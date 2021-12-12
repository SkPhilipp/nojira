# Nojira

Documentation as project management. Synchronizes your documents as GitHub Issues, Projects, Cards, Labels & Milestones. All you
have to do is write documentation and close issues.

## Functionalities

- Documents' paths are synchronized with GitHub Labels, i.e. `'designs/users.md'` will become Labels `designs`, `users`.
- Documents' parent directories are synchronized with GitHub Projects, i.e. `'designs/users.md'` will become a Project `Designs`.
- Documents' markdown headers (`###`, exclusively) are synchronized with GitHub Issues, i.e. `'designs/users.md'`'s
  header `#### User Names` becomes Issue `'Users: User Names'`.
- Documents' GitHub Issues are added as Cards to their respective parent directory's Project.
- Documents' GitHub Issues receive the labels created by their parent directory.
- Documents' GitHub Labels are synchronized with GitHub Milestones when they match the pattern `v\d+`.

## Example

A project with the following structure:

    +- README.md
    +- designs
        +- users.md

And the following content in `users.md`, will set up;

    ### User Names

    (...)

- A Project "Designs"
- Labels "designs", "users" and "v1"
- A Milestone "v1"
- A GitHub Issue and its Card on Project "Designs" named "Users: User Names", labelled with "designs", "users" and "v1" and a
  marker label to indicate automation

## Install

```shell
pip install -r requirements.txt
```
