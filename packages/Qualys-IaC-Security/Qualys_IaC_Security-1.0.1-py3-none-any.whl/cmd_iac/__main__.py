import click, requests, json, re, time, copy
import os, shutil, tempfile
import zipfile, py7zr, tarfile, gzinfo
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
import yaml
from getpass import getpass
from yaml.loader import SafeLoader

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
API_getScanList = "/cloudview-api/rest/v1/iac/getScanList"
API_getScanResult = "/cloudview-api/rest/v1/iac/scanResult"
API_Launch_Scan = "/cloudview-api/rest/v1/iac/scan"
ZIP_FILE_NAME = ".zip"
VERSION = "1.0.1"
BLACKLIST_FROM_ZIPPING = [".*[.]zip$|.*[.]ZIP$", "^[.].*", ".*[.]hcl$", ".*[.]binary$", ".*[.]jpg$", ".*[.]exe$",
                          ".*[.]7z$", ".*[.]gz$", ".*[.]tar$"]
BLACKLIST_FOLDER_FROM_ZIPPING = ["^[.].*"]
WHITELIST_FOR_ZIPPING = [".*[.]tf$", ".*[.]template$", ".*[.]json$", ".*[.]yaml$", ".*[.]yml$"]
CONFIG_FILE_NAME = ".qiac.yaml"
HOME_DIR = os.path.expanduser('~') + os.sep
OUTPUT_FILE_NAME = "scan_response"

Platform_Details = {"_": "https://qualysguard.qualys.com",
                    "2": "https://qualysguard.qg2.apps.qualys.com",
                    "3": "https://qualysguard.qg3.apps.qualys.com",
                    "-": "https://qualysguard.qualys.eu",
                    "5": "https://qualysguard.qg2.apps.qualys.eu",
                    "!": "https://qualysguard.qg2.apps.qualys.eu",
                    "8": "https://qualysguard.qg1.apps.qualys.in",
                    "9": "https://qualysguard.qg1.apps.qualys.ca",
                    "7": "https://qualysguard.qg1.apps.qualys.ae",
                    "#": "https://qualysguard.qg1.apps.qualys.co.uk",
                    "4": "https://qualysguard.qg1.apps.qualys.com.au"}


# platform url option details
platform_url_details = {'help': 'Qualys Platform URL', "metavar": ''}
platform_url_short_name = "-a"
platform_url_full_name = "--platform_url"

# user option details
user_details = {'help': 'Qualys username', "metavar": ''}
user_short_name = "-u"
user_full_name = "--user"

# password option details
password_details = {'help': 'Qualys password', 'hide_input': True, "metavar": ''}
password_short_name = "-p"
password_full_name = "--password"

# path option details
path_details = {'help': 'Single template file or a directory', 'required': True, "metavar": '', 'multiple': True}
path_short_name = "-d"
path_full_name = "--path"

# formats option details
format_details = {'help': 'Show the output in specified format. [json]', "metavar": ''}
format_short_name = "-m"
format_full_name = "--format"

# filter option details
filter_details = {
    'help': 'Use regular expression to filter and include the input files. This option can be used only when directory path is specified in the path option. Example: ".*[.]tf$"',
    "metavar": ''}
filter_short_name = "-f"
filter_full_name = "--filter"

# quiet option details
quiet_details = {'help': 'Show only failed checks', 'is_flag': True}
quiet_short_name = "-q"
quiet_full_name = "--quiet"

# tag option details
tag_details = {
    'help': 'Add the tag (in JSON format) to the scan. e.g. [{\\"env\\":\\"linux\\"},{\\"test_key\\":\\"tags\\"}]',
    "metavar": ''}
tag_short_name = "-g"
tag_full_name = "--tag"

# proxy option details
proxy_details = {
    'help': 'Provide proxy in JSON format e.g. {\\"http\\":\\"http://<user>:<password>@<host>:<port>\\",\\"https\\":\\"https://<host>:<port>\\"}',
    "metavar": ''}
proxy_short_name = "-x"
proxy_full_name = "--proxy"

# scan_id option details
scan_id_details = {'help': 'Scan ID', "metavar": ''}
scan_id_short_name = "-i"
scan_id_full_name = "--scan_id"

# async option details
async_details = {'help': 'Triggers the IaC scan asynchronously', 'is_flag': True}
async_short_name = "-as"
async_full_name = "--async"

# scan_name option details
scan_name_details = {'help': 'Name of the scan', 'required': True, "metavar": ''}
scan_name_short_name = "-n"
scan_name_full_name = "--scan_name"

# config file option details
config_file_details = {'help': 'Path of the credentials config file set using "config" command', "metavar": ''}
config_file_short_name = "-c"
config_file_full_name = "--config_file"

# timeout option details
timeout_details = {"hidden": True, "default": 600}
timeout_full_name = "--timeout"

# interval option details
interval_details = {"hidden": True, "default": 30}
interval_full_name = "--interval"

# gitrepo name details
gitrepo_details = {"hidden": True}
gitrepo_full_name = "--gitrepo"

# branch name details
branch_details = {"hidden": True}
branch_full_name = "--branch"

# source details
source_details = {"hidden": True}
source_full_name = "--source"


# Save output option details
save_output_details = {'help': 'Save output in current directory', 'is_flag': True}
save_output_short_name = "-s"
save_output_full_name = "--save_output"


def check_option_values(params):
    options = list(globals().keys())
    options = list(filter(lambda x: x.endswith("_short_name") or x.endswith("_full_name"), options))

    for k, v in params.items():
        for o in options:
            if str(v) == globals().get(o):
                return k
    return False


def modify_usage_error(main_command):
    from click._compat import get_text_stderr
    from click.utils import echo
    def show(self, file=None):
        import sys
        if file is None:
            file = get_text_stderr()
        color = None
        if self.ctx is not None:
            color = self.ctx.color
            echo(self.ctx.get_usage() + '\n', file=file, color=color)
        param = False
        if self.ctx:
            param = check_option_values(self.ctx.params)
        if param:
            short_name = param + "_short_name"
            echo('Error: Option \'%s/--%s\' requires an argument.\n' % (globals().get(short_name), param), file=file,
                 color=color)
        else:
            echo('Error: %s\n' % self.format_message(), file=file, color=color)
        sys.argv = [sys.argv[0]]
        # Below function will add help text in error message
        # main_command()

    click.exceptions.UsageError.show = show


@click.group(options_metavar='[OPTIONS] |', context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(VERSION, '-v', '--version')
def run_cli(**params):
    pass


modify_usage_error(run_cli)


@run_cli.command('scan', short_help='Triggers/Launches the IaC scan.')
@click.option(config_file_full_name, config_file_short_name, **config_file_details)
@click.option(platform_url_full_name, platform_url_short_name, **platform_url_details)
@click.option(user_full_name, user_short_name, **user_details)
@click.option(password_full_name, password_short_name, **password_details)
@click.option(scan_name_full_name, scan_name_short_name, **scan_name_details)
@click.option(path_full_name, path_short_name, **path_details)
@click.option(async_full_name, async_short_name, **async_details)
@click.option(filter_full_name, filter_short_name, **filter_details)
@click.option(quiet_full_name, quiet_short_name, **quiet_details)
@click.option(tag_full_name, tag_short_name, **tag_details)
@click.option(format_full_name, format_short_name, **format_details)
@click.option(proxy_full_name, proxy_short_name, **proxy_details)
@click.option(timeout_full_name, **timeout_details)
@click.option(interval_full_name, **interval_details)
@click.option(gitrepo_full_name, **gitrepo_details)
@click.option(branch_full_name, **branch_details)
@click.option(source_full_name, **source_details)
@click.option(save_output_full_name, save_output_short_name, **save_output_details)
def scan(**params):
    validate_input(params)
    get_credentials(params)
    try:
        scan_id = launch_scan(params)
    except Exception as e:
        click.echo(click.style('Unable to launch the scan. ' + str(e), fg='red'))
        return
    if params.get("async") or not scan_id:
        return scan_id
    params["scan_id"] = scan_id
    click.echo()
    scan_status = ""
    start_time = time.time()
    polling_counter = 1
    while scan_status != "FINISHED":
        if int(time.time() - start_time) >= int(params.get("timeout")):
            click.echo(click.style('Polling timeout of ' + str(params.get("timeout")) + ' seconds reached.', fg='red'))
            return
        if polling_counter > 3:
            click.echo("Waiting for " + str(params.get("interval")) + " seconds to check the scan status")
            time.sleep(int(params.get("interval")))
        else:
            click.echo("Waiting for 10 seconds to check the scan status")
            time.sleep(10)
        polling_counter += 1
        try:
            scan_status = get_scan_status(params)
            if scan_status == None or scan_status == "ERROR":
                return
        except Exception as e:
            click.echo(click.style('Unable to get the scan status. ' + str(e), fg='red'))
            return

    click.echo()
    try:
        return get_scan_result(params)
    except Exception as e:
        click.echo(click.style('Unable to get the scan result. ' + str(e), fg='red'))
        return


@run_cli.command('listscans', short_help='List all the scans.')
@click.option(config_file_full_name, config_file_short_name, **config_file_details)
@click.option(platform_url_full_name, platform_url_short_name, **platform_url_details)
@click.option(user_full_name, user_short_name, **user_details)
@click.option(password_full_name, password_short_name, **password_details)
@click.option(scan_id_full_name, scan_id_short_name, **scan_id_details)
@click.option(format_full_name, format_short_name, **format_details)
@click.option(proxy_full_name, proxy_short_name, **proxy_details)
def listscans(**params):
    validate_input(params)
    get_credentials(params)
    try:
        return get_scan_list(params)
    except Exception as e:
        click.echo(click.style('Unable to get the list of scans. ' + str(e), fg='red'))
        return


@run_cli.command('getresult', short_help='Gets the scan result.')
@click.option(config_file_full_name, config_file_short_name, **config_file_details)
@click.option(platform_url_full_name, platform_url_short_name, **platform_url_details)
@click.option(user_full_name, user_short_name, **user_details)
@click.option(password_full_name, password_short_name, **password_details)
@click.option(scan_id_full_name, scan_id_short_name, **scan_id_details, required=True)
@click.option(format_full_name, format_short_name, **format_details)
@click.option(proxy_full_name, proxy_short_name, **proxy_details)
@click.option(save_output_full_name, save_output_short_name, **save_output_details)
def getresult(**params):
    validate_input(params)
    get_credentials(params)
    try:
        return get_scan_result(params)
    except Exception as e:
        click.echo(click.style('Unable to get the scan result. ' + str(e), fg='red'))
        return


@run_cli.command('config', short_help='Configure IaC CLI credentials.')
@click.option(platform_url_full_name, platform_url_short_name, **platform_url_details, required=True)
@click.option(user_full_name, user_short_name, **user_details, required=True)
@click.option(password_full_name, password_short_name, **password_details, required=True)
@click.option(config_file_full_name, config_file_short_name,
              help="File path to store the configuration", metavar='')
def configure(**params):
    validate_input(params)
    try:
        return configure_cli(params)
    except Exception as e:
        click.echo(click.style('Unable to configure the CLI. ' + str(e), fg='red'))
        return


def get_credentials(params):
    try:
        config_file_path = params.get("config_file")
        if params["platform_url"] and params["user"] and params["password"]:
            click.echo("Using credentials from command options")
            return params
        elif params["platform_url"] and params["user"]:
            params["password"] = getpass("Password: ")
            click.echo("Using credentials from command options")
            return params
        elif config_file_path:
            if os.path.exists(config_file_path):
                click.echo("Using credentials from configuration file: " + config_file_path)
            else:
                click.echo(click.style("Configuration file does not exist at: " + config_file_path, fg='red'))
                exit(0)
        elif os.path.exists(CONFIG_FILE_NAME):
            click.echo("Using configuration file with credentials from current directory")
            config_file_path = CONFIG_FILE_NAME
        elif os.path.exists(HOME_DIR + CONFIG_FILE_NAME):
            click.echo("Using configuration file with credentials from user's home directory")
            config_file_path = HOME_DIR + CONFIG_FILE_NAME
        else:
            click.echo(
                click.style("Credentials not found. Please check the configuration file or command line options", fg='red'))
            exit(0)
        with open(config_file_path) as f:
            data = yaml.load(f, Loader=SafeLoader)
    except Exception as e:
        click.echo(click.style('Failed to get credentials. ' + str(e), fg='red'))
        exit(0)

    params["platform_url"] = data.get("platform_url")
    params["user"] = data.get("user")
    params["password"] = data.get("password")
    return params


def validate_input(params):
    param = check_option_values(params)
    if param:
        raise click.MissingParameter(param)
    validation_messages = []

    # validation for interval option
    if params.get("interval"):
        if int(params.get("interval")) < 30:
            validation_messages.append("Interval: Interval should be greater than 30 seconds")

    # validation for platform URL
    if params.get("platform_url"):
        platform_list = Platform_Details.values()
        if params.get("platform_url") not in platform_list:
            validation_messages.append("Qualys Platform URL: Platform Server URL is not valid!")

    # Validation for tag option
    if params.get("tag"):
        if not get_json(params.get("tag")):
            validation_messages.append("Tag: Provide it in a valid JSON Array format.")

    # Validation for proxy option
    if params.get("proxy"):
        if not get_json(params.get("proxy")):
            validation_messages.append("Proxy: Provide it in a valid JSON format.")

    if validation_messages:
        click.echo(click.style("Input validation failed! ", fg='red'))
        for m in validation_messages:
            click.echo(click.style(m, fg='red'))
        exit(0)
    else:
        return True


def get_platform(params):
    if params.get("platform_url"):
        return params.get("platform_url")
    else:
        if Platform_Details.get(params.get("user")[5]):
            pod_url = Platform_Details.get(params.get("user")[5])
            click.echo("According to the username POD should be: " + pod_url)
            return pod_url
        else:
            url = input("Please provide the Qualys Platform URL: ")
            return url.strip()


def my_request(params, query_params, api, method='get', files=None, body_params=None, headers=None):
    credentials = (params.get("user"), params.get("password"))
    params["platform_url"] = get_platform(params)
    if params["platform_url"][-1] == "/":
        params["platform_url"] = params["platform_url"][:-1]
    proxyDict = None
    if params.get("proxy"):
        proxyDict = params.get("proxy")
        click.echo("Applying following proxy to the request: " + str(proxyDict))
        proxyDict = json.loads(proxyDict)
    try:
        response = requests.request(method=method, url=params.get("platform_url") + api, params=query_params,
                                    data=body_params, auth=credentials, files=files, proxies=proxyDict, headers=headers)
        if response.status_code != 201 and response.status_code != 200:
            click.echo(click.style("The API request failed : " + response.text, fg='red'))
            return None
        return response
    except Exception as e:
        click.echo(click.style("The API request failed : " + str(e), fg='red'))


def configure_cli(params):
    config_data = {"platform_url": params.get("platform_url"), "user": params.get("user"),
                   "password": params.get("password")}
    if params.get("config_file"):
        config_file_path = params.get("config_file")
    else:
        config_file_path = HOME_DIR + CONFIG_FILE_NAME
    if os.path.isdir(config_file_path):
        if not config_file_path.endswith(os.sep):
            config_file_path += os.sep
        config_file_path += CONFIG_FILE_NAME

    with open(config_file_path, 'w') as f:
        yaml.dump(config_data, f, sort_keys=False, default_flow_style=False)

    click.echo(click.style("Configuration file is created at: " + config_file_path, fg='green'))
    return config_file_path


def get_scan_status(params):
    click.echo("Fetching the scan status with scan ID: " + str(params.get("scan_id")))
    query_params = {"filter": "scanUuid:" + str(params.get("scan_id"))}
    response = my_request(params, query_params, API_getScanList)
    if (response and response.status_code == 200):
        result = json.loads(response.text)
        if len(result.get('content')) == 0:
            click.echo(click.style(
                'Unable to fetch the scan status as the scan Id "%s" is not found. Check the scan Id.' % str(
                    params.get("scan_id")), fg='red'))
            return None
        color = 'red'
        if result.get('content')[0].get("status") == "FINISHED":
            color = 'green'
        elif result.get('content')[0].get("status") == "PROCESSING" or result.get('content')[0].get(
                "status") == "SUBMITTED":
            color = 'yellow'
        else:
            color = 'red'
        click.echo(click.style('The scan status is: ' + str(result.get('content')[0].get("status")), fg=color))
        return result.get('content')[0].get("status")
    else:
        click.echo(click.style('Failed to fetch the scan status', fg='red'))
        return None


def get_scan_result(params):
    click.echo("Fetching the scan result with scan ID: " + str(params.get("scan_id")))
    query_params = {"scanUuid": str(params.get("scan_id"))}
    header = None
    if params.get("format") and params.get("format").lower() == "sarif":
        header = {"responseFormat": "sarif"}
    response = my_request(params, query_params, API_getScanResult, headers=header)
    if response and response.status_code == 200:
        result = json.loads(response.text)
        if result.get('status') and result.get('status') != "FINISHED":
            click.echo(click.style(
                'The scan result is not ready yet. The scan results are available only after the scan is completed/is in FINISHED state.',
                fg='red'))
            return None
        if result.get('result') != None and result.get('result') == []:
            click.echo(
                click.style('The scan is FINISHED, but the scan result is empty. Check the scan configuration file.',
                            fg='yellow'))
        if params.get("format"):
            if params.get("format").lower() == "json":
                if params.get("save_output"):
                    fp = open(OUTPUT_FILE_NAME + "_" + str(params.get("scan_id")) + ".json", "w")
                    json.dump(result, fp, indent=2)
                    fp.close()
                    os.chmod(OUTPUT_FILE_NAME + "_" + str(params.get("scan_id")) + ".json", 0o660)
                click.echo(
                    click.style('The scan result is successfully retrieved. JSON output is as follows: ',
                                fg='green'))
                click.echo(json.dumps(result, indent=2))
            # We can add outer output format here by adding elif
            elif params.get("format").lower() == "sarif":
                if params.get("save_output"):
                    fp = open(OUTPUT_FILE_NAME + "_" + str(params.get("scan_id")) + ".sarif", "w")
                    json.dump(result, fp, indent=2)
                    fp.close()
                    os.chmod(OUTPUT_FILE_NAME + "_" + str(params.get("scan_id")) + ".sarif", 0o660)
                click.echo(
                    click.style('The scan result is successfully retrieved. SARIF output is as follows: ',
                                fg='green'))
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo(
                    click.style(
                        'The output is in the default table format as the format you specified is not supported.',
                        fg='yellow'))
                show_result_in_table(result)
        else:
            show_result_in_table(result)
        return result
    else:
        click.echo(click.style('Failed to fetch the scan result', fg='red'))
        return None


def create_zip(path, include_files):
    zip_file_name = path + "_" + str(time.time()).replace(".", "_") + ZIP_FILE_NAME
    if os.path.exists(zip_file_name):
        click.echo("Discrepancy while creating a zip file as a file with same name exists: " + zip_file_name)
        click.echo("Removing the existing file to resolve discrepancy.")
        os.remove(zip_file_name)
    click.echo("Creating a zip file of the following files:")
    zipobj = zipfile.ZipFile(zip_file_name, 'w')
    rootlen = len(path) + 1
    trigger_scan = False
    for base, dirs, files in os.walk(path):
        pop_dir = []
        for d in dirs:
            if True in list(map(lambda ex: re.match(ex, d) is not None, BLACKLIST_FOLDER_FROM_ZIPPING)):
                pop_dir.append(d)
        for p in pop_dir:
            dirs.remove(p)
        for file in files:
            if True in list(map(lambda ex: re.match(ex, file) is not None, BLACKLIST_FROM_ZIPPING)):
                continue

            if True not in list(map(lambda ex: re.match(ex, file.lower()) is not None, WHITELIST_FOR_ZIPPING)):
                continue

            match = None
            try:
                match = re.match(include_files, file)
            except:
                click.echo(
                    click.style("The regular expression you provided is invalid. Provide a valid regular expression.",
                                fg='red'))
                return None
            if match:
                fn = os.path.join(base, file)
                click.echo(fn)
                zipobj.write(fn, fn[rootlen:])
                trigger_scan = True
    zipobj.close()
    os.chmod(zip_file_name, 0o660)
    return zip_file_name, trigger_scan


def get_json(data):
    try:
        json.loads(str(data))
        return data
    except ValueError as err:
        return False


def validate_white_list(listOfiles, file_format):
    path = "\n "
    for file in listOfiles:
        if file_format == "ZIP":
            is_dir = file.is_dir()
            f_name = file.filename
            if f_name.endswith("\\") or f_name.endswith("/"):
                f_name = f_name[:-1]
        elif file_format == "7Z":
            is_dir = file.is_directory
            f_name = file.filename
        else:
            is_dir = file.isdir()
            f_name = file.name
        filename = os.path.basename(f_name)
        if not is_dir:
            if True not in list(map(lambda ex: re.match(ex, filename.lower()) is not None, WHITELIST_FOR_ZIPPING)):
                path += f_name + ",\n "
        else:
            if True in list(map(lambda ex: re.match(ex, filename) is not None, BLACKLIST_FOLDER_FROM_ZIPPING)):
                path += f_name + ",\n "
    if path.endswith(",\n "):
        return path[:-3]
    else:
        return


def validate_input_file(file_path):
    click.echo("Validating file \"%s\"" % file_path)
    path = ""
    if file_path.lower().endswith(".zip"):
        with zipfile.ZipFile(file_path, 'r') as zipObj:
            listOfiles = zipObj.filelist
        path = validate_white_list(listOfiles, "ZIP")
    elif file_path.lower().endswith(".7z"):
        with py7zr.SevenZipFile(file_path, 'r') as zip_obj:
            listOfiles = zip_obj.list()
        path = validate_white_list(listOfiles, "7Z")
    elif file_path.lower().endswith(".tar") or file_path.lower().endswith(".tar.gz"):
        with tarfile.open(file_path) as tar_obj:
            listOfiles = tar_obj.getmembers()
        path = validate_white_list(listOfiles, "TAR")
    elif file_path.lower().endswith(".gz"):
        info = gzinfo.read_gz_info(file_path)
        return validate_input_file(info.fname)
    else:
        filename = os.path.basename(file_path)
        if True not in list(map(lambda ex: re.match(ex, filename.lower()) is not None, WHITELIST_FOR_ZIPPING)):
            path = file_path
    if path:
        click.echo(
            click.style("Unable to launch the scan. The following files/folders are not supported: " + path, fg='red'))
        return None
    click.echo("Validation completed successfully")
    return True


def clean_files(clean_file, file_path, temp_folder):
    if clean_file:
        click.echo("Cleaning the ZIP file: \"%s\"" % file_path)
        os.remove(file_path)
    if temp_folder:
        click.echo("Cleaning the temporary input folder : \"%s\"" % temp_folder)
        shutil.rmtree(temp_folder)
    return clean_file


def consolidate_input_path(input_paths):
    temp_folder_prefix = "qiac_input_dir_"
    temp_folder = tempfile.mkdtemp(prefix=temp_folder_prefix)
    copy_files = False
    for input_path in input_paths:
        if not os.path.exists(input_path):
            click.echo(
                click.style("The file/directory path you provided is invalid: " + input_path, fg='yellow'))
            continue
        if os.path.isfile(input_path):
            shutil.copy(input_path, temp_folder + os.sep)
            copy_files = True
        elif os.path.isdir(input_path):
            if input_path.endswith(os.sep):
                input_path = input_path[:-1]
            folder_name = input_path.replace(os.sep, "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-")
            if input_path == ".":
                folder_name = "-"
            elif input_path == "..":
                folder_name = "--"
            if folder_name.startswith("."):
                folder_name = "-" + folder_name[1:]
            try:
                shutil.copytree(input_path, temp_folder + os.sep + folder_name)
                copy_files = True
            except FileNotFoundError:
                click.echo(click.style("The file/directory path you provided is invalid: " + input_path, fg='yellow'))
        else:
            click.echo(click.style("Please provide File/Directory path: " + input_paths, fg='red'))
            continue
    # Cleaning temp folder if no files or directories are copied into a temp folder.
    if not copy_files:
        clean_files(False, "", temp_folder)
    return temp_folder

def launch_scan(params):
    file_path = None
    temp_folder = None
    clean_file = False
    trigger_scan = True
    if params.get("quiet"):
        click.echo("Quiet mode is enabled")
    if len(params.get("path")) == 1:
        params["path"] =  params.get("path")[0]
    else:
        params["path"] =  consolidate_input_path(params.get("path"))
        temp_folder = params["path"]
    if not os.path.exists(params.get("path")):
        click.echo(click.style("The file/directory path you provided is invalid. Provide a valid file/directory path.",
                               fg='red'))
        return None
    if os.path.isfile(params.get("path")):
        if params.get("filter"):
            click.echo(
                click.style("The given input path is already a file type. Ignoring the filter parameter!", fg='yellow'))
        file_path = params.get("path")
        if validate_input_file(file_path) is None:
            return None
    elif os.path.isdir(params.get("path")):
        if params.get("path").endswith(os.sep):
            params["path"] = params.get("path")[:-1]
        if params.get("filter"):
            file_path, trigger_scan = create_zip(params.get("path"), params.get("filter"))
            clean_file = True
        else:
            file_path, trigger_scan = create_zip(params.get("path"), ".*.")
            clean_file = True
    else:
        click.echo(click.style("Please provide File/Directory path", fg='red'))
        return None
    if file_path is None:
        return None
    body_params = {"showOnlyFailedControls": params.get("quiet"), "name": params.get("scan_name")}
    if params.get("gitrepo"):
        body_params.update({"gitrepo": params.get("gitrepo")})
    if params.get("branch"):
        body_params.update({"branch": params.get("branch")})
    if params.get("source"):
        body_params.update({"source": params.get("source")})

    if params.get("tag"):
        tag = params.get("tag")
        if tag:
            click.echo("Adding provided tag: " + str(tag))
            body_params["tags"] = tag
        else:
            clean_files(clean_file, file_path, temp_folder)
            return None
    ret = None
    if trigger_scan:
        if int(os.stat(file_path).st_size) >= 10485760:
            click.echo(click.style("File size too large, File name: " + file_path + ", File size: " + str(
                round(os.stat(file_path).st_size / 1024, 4)) + " KB", fg='red'))
            clean_files(clean_file, file_path, temp_folder)
            return None
        click.echo("Uploading the file \"%s\"" % file_path)
        fp = open(file_path, "rb")
        response = my_request(params, {}, API_Launch_Scan, method="post", files={"file": fp}, body_params=body_params)
        fp.close()
        if response and response.status_code == 200:
            result = json.loads(response.text)
            click.echo(click.style('Scan launched successfully. Scan ID: ' + str(result.get("scanUuid")), fg='green'))
            ret = result.get("scanUuid")
        else:
            click.echo(click.style('Failed to launch the scan', fg='red'))
    else:
        click.echo(
            click.style('Unable to launch the scan. No files match the specified filter criteria.', fg='red'))
    clean_files(clean_file, file_path, temp_folder)
    return ret


def format_column_names(column):
    column_names = []
    for c in column:
        if c == "checkId":
            column_names.append("Control Id")
        elif c == "checkName":
            column_names.append("Control Name")
        else:
            c_name = c[0].upper() + c[1:]
            i = 1
            while i != len(c_name):
                if c_name[i].isupper():
                    c_name = c_name[:i] + " " + c_name[i:]
                    i = i + 1
                i = i + 1
            column_names.append(c_name)
    return column_names


def show_table(column, rows):
    column = format_column_names(column)
    table = PrettyTable(column)
    table.align = 'l'
    for r in rows:
        table.add_row(r)
    click.echo(table)


def get_keys_values_check_list(result):
    checks_list = []
    if result.get("results").get("failedChecks"):
        checks_list += copy.deepcopy(result.get("results").get("failedChecks"))
    if result.get("results").get("passedChecks"):
        checks_list += copy.deepcopy(result.get("results").get("passedChecks"))
    check_rows = []
    checks_keys = ["checkId", "checkName", "criticality", "Result", "filePath", "resource"]

    criticality_high = []
    criticality_medium = []
    criticality_low = []
    for r in checks_list:
        checks_values = []
        checks_values.append(r.get(checks_keys[0]))
        checks_values.append(r.get(checks_keys[1]))

        criticality = r.get(checks_keys[2])
        if criticality == "HIGH":
            r["criticality"] = click.style("HIGH", fg='red')
        elif criticality == "MEDIUM":
            r["criticality"] = click.style("MEDIUM", fg='yellow')
        elif criticality == "LOW":
            r["criticality"] = click.style("LOW", fg='magenta')
        checks_values.append(criticality)

        if r.get("checkResult").get("result") == "FAILED":
            check_status = click.style("FAILED", fg='red')
        elif r.get("checkResult").get("result") == "PASSED":
            check_status = click.style("PASSED", fg='green')
        else:
            check_status = click.style("NULL", fg='red')
        checks_values.append(check_status)

        checks_values.append(r.get(checks_keys[4]))
        checks_values.append(r.get(checks_keys[5]))

        if criticality == "HIGH":
            criticality_high.append(checks_values)
        elif criticality == "MEDIUM":
            criticality_medium.append(checks_values)
        elif criticality == "LOW":
            criticality_low.append(checks_values)
        else:
            check_rows.append(checks_values)
    return checks_keys, criticality_high + criticality_medium + criticality_low + check_rows


def show_result_in_table(result):
    summary_keys = []
    summary_rows = []

    results = copy.deepcopy(result.get("result"))
    for result in results:
        summary_keys = []
        summary_values = []
        summary_keys.append("checkType")
        summary_values.append(result.get("checkType"))
        summary_keys = summary_keys + list(result.get("summary").keys())
        failed_stats_dict = result.get("summary").get("failedStats")
        dict_str = ""
        for i in failed_stats_dict:
            dict_str += i + "=" + str(failed_stats_dict.get(i)) + ", "
        result["summary"]["failedStats"] = dict_str[:-2]
        summary_values = summary_values + list(result.get("summary").values())
        summary_rows.append(summary_values)
    if summary_keys != []:
        click.echo('Result Summary')
        show_table(summary_keys, summary_rows)
    remediation_row_list = []
    remediation_value_dict = {}
    parsing_error_list = []
    for result in results:
        checks_key, checks_value = get_keys_values_check_list(result)
        if checks_value:
            click.echo('\n' + format_column_names([result.get("checkType")])[0] + " Checks")
            show_table(checks_key, checks_value)

        # For Remediation table
        if result.get("results").get("failedChecks"):
            failed_checks_list = copy.deepcopy(result.get("results").get("failedChecks"))
            for r in failed_checks_list:
                if r.get("remediation"):
                    remediation_value_dict[str(r.get("checkId")) + "::::" + str(r.get("remediation"))] = True

        # For parsing error table
        if result.get("results").get("parsingErrors"):
            parsing_errors = ""
            for p in result.get("results").get("parsingErrors"):
                parsing_errors += p + "\n"
            if parsing_errors != "":
                parsing_error_list.append([result.get("checkType"), parsing_errors[:-1]])

    for r in remediation_value_dict.keys():
        check_id, remediation = r.split("::::")
        remediation_row_list.append([check_id, remediation])

    if remediation_row_list:
        click.echo('\nRemediation')
        show_table(["checkId", "remediation"], remediation_row_list)

    if len(parsing_error_list) != 0:
        click.echo('\nParsing Errors')
        show_table(["checkType", "Location"], parsing_error_list)


def show_list_in_table(result):
    keys = []
    rows = []
    for r in result.get("content"):
        values = []
        tags_str = ""
        for t in r.get("tags"):
            t_value = list(t.values())
            tags_str += t_value[0] + ":" + t_value[1] + ",\n"
        if len(tags_str) > 0:
            r["tags"] = tags_str[:-2]
        else:
            r["tags"] = "-"
        status = ""
        if r.get("status") == "ERROR":
            status = click.style("ERROR", fg='red')
        elif r.get("status") == "FINISHED":
            status = click.style("FINISHED", fg='green')
        elif r.get("status") == "PROCESSING":
            status = click.style("PROCESSING", fg='yellow')
        elif r.get("status") == "SUBMITTED":
            status = click.style("SUBMITTED", fg='magenta')
        r["status"] = status
        keys = list(r.keys())
        value = list(r.values())

        # Putting scan name column at first position
        k = keys.pop(len(keys) - 1)
        keys.insert(0, k)
        v = value.pop(len(value) - 1)
        value.insert(0, v)
        values += value
        rows.append(values)
    click.echo('\nScan List')
    show_table(keys, rows)


def get_scan_list(params):
    click.echo("Fetching the scan list...")
    query_params = {}
    if params.get("scan_id"):
        query_params = {"filter": "scanUuid:" + str(params.get("scan_id"))}

    response = my_request(params, query_params, API_getScanList)
    if response and response.status_code == 200:
        result = json.loads(response.text)
        if params.get("format"):
            if params.get("format").lower() == "json":
                click.echo(click.style('The scan list is fetched successfully. The JSON output is: ', fg='green'))
                click.echo(json.dumps(result, indent=2))
            else:
                if not result.get("content"):
                    click.echo(click.style('Scan list is empty', fg='yellow'))
                    return result
                click.echo(
                    click.style('Provided output format is not supported. Ignoring format parameter!', fg='yellow'))
                show_list_in_table(result)
        else:
            if not result.get("content"):
                click.echo(click.style('Scan list is empty', fg='yellow'))
                return result
            show_list_in_table(result)
        return result
    else:
        click.echo(click.style('Failed to fetch the scan list', fg='red'))
        return None


def main():
    run_cli()


if __name__ == '__main__':
    main()
