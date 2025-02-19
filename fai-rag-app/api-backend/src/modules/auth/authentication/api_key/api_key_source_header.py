from fastapi.security import APIKeyHeader

api_key_source_header = APIKeyHeader(
    name='X-Api-Key',
    description='API Key. Can be created/revoked by an administrator.',
    auto_error=False
)
