
service_relation = {
    "argocd": {
        "service": "-argocd-instance-server",
        "secret": "argocd-initial-admin-secret",
        "secret-password": "password",
        "user": "admin",
        "password": "",
        "monitor": "http://172.30.1.12:32719/d/ArgoCD/argocd?orgId=1&var-namespace={}",
    },
    "dbgate": {
        "service": "-dbgate-instance-dbgate",
        "secret-password": "",
        "secret": "",
        "user": "postgres",
        "password": "Def@u1tpwd",
        "monitor": "-",
    },
    "gitlab": {
        "service": "-gitlab-instance-webservice-default",
        "secret": "-gitlab-instance-gitlab-initial-root-password",
        "secret-password": "password",
        "user": "root",
        "password": "",
        "monitor": "http://172.30.1.12:32719/d/gitlab/gitlab?orgId=1&var-namespace={}",
    },
    "harbor": {
        "service": "-harbor-instance-portal",
        "secret": "",
        "secret-password": "",
        "user": "admin",
        "password": "Harbor12345",
        "monitor": "http://172.30.1.12:32719/d/Harbor/harbor_dashboard?orgId=1&var-namespace={}",
    },
    "jenkins": {
        "service": "-jenkins-instance",
        "secret-password": "",
        "secret": "",
        "user": "admin",
        "password": "Def@u1tpwd",
        "monitor": "http://172.30.1.12:32719/d/jenkins/jenkins?orgId=1&var-namespace={}",
    },
    "postgresql": {
        "service": "-postgresql-instance",
        "secret": "-postgresql-instance",
        "secret-password": "postgres-password",
        "user": "postgres",
        "password": "",
        "monitor": "http://172.30.1.12:32719/d/PostgreSQL/postgresql-database?orgId=1&var-namespace={}",
    },
    "sonarqube": {
        "service": "-sonarqube-instance-sonarqube",
        "secret": "",
        "secret-password": "",
        "user": "admin",
        "password": "Def@u1tpwd",
        "monitor": "http://172.30.1.12:32719/d/sonarqube/sonarqube?orgId=1&var-namespace={}",
    },
    "grafana": {
        "service": "-grafana-instance",
        "secret": "",
        "secret-password": "",
        "user": "admin",
        "password": "Def@u1tpwd",
        "monitor": "-",
    },
    "minio": {
        "service": "minio-service",
        "secret": "",
        "secret-password": "",
        "user": "admin",
        "password": "Def@u1tpwd",
        "monitor": "http://172.30.1.12:32719/d/minio/minio?orgId=1&var-namespace={}",
    }
}


def get_relation_info(name):
    for key in service_relation:
        if key in name:
            return service_relation[key]
    return None