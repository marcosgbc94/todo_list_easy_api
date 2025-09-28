
from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider



def setup_otel_providers():
    """
    Configura los proveedores de trazas y métricas.
    No depende de la app de FastAPI y se puede llamar de forma segura al inicio.
    """
    resource = Resource(attributes={"service.name": "todolist-api"})

    # Configuración de Trazas
    tracer_provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
    processor = SimpleSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)

    # Configuración de Métricas
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

def instrument_app(app: FastAPI):
    """
    Aplica las instrumentaciones automáticas a la instancia de la app.
    """
    SQLAlchemyInstrumentor().instrument(track_db_statement=True)
    AsyncPGInstrumentor().instrument()
    FastAPIInstrumentor.instrument_app(app)