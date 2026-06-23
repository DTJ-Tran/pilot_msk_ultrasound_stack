# Infrastructure Interface Contract

## Purpose
Provides platform-level infrastructure services including network routing, high availability, reverse proxy, and foundational resource management to ensure secure, reliable, and observable operation of the VKIST MSK system.

## Owner
Platform Engineering Team

## Provides
- network routing and security (NGINX reverse proxy with TLS termination, request routing, rate limiting, WAF)
- high availability and failover (Keepalived VRRP, virtual IP, health checks)
- foundational resource provisioning (PostgreSQL and Redis connection details via environment variables)
- infrastructure observability (Prometheus metrics endpoints, health check endpoints)
- foundational logging and monitoring (structured logs, alerting foundations)

## Consumes
- (none) – Infra room provides foundational services; it does not consume other rooms' interfaces for its core purpose.
  Note: Infra relies on underlying cloud/provider services (VMs, networking, storage) which are outside the scope of this interface contract.

## Consumers
- frontend: consumes network routing and availability for accessing the application.
- backend: consumes reverse proxy for external API exposure, HA for service continuity.
- ml: consumes reverse proxy for model serving endpoints (Triton), HA for inference reliability.
- data: consumes foundational resource provisioning (Postgres, Redis) for stateful services; consumes HA for storage durability.
- knowledge: consumes reverse proxy for external access to knowledge services (if exposed), HA for service durability.

## Not Directly Consumable
- internal NGINX configuration details (upstreams, SSL certificates)
- Keepalived VRRP configuration and scripts
- Terraform state and provider specifics
- underlying VM/hardware details

## Breaking-change Policy
- Changes to provided network endpoints (e.g., port, path prefixes) require version bump and backward compatibility period of one release.
- Deprecation of any provided interface will be communicated with at least one release notice.
- Resource provisioning interface (environment variable names) is considered stable; changes will be backward compatible where possible.

## References
- NFR-2 (System Availability ≥99.9% Monthly)
- NFR-8 (Network Latency ≤50ms Inter-Region)
- NFR-12 (Infrastructure as Code & Immutable Deployments)
- SOLUTION_ARCHITECTURE_SPEC.md (Sections 3.1-3.4)
- DATA_ENGINEERING_SPEC.md (Section 2 for storage provisioning)
