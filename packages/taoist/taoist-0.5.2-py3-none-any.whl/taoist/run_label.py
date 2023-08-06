"""run_label.py"""
from argparse import ArgumentParser
from tabulate import tabulate
from todoist_api_python.api_async import TodoistAPIAsync
from taoist.read_project_dict import read_project_dict
from taoist.read_label_dict import read_label_dict

async def run_label(args: ArgumentParser) -> None:
    """
    Run the label command
    """

    # Read config and project list
    config, project_dict = await read_project_dict()

    # Read label list into dictionary
    label_dict = await read_label_dict(config)

    # Process subcommand
    if args.subcommand == "list":
        table_header = ["id", "name"]
        label_list = []
        for key, label in label_dict.items():
            row = [key, label.name]
            label_list.append(row)
        print(tabulate(label_list, headers=table_header))
    elif args.subcommand == "create":
        api = TodoistAPIAsync(config['Default']['token'])
        try:
            label = await api.add_label(name=args.label_name)
        except Exception as error:
            raise error
    elif args.subcommand == "delete":
        api = TodoistAPIAsync(config['Default']['token'])
        try:
            is_success = await api.delete_label(label_id=args.label_id)
            if is_success:
                print(f"Deleted project {label_dict[args.label_id].name}")
        except Exception as error:
            raise error 