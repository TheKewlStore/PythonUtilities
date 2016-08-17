# coding=utf-8
""" Convenience wrappers for SchedulingJobs using pyqt QTimers.

Author: Ian Davis
"""

from datetime import datetime

from Pyqt4.QtCore import QTimer

SECOND = 1000
MINUTE = 60 * SECOND


class ScheduledJob(object):
    """ Data holder for a job scheduled to run in the future.

    :param name: The name of the job.
    :param data: Any data pertaining to the job.
    :param time: The time the job should start.
    :param day: The day the job is scheduled for.
    :param frequency: The frequency the job should repeat.
    """
    DAILY = 1
    WEEKLY = 2

    def __init__(self, name, data, time, day=None, frequency=None):
        self.name = name
        self.data = data
        self.time = datetime.strptime(time, '%H:%M')
        self.day = day.lower()
        self.frequency = frequency

    def ready(self):
        """ Method to determine whether or not the job should be executed now.

        :return: True or False to determine if the job should be executed now.
        """
        current_date = datetime.now()
        current_day = current_date.strftime('%A').lower()

        if self.day and not current_day == self.day:
            return False
        elif not current_date.hour == self.time.hour:
            return False
        elif not current_date.minute == self.time.minute:
            return False

        return True


class Scheduler(object):
    """ Manage a queue of scheduled jobs, and execute them at the proper time.
    """

    def __init__(self):
        self.jobs = {}
        self.schedule_checker = QTimer()
        self.schedule_checker.setInterval(MINUTE)

        self._connect_slots()

        self.schedule_checker.start()

    def _connect_slots(self):
        """ Connect PyQt Signals to event handler slots.
        """
        self.schedule_checker.timeout.connect(self.process_jobs)

    def add_job(self, name, data, time, day=None, frequency=None):
        """ Add a new ScheduledJob to the queue.

            :param name: The name of the job. 
            :param data: Any data pertaining to the job.
            :param time: The time the job should execute.
            :param day: The day of the week the job should execute.
            :param frequency: The frequency the job should execute.
        """
        self.jobs[name] = ScheduledJob(name, data, time, day=day, frequency=frequency)

    def start_job(self, name, job):
        """ Handle invoking the necessary handlers to execute a job that is ready to run.

        :param name: The name of the job to start.
        :param job: The ScheduledJob instance.
        """
        pass

    def process_jobs(self):
        """ Check all the jobs in the queue for any that are ready to execute.
        """
        for name, job in self.jobs.iteritems():
            if job.ready():
                self.start_job(name, job)


class UpdateScheduler(Scheduler):
    """ Manage a queue of scheduled update jobs.

        :param update_queue: The queue to add our jobs too.
    """

    def __init__(self, update_queue):
        self.update_queue = update_queue
        super(UpdateScheduler, self).__init__()

    def start_job(self, ip_address, job):
        """ Start a new scheduled job through the update_queue.

            :param ip_address: The address that will be updated when the job runs.
            :param job: The ScheduledJob instance to start.
        """
        self.update_queue.queue(ip_address, **job.data)
        self.update_queue.start_update(ip_address)
