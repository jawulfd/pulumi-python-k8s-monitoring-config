import pulumi
import pulumi_kubernetes as kubernetes

config = pulumi.Config()
monitoring_namespace = config.get("k8sNamespace", "monitoring")

monitoring_version = config.get("monitoringVersion", "kube-prometheus-stack-66.3.0")

monitoring_ns = kubernetes.core.v1.Namespace(
    "monitoringns",
    metadata=kubernetes.meta.v1.ObjectMetaArgs(
        name=monitoring_namespace,
    )
)

monitoring_release = kubernetes.helm.v4.Chart(
    "monitoring",
    chart=f"https://github.com/prometheus-community/helm-charts/releases/download/{monitoring_version}/{monitoring_version}.tgz",
    namespace=monitoring_ns.metadata.name,
    values={
        "prometheusOperator": {
            "tls": {
                "enabled": False,
            },
            "admissionWebhooks": {
                "enabled": False,
            }
        },
    }
)

monitoring_ingress = kubernetes.yaml.v2.ConfigGroup(
    "monitoring_ingress",
    files=["resources/monitoring/ingress-*.yaml"],
    opts=pulumi.ResourceOptions(depends_on=monitoring_release)
)
