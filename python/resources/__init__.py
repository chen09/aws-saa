from flask_restful import fields

auditData_fields = {
    'requestHost': fields.String,
    'serverId': fields.String,
    'release': fields.String,
    'processTime': fields.Float,
    'timestamp': fields.String,
}

response_base_fields = {
    'auditData': fields.Nested(auditData_fields),
    'status': fields.Integer,
    'message': fields.String,
}
