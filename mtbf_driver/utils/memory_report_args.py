## this is for faking out an argument set for memory report


class memory_args(object):
    pass


def memory_report_args(
        output_directory="output",
        minimize_memory_usage=False,
        create_archive=True,
        leave_on_device=False,
        open_in_firefox=False,
        keep_individual_reports=False,
        abbreviated_gc_cc_log=False,
        get_gc_cc_logs=True,
        compress_gc_cc_logs=True,
        no_kgsl_logs=False,
        compress_dmd_logs=True):
    mem_args = memory_args()

    mem_args.output_directory = output_directory
    mem_args.minimize_memory_usage = minimize_memory_usage
    mem_args.create_archive = create_archive
    mem_args.leave_on_device = leave_on_device
    mem_args.open_in_firefox = open_in_firefox
    mem_args.keep_individual_reports = keep_individual_reports
    mem_args.abbreviated_gc_cc_log = abbreviated_gc_cc_log
    mem_args.get_gc_cc_logs = get_gc_cc_logs
    mem_args.compress_gc_cc_logs = compress_gc_cc_logs
    mem_args.no_kgsl_logs = no_kgsl_logs
    mem_args.compress_dmd_logs = compress_dmd_logs
    return mem_args
