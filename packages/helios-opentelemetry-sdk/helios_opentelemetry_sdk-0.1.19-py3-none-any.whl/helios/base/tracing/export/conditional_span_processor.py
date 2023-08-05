from logging import getLogger
from typing import Optional, Callable

from opentelemetry.context.context import Context
from opentelemetry.sdk.trace import ReadableSpan, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from .utils import is_running_in_pytest


_LOG = getLogger(__name__)


class ConditionalSpanProcessorConfig(object):
    def __init__(self,
                 on_start_hook: Optional[Callable[[Span, Optional[Context]], None]] = None,
                 on_end_condition: Optional[Callable[[ReadableSpan], bool]] = False):

        self.on_start_hook = on_start_hook
        self.on_end_condition = on_end_condition


class ConditionalSpanProcessor(BatchSpanProcessor):
    def __init__(self, exporter: SpanExporter, config: Optional[ConditionalSpanProcessorConfig] = None):
        super().__init__(exporter)
        self.on_start_hook = config.on_start_hook if config else None
        self.on_end_condition = config.on_end_condition if config else None

    def on_start(self, span: Span, parent_context: Optional[Context] = None) -> None:
        super().on_start(span)
        if self.on_start_hook:
            try:
                self.on_start_hook(span, parent_context)
            except Exception as err:
                _LOG.error('ConditionalSpanProcessor: error running on_start_hook', err)

    def on_end(self, span: ReadableSpan) -> None:
        if not self.on_end_condition(span):
            # This isn't a test, so no need to export at all
            return

        super().on_end(span)
        if not is_running_in_pytest():
            self.force_flush()
