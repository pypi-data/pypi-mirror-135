from traitlets.config import Configurable, Unicode


class ClusterInfrastructure(Configurable):
    """
    Manage required infrastructure at a target cluster
    """

    kubernetes_context = Unicode(
        "",
        help="""
        Kubernetes context to use for connecting to the kubernetes cluster.
        """,
        config=True,
    )

    namespace = Unicode(
        "jupyterhub-mcks-infra",
        help="""
        Namespace to put our infra in at the target cluster.

        Will be created if it does not exist
        """,
        config=True,
    )

    def deploy(self):
        cmd = ["helm", "upgrade", "--install"]
