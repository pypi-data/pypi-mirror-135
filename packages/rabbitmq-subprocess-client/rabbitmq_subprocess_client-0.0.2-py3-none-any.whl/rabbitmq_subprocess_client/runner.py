import logging
import time

LOGGER = logging.getLogger(__name__)


class Runner:
    """This is an example consumer that will reconnect if the nested
    ExampleConsumer indicates that a reconnect is necessary.

    """

    def __init__(
        self,
        queue_name,
        consumer_class,
        host="127.0.0.1",
        port="5672",
        user="guest",
        password="guest",
        timeout=None,
    ):
        self._reconnect_delay = 0
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout
        self.consumer_class = consumer_class
        self._consumer = self.consumer_class(
            self.queue_name, self.host, self.port, self.user, self.password, timeout
        )

    def run(self):
        while True:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break
            except ConnectionError:
                pass
            self._maybe_reconnect()

    def stop(self):
        self._consumer.stop()

    def _maybe_reconnect(self):
        if self._consumer.should_reconnect:
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            LOGGER.info("Reconnecting after %d seconds", reconnect_delay)
            time.sleep(reconnect_delay)
            self._consumer = self.consumer_class(
                self.queue_name, self.host, self.port, self.user, self.password, self.timeout
            )

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 5
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay
