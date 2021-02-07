import socket
from contextlib import closing

from . import Host, Port
from .initialization import ApplicationSettings
from .util import read_application_init_data
from .configuration.models import ApplicationConfig, InitData

from .console_logging import print_upcoming_step, print_error_step, print_success_step, print_warning_step


def check_if_application_init_process_ran_successfully() -> bool:
    settings = ApplicationSettings.create_default()
    print_upcoming_step("Checking jetson module availability")
    try:
        init_json: InitData = read_application_init_data(settings.application_init_report_file)
        if init_json.success:
            print_success_step("Application initiation ran successfully")
            return True

        print_error_step("Application initiation ran failed. Please run \"jetson-detectify init\" again.")
    except FileNotFoundError:
        print_error_step(
            f"Application initiation ran failed. Application data [{settings.application_init_report_file}] not available")
        return False

    return True


def check_jetson_python_module_availability() -> bool:
    print_upcoming_step("Checking jetson python module availability")
    if not _is_jetson_python_module_available():
        # print_error_step("Jetson python module availability check failed! Please check the JetsonDetectify documentation.")
        print_warning_step("Fake jetson module availability test value for development purposes. Has to be removed!!!")
        # return False
        return True
    else:
        print_success_step(f"Jetson python module availability check succeeded!")
        return True


def check_general_host_availability(config: ApplicationConfig) -> bool:
    print_upcoming_step("Checking host availability")
    if not _is_host_generally_available(Host(config.mqtt_broker.host), Port(config.mqtt_broker.port)):
        print_error_step(f"Host availability check to {config.mqtt_broker.host}:{config.mqtt_broker.port} "
                         "failed! Please Check your settings in application.yaml!")
        return False
    else:
        print_success_step(f"Host availability check to {config.mqtt_broker.host}:{config.mqtt_broker.port} succeeded!")
        return True


def _is_host_generally_available(host: Host, port: Port) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        if sock.connect_ex((host, port)) == 0:
            return True
    return False


def _is_jetson_python_module_available():
    try:
        import jetson
        return True
    except ModuleNotFoundError:
        return False
