from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.actions.slack.notifiers import (
    SendSlackMessageSpiderFinished,
)
from spidermon.contrib.monitors.mixins import StatsMonitorMixin

from .actions import CloseSpiderAction

# Monitors


@monitors.name("Item validation")
class ItemValidationMonitor(Monitor, StatsMonitorMixin):
    @monitors.name("No item validation errors")
    def test_no_item_validation_errors(self):
        validation_errors = getattr(
            self.stats, "spidermon/validation/fields/errors", 0
        )
        self.assertEqual(
            validation_errors,
            0,
            msg="Found validation errors in {} fields".format(
                validation_errors
            ),
        )


@monitors.name("Periodic item validation")
class PeriodicItemValidationMonitor(ItemValidationMonitor):
    pass


# Suites


class SpiderPeriodicMonitorSuite(MonitorSuite):
    monitors = [PeriodicItemValidationMonitor]
    monitors_failed_actions = [
        SendSlackMessageSpiderFinished,
        CloseSpiderAction,
    ]


class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [ItemValidationMonitor]

    monitors_failed_actions = [SendSlackMessageSpiderFinished]
