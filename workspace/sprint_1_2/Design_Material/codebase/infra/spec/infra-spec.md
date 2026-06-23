# Infrastructure Specification

## Purpose
Provides platform-level infrastructure services including network routing, high availability, reverse proxy, and foundational resource management to ensure secure, reliable, and observable operation of the VKIST MSK system.

## Owner
Platform Engineering Team

## Boundary
- NGINX reverse proxy (TLS termination, request routing, rate limiting)
- Keepalived for VRRP-based high availability and failover
- Shared PostgreSQL and Redis instances (coordinated with Data room for provisioning)
- System-level monitoring, logging, and alerting foundations
- Network segmentation, firewall rules, and VPN/gateway configuration
- Infrastructure-as-code (Terraform) for provisioning and lifecycle management

## Internal Design
- NGINX configured as ingress controller with SSL/TLS termination, path-based routing to backend services, and WebSocket support for real-time features.
- Keepalived deployed in active-passive mode across cluster nodes, assigning a virtual IP (VIP) for seamless failover.
- PostgreSQL and Redis instances are provisioned and managed via Terraform; connection details are exposed as environment variables to consuming rooms.
- Foundational logging: structured JSON logs shipped to centralized observability stack (outside scope of this spec).
- Security: network policies restrict inter-room communication to declared interfaces; NGINX enforces authentication headers and rate limits.
- Observability: exposes Prometheus metrics endpoints; health checks for liveness and readiness.

## Interface Contract
See `infra/spec/interface-contract.md`.

## Consumers
- All rooms (frontend, backend, ml, data, knowledge) consume networking and availability guarantees.
- Backend and ML rooms consume reverse proxy for external API exposure.
- Data room consumes shared storage provisioning (Postgres, Redis) for stateful services.

## Breaking-change Policy
See `infra/spec/interface-contract.md`.

## References
- NFR-2 (System Availability ≥99.9% Monthly)
- NFR-8 (Network Latency ≤50ms Inter-Region)
- NFR-12 (Infrastructure as Code & Immutable Deployments)
- SOLUTION_ARCHITECTURE_SPEC.md (Sections 3.1-3.4)
- DATA_ENGINEERING_SPEC.md (Section 2 for storage provisioning)
