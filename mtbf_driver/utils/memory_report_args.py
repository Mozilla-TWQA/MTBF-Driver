import argparse
## this is for faking out an argument set for memory report


def memory_report_args(
        minimize=False,
        leave_on_device=False,
        no_auto_open=False,
        keep_report=False,
        gc_log=True,
        abbrev_gc_log=False):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--minimize',
        '-m',
        dest='minimize_memory_usage',
        action='store_true',
        default=minimize)
    parser.add_argument(
        '--directory',
        '-d',
        dest='output_directory',
        action='store',
        metavar='DIR')

    parser.add_argument(
        '--leave-on-device',
        '-l',
        dest='leave_on_device',
        action='store_true',
        default=leave_on_device)

    parser.add_argument(
        '--no-auto-open',
        '-o',
        dest='open_in_firefox',
        action='store_false',
        default=no_auto_open)
    parser.add_argument(
        '--keep-individual-reports',
        dest='keep_individual_reports',
        action='store_true',
        default=keep_report)

    gc_log_group = parser.add_mutually_exclusive_group()

    gc_log_group.add_argument(
        '--no-gc-cc-log',
        dest='get_gc_cc_logs',
        action='store_false',
        default=gc_log)

    gc_log_group.add_argument(
        '--abbreviated-gc-cc-log',
        dest='abbreviated_gc_cc_log',
        action='store_true',
        default=abbrev_gc_log)

    parser.add_argument('--no-dmd', action='store_true', default=False)

    args, unknown = parser.parse_known_args()
    return args
