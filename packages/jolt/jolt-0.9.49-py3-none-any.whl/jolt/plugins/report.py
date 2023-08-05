from contextlib import contextmanager

from jolt.hooks import TaskHook, TaskHookFactory
from jolt.manifest import JoltManifest


class ReportHooks(TaskHook):
    def __init__(self):
        self.manifest = JoltManifest()

    def finalize_report(self, report, task, result):
        report.name = task.qualified_name
        report.duration = str(task.duration_running.seconds)
        report.goal = str(task.is_goal()).lower()
        report.identity = task.identity
        report.result = result
        if hasattr(task, "logstash"):
            report.logstash = task.logstash
        self.manifest.append(report)

    @contextmanager
    def task_run(self, task):
        try:
            yield
        except Exception as e:
            with task.task.report() as report:
                if not report.errors:
                    report.add_exception(e)
                self.finalize_report(report.manifest, task, "FAILED")
            raise e
        else:
            with task.task.report() as report:
                self.finalize_report(report.manifest, task, "SUCCESS")

    def write(self, filename):
        self.manifest.write(filename)

    @contextmanager
    def update(self):
        yield self.manifest


_report_hooks = ReportHooks()


def update():
    return _report_hooks.update()


def write(filename):
    return _report_hooks.write(filename)


@TaskHookFactory.register_with_prio(-10)
class ReportFactory(TaskHookFactory):
    def create(self, env):
        return _report_hooks
