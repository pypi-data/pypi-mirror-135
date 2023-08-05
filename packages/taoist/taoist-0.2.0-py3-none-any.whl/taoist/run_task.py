"""run_task.py"""
import json
from argparse import ArgumentParser
from taoist.read_project_dict import read_project_dict
from taoist.read_label_dict import read_label_dict
from tabulate import tabulate
from todoist_api_python.api import TodoistAPI

def run_task(args: ArgumentParser) -> None:
    """
    Run the task command
    """

    # Read config and project list
    config, project_dict = read_project_dict()

    label_dict = read_label_dict(config)

    # Initialize Todoist API
    api = TodoistAPI(config['Default']['token'])

    # Get tasks
    try:
        tasks = api.get_tasks()
    except Exception as error:
        print(error)

    # Process subcommand
    if args.subcommand == "list":
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
            row = [task.id, task.content, project_dict[task.project_id].name, status, task.due.date, label_string]
            task_list.append(row)
        task_list.sort(key=lambda x: x[4])
        print(tabulate(task_list, headers=table_header))
    elif args.subcommand == "delete":
        try:
            is_success = api.delete_task(task_id=args.task_id)
            if is_success:
                print(f"Task {args.task_id} deleted")
        except Exception as error:
            print(error)
    elif args.subcommand == "done":
        try:
            is_success = api.close_task(task_id=args.task_id)
            if is_success:
                print(f"Task {args.task_id} marked as done")
        except Exception as error:
            print(error)
    elif args.subcommand == "view":
        try:
            task = api.get_task(task_id=args.task_id)
            print(json.dumps(task.to_dict(), indent=2))
        except Exception as error:
            print(error)