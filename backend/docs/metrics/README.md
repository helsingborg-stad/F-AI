# Metrics

Metrics are exposed in OpenMetrics format, from the `/api/metrics` endpoint,
which requires authentication with the `metrics.read` scope. The recommended
method is to provide an API key as a Bearer token in the `Authorization`
header.

## Example

The [prometheus.yml](./prometheus.yml) and [docker-compose.yml](./docker-compose.yml)
files showcases an example on how to set up Prometheus and Grafana to
visualize the metrics.

1. Generate an API key with `metrics.read` scope.

   Easiest is to use the OpenAPI UI (localhost:8000/docs) - make sure backend is up and running.
    1. Login with `POST /login/initiate` + `POST /login/confirm`
    2. Generate an API key with `POST /api/apikey`
    3. Add a new group with `POST /api/group` and call it "metrics"
    4. Add the API (revoke) key to the group with `POST /api/group/{group_id}/members`
    5. Set group scopes to include `"metrics.read"` using `PATCH /api/group/{group_id}/scopes`

2. Edit `prometheus.yml` and enter the API key with `metrics.read` scope in the `credentials` variable.
3. Run `docker-compose up -d`
4. Open Grafana (http://localhost:3000) and login with `admin` / `admin` and navigate to the sample dashboard.
