"""run_task.py"""
from argparse import ArgumentParser
from tabulate import tabulate
from todoist_api_python.api_async import TodoistAPIAsync
from taoist.read_project_dict import read_project_dict
from taoist.read_label_dict import read_label_dict
from taoist.parent_project import parent_project

async def run_task(args: ArgumentParser) -> None:
    """
    Run the task command
    """

    # Read config and project list
    config, project_dict = await read_project_dict()

    # Read label list into dictionary
    label_dict = await read_label_dict(config)

    # Initialize Todoist API
    api = TodoistAPIAsync(config['Default']['token'])

    # Process subcommand
    if args.subcommand == "list":
        # Get all tasks
        try:
            tasks = await api.get_tasks()
        except Exception as error:
            print(error)
        table_header = ["id", "content", "project", "status", "due", "labels"]
        task_list = []
        for task in tasks:
            status = "Open"
            if task.completed:
                status = "Done"
            label_list = []
            for lab in task.label_ids:
                label_list.append(label_dict[lab].name)
            label_string = ','.join(label_list)
            if task.due:
                due_date = task.due.date
            else:
                due_date = ""
            project_path_string = parent_project(task.project_id, project_dict)
            row = [task.id, task.content, project_path_string, status, due_date, label_string]
            task_list.append(row)
        task_list.sort(key=lambda x: x[4])
        print(tabulate(task_list, headers=table_header))
    elif args.subcommand == "delete":
        try:
            is_success = await api.delete_task(task_id=args.task_id)
        except Exception as error:
            print(error)
        if is_success:
            print(f"Task {args.task_id} deleted")
    elif args.subcommand == "done":
        try:
            is_success = await api.close_task(task_id=args.task_id)
        except Exception as error:
            print(error)
        if is_success:
            print(f"Task {args.task_id} marked as done")
    elif args.subcommand == "view":
        view_list = []
        try:
            task = await api.get_task(task_id=args.task_id)
        except Exception as error:
            print(error)
        task_dict = task.to_dict()
        view_list.append(["Name", task_dict['content']])
        project_path_string = parent_project(task.project_id, project_dict)
        view_list.append(["Project", project_path_string])
        due_dict = task_dict['due']
        if due_dict:
            view_list.append(["Due", due_dict['date']])
            view_list.append(["Recurring", due_dict['recurring']])
        view_list.append(["Priority", task_dict['priority']])
        label_list = []
        for lab in task_dict['label_ids']:
            label_list.append(label_dict[lab].name)
        if len(label_list) > 0:
            label_string = ','.join(label_list)
            view_list.append(["Labels", label_string])
        print(tabulate(view_list))
    elif args.subcommand == "label":
        try:
            task = await api.get_task(task_id=args.task_id)
        except Exception as error:
            print(error)
        new_list = task.label_ids
        new_list.append(args.label_id)
        try:
            is_success = await api.update_task(task_id=args.task_id, label_ids=new_list)
        except Exception as error:
            print(error)
        if is_success:
            print("Label successfully added to task")
    elif args.subcommand == "create":
        try:
            task = await api.add_task(
                content=args.content,
                due_string=args.due,
                project_id=args.project,
                due_lang='en',
                priority=args.priority,
            )
            print(task)
        except Exception as error:
            print(error)