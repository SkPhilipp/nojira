# Nojira

Makes documentation the source of truth for your project boards.

Sets up;
- GitHub Issues (including Labels)
- GitHub Project Boards (including Tasks)
- GitHub Milestones

All you have to do is write documentation and drag tasks to done (or close issues).

## Example

A project with the following structure:

    +- README.md
    +- designs
        +- users.v1.md

And the following content in `users.v1.md`, will set up;

    ### User Names

    (...)

- A Project Board "Designs"
- Labels "designs", "users" and "v1"
- A Milestone "v1"
- A GitHub Issue "User Names (Designs / Users)", labelled with "designs", "users" and "v1"
- A GitHub Task "User Names (Designs / Users)" on Project Board "Designs"

## Functionalities

### Label Synchronization

Directories containing documents are scheduled to become GitHub Labels.
- Path segments become "Scheduled Labels", i.e. `'designs/users.v1.md'` will schedule labels `designs`, `users` and `v1`.

Scheduled Labels and Label synchronization is resolved as follows;
- Scheduled Labels are created if they do not exist.

### Issue Synchronization

Directories containing documents are scheduled to become GitHub Issues and Labels.
- Path segments become part of potential issue titles, i.e. `'designs/users.v1.md'` will add a`(Designs / Users)` suffix to issues scheduled from the document.
- Markdown document headers (`###`, exclusively) become "Scheduled Issues", i.e. `### User Names` will schedule an issue with the title prefix `User Names`.

Scheduled Issues and Issues synchronization is resolved as follows;
- Scheduled Issues are created if they do not exist and no other issue exists with the same suffix to match it with.
- Issues are removed if they do not exist as Scheduled Issues and no other issue exists with the same suffix to match it with.
- Scheduled Issues and Issues matched with each other have their title and body synchronized to that of the Scheduled Issue.

### Project Board Synchronization

Directories are scheduled to become Project Boards.
- Directory names become "Scheduled Project Boards", i.e. `'designs/'` will schedule a project board `Designs`.

Scheduled Project Boards and Project Boards are synchronized as follows;
- Scheduled Project Boards are created if they do not exist.

### Project Board Task Synchronization

Scheduled Issues become Project Board Tasks.

Scheduled Issues and Project Board Task synchronization is resolved as follows;
- Each action runs against the Scheduled Project Board related to the directory 
- Issues which were created are created as Project Board Tasks
- Issues which were modified have their respective Project Board Task modified
- Issues which were closed have their respective Project Board Task removed

### Milestone Synchronization

Scheduled Labels become Scheduled Milestones.
- Any label in the format of `v\d+` becomes a Scheduled Milestone.

Scheduled Milestones and Milestone synchronization is resolved as follows;
- Scheduled Milestones are created if they do not exist.
