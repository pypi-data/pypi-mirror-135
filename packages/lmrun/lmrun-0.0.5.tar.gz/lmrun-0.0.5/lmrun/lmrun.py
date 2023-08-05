import fire
import json
import logicmonitor_sdk
import sys
import random

from logicmonitor_sdk import LMApi
from pathlib import Path


def connect_to_lm(creds):
    configuration = logicmonitor_sdk.Configuration()
    configuration.company = creds.get('company')
    configuration.access_id = creds.get('access_id')
    configuration.access_key = creds.get('access_key')

    api_instance = logicmonitor_sdk.LMApi(
        logicmonitor_sdk.ApiClient(configuration))
    return api_instance


def submit_script(path: Path, collector_id: int, api_instance: LMApi):
    if path.suffix == ".groovy":
        command = "groovy"
    elif path.suffix == ".ps1":
        command = "posh"
    else:
        print("Input script must be .groovy or .ps1")
        sys.exit(1)

    try:
        with open(path, 'r', encoding="utf-8-sig") as f:  # utf-8-sig handles with and w/o BOM
            script = f.read().strip()
    except FileNotFoundError:
        print(f"Error: {path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error while importing {path}: {e}")

    body = {"cmdline": f"!{command} \n {script}"}
    thread = api_instance.execute_debug_command(
        async_req=True,
        body=body,
        collector_id=collector_id
    )
    result = thread.get()

    return result.session_id


def get_script_result(session_id: str, collector_id: int, api_instance: LMApi):
    response = api_instance.get_debug_command_result(
        id=session_id, collector_id=collector_id)

    return response.output


def get_config_file_path():
    home = Path.home()
    return home.joinpath(".lmrun", "config.json")


def get_login_credentials():
    path = get_config_file_path()
    try:
        with open(path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("Please login first by running 'lmrun login'")
        sys.exit(1)
    except Exception:
        print("An error occured while getting credential file from local storage.")
        sys.exit(1)
    creds = json.loads(content)
    return creds


def get_random_collector(api_instance: LMApi):
    collectors = api_instance.get_collector_list().items
    return random.choice(collectors)


def command_login(company: str = None, access_id: str = None, access_key: str = None):
    if company == None:
        company = input(
            "Please enter your LogicMonitor company name: ").strip()
    if access_id == None:
        access_id = input("Please enter the API access id: ").strip()
    if access_key == None:
        access_key = input("Please enter the API access key: ").strip()

    config_file = get_config_file_path()
    file_contents = {
        "company": company,
        "access_id": access_id,
        "access_key": access_key
    }
    parent_dir = config_file.parent
    parent_dir.mkdir(parents=True, exist_ok=True)
    with config_file.open(mode="w") as f:
        f.write(json.dumps(file_contents, indent=1))


def command_logout():
    path = get_config_file_path()
    path.unlink()


def command_run(path: str, collector_id: int = None):
    creds = get_login_credentials()
    api = connect_to_lm(creds)
    if collector_id == None:
        collector_id = get_random_collector(api).id
    session_id = submit_script(Path(path), collector_id, api)
    result = get_script_result(session_id, collector_id, api)
    print(result)


def main():
    fire.Fire({
        "login": command_login,
        "execute": command_run,
        "exe": command_run,
        "logout": command_logout
    })


if __name__ == "__main__":
    main()
