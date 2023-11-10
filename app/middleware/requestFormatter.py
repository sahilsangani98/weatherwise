from marshmallow import Schema, fields

class MetricsReportRequestSchema(Schema):
    """
    Schema definition for validating a metrics report request.

    Attributes:
    - metrics: A dictionary of metrics where keys represent metric names and values represent their values.
    - recorded_at: DateTime field representing the time of the report.
    """
    metrics = fields.Dict(
        required=True,
    )
    recorded_at = fields.DateTime(required=True, format="%Y-%m-%dT%H:%M:%SZ")
